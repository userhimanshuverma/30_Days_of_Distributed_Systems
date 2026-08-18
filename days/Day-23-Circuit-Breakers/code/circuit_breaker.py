#!/usr/bin/env python3
"""
Day 23 — Circuit Breaker Implementation (Educational Model)
-----------------------------------------------------------
This module provides a zero-dependency, self-contained implementation of the
classic 3-state Circuit Breaker pattern (CLOSED, OPEN, HALF-OPEN).

Goal:
    Prevent a client service from sending traffic to a failing downstream dependency,
    protecting application resources (threads, sockets, queues) and allowing the
    dependency time to recover.

States:
    - CLOSED: Normal operation. Requests pass through. Failures are monitored.
    - OPEN: Dependency is failing. Requests fail fast (or execute fallback) immediately.
    - HALF-OPEN: Recovery trial period. A limited number of test requests are allowed
                 through to probe downstream health.

NOTE: This is an educational implementation designed for clarity and teaching.
      Production circuit breakers (such as Resilience4j or Envoy) typically use
      sliding-window error rates, concurrency semaphores, and thread isolation.
"""

import time
import enum
import logging
from typing import Callable, Any, Optional

# Configure logging for demo output
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger("CircuitBreaker")


class CircuitState(enum.Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


class CircuitBreakerOpenException(Exception):
    """Raised when a call is short-circuited while the circuit is in the OPEN state."""
    pass


class CircuitBreaker:
    """
    A 3-State Circuit Breaker managing outbound calls to a downstream dependency.

    Parameters:
        failure_threshold (int): Number of consecutive failures before tripping the circuit OPEN.
        recovery_timeout (float): Time in seconds the circuit stays OPEN before probing in HALF-OPEN.
        expected_exception (Exception): Exception class considered a downstream failure (default: Exception).
        fallback (Callable): Optional fallback function to invoke when circuit is OPEN or call fails.
    """

    def __init__(
        self,
        failure_threshold: int = 3,
        recovery_timeout: float = 3.0,
        expected_exception: type = Exception,
        fallback: Optional[Callable[..., Any]] = None,
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        self.fallback = fallback

        # Internal state variables
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_state_change = time.time()
        self.half_open_trial_in_flight = False

    def __call__(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """
        Wrap and execute a target dependency call with circuit breaker protection.
        """
        return self.call(func, *args, **kwargs)

    def call(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """
        Executes the function with circuit breaker state management.
        """
        # Step 1: Evaluate state and transition from OPEN to HALF-OPEN if recovery timeout has elapsed
        self._check_state_transition()

        # Step 2: Handle OPEN state (Short-circuiting)
        if self.state == CircuitState.OPEN:
            logger.warning(
                f"[SHORT-CIRCUIT] Call to '{func.__name__}' blocked [State: OPEN, Failures: {self.failure_count}]"
            )
            if self.fallback:
                return self.fallback(*args, **kwargs)
            raise CircuitBreakerOpenException(
                f"Circuit breaker is OPEN. Downstream dependency '{func.__name__}' is unavailable."
            )

        # Step 3: Attempt execution for CLOSED or HALF-OPEN states
        try:
            logger.info(f"Executing call to '{func.__name__}' [State: {self.state.value}]")
            result = func(*args, **kwargs)
            
            # Step 4: Handle Successful Call
            self._on_success()
            return result

        except self.expected_exception as exc:
            # Step 5: Handle Failed Call
            logger.error(f"[FAILURE] Call to '{func.__name__}' failed with exception: {exc}")
            self._on_failure()

            if self.fallback:
                logger.info("Executing fallback function after failure.")
                return self.fallback(*args, **kwargs)
            raise exc

    def _check_state_transition(self) -> None:
        """
        Checks if the recovery window has passed while in OPEN state.
        If elapsed, transitions to HALF-OPEN to allow a trial request.
        """
        if self.state == CircuitState.OPEN:
            elapsed = time.time() - self.last_state_change
            if elapsed >= self.recovery_timeout:
                self._transition_to(CircuitState.HALF_OPEN)
                logger.info(
                    f"[TIMEOUT ELAPSED] Recovery timeout window ({self.recovery_timeout}s) passed. Transitioning OPEN -> HALF-OPEN."
                )

    def _on_success(self) -> None:
        """
        Called when a dependency call completes successfully.
        """
        if self.state == CircuitState.HALF_OPEN:
            logger.info("[PROBE SUCCESS] Probe request succeeded in HALF-OPEN state. Resetting circuit -> CLOSED.")
            self.failure_count = 0
            self._transition_to(CircuitState.CLOSED)
        elif self.state == CircuitState.CLOSED:
            # Reset consecutive failure counter on success in CLOSED state
            if self.failure_count > 0:
                logger.info(f"Resetting failure counter from {self.failure_count} to 0 after success.")
                self.failure_count = 0

    def _on_failure(self) -> None:
        """
        Called when a dependency call raises an expected exception.
        """
        self.failure_count += 1

        if self.state == CircuitState.HALF_OPEN:
            logger.warning("[PROBE FAILURE] Probe request failed in HALF-OPEN state. Re-tripping circuit -> OPEN.")
            self._transition_to(CircuitState.OPEN)

        elif self.state == CircuitState.CLOSED:
            logger.warning(f"Failure recorded in CLOSED state ({self.failure_count}/{self.failure_threshold}).")
            if self.failure_count >= self.failure_threshold:
                logger.warning(
                    f"[TRIPPED] Failure threshold ({self.failure_threshold}) reached! Tripping circuit CLOSED -> OPEN."
                )
                self._transition_to(CircuitState.OPEN)

    def _transition_to(self, new_state: CircuitState) -> None:
        """
        Internal state transition helper.
        """
        old_state = self.state
        self.state = new_state
        self.last_state_change = time.time()
        logger.info(f"[STATE TRANSITION] {old_state.value} ===> {new_state.value}")
