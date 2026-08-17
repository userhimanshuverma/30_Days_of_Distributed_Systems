# Day 22 Visual Assets Specification

This directory holds visual specifications and asset placeholders for **Day 22 — Timeouts: The Bounded Waiting Principle**.

---

## 🎨 Required Asset Specifications

### 1. `timeout-lifecycle.png`
* **Description**: Visualizing the transition from an open socket request to a timed-out client state, demonstrating how time elapsed reaches a boundary while the remote server state remains ambiguous.
* **Layout**:
  * **Top Canvas Header**: "The Lifecycle of Bounded Waiting ($t_{\text{start}} \rightarrow t_{\text{timeout}}$)"
  * **Timeline View**: Horizontal timeline showing request initiation at $t=0$, in-flight network transit, and the hard deadline boundary at $t=1,000\text{ms}$.
  * **Client Node (Left)**: Dark blue card showing active socket thread waiting on I/O. At $t=1,000\text{ms}$, the socket throws `ErrTimeout`, frees the thread, and returns an error response.
  * **Network Pipe (Center)**: Dotted vector with lost or delayed packet icon (`POST /checkout`).
  * **Server Node (Right)**: Dark grey box labeled "Ambiguous State" (could be processing slowly, crashed, or completed but response dropped).
  * **Callout Banner**: "⚠️ Timeout halts client waiting. It does NOT report or change server state."
* **Visual Style**: Sleek modern dark mode, royal blue and crisp yellow highlights, soft drop shadows, clean latency badges ($1,000\text{ms}$ limit).

---

## 2. `deadline-propagation.png`
* **Description**: Visualizing end-to-end deadline budget decay as a user request travels through a multi-tier microservice architecture.
* **Layout**:
  * **Top Canvas Header**: "Distributed Time Budget & Deadline Propagation"
  * **Request Pipeline**:
    * **Client (Entry)**: Sets total time budget $T_{\text{budget}} = 2,000\text{ms}$.
    * **Service A (API Gateway)**: Consumes $300\text{ms}$. Passes remaining budget $1,700\text{ms}$ in HTTP Header (`X-Deadline: 1700ms` / gRPC context).
    * **Service B (Order Service)**: Consumes $800\text{ms}$. Passes remaining budget $900\text{ms}$ downstream.
    * **Database (State Store)**: Receives $900\text{ms}$ deadline. Aborts query execution early if query exceeds $900\text{ms}$.
  * **Budget Meter**: Shrinking progress bar underneath each hop showing remaining millisecond allocation.
* **Visual Style**: High-contrast card layout, vibrant emerald to amber budget bar, clear mathematical subtraction markers (e.g., $2000 - 300 = 1700\text{ms}$).

---

## 3. `timeout-retry-loop.png`
* **Description**: Visualizing the destructive feedback loop when client timeouts trigger unthrottled immediate retries against an already overloaded backend.
* **Layout**:
  * **Top Canvas Header**: "The Timeout + Immediate Retry Failure Loop"
  * **Circular Loop Diagram**:
    1. **Slow Dependency**: Database processing latency surges to $2,500\text{ms}$.
    2. **Client Timeout**: Client timeout triggers at $1,000\text{ms}$.
    3. **Immediate Retry**: Client issues 2nd and 3rd retry attempts immediately.
    4. **Amplified Inbound Load**: Target database traffic surges by $300\%$, increasing latency to $10,000\text{ms}$.
    5. **Total Outage**: Thread pools exhaust, connection pools drain, and cascading failure spreads upstream.
  * **Warning Callout Banner**: "🔥 Unbounded retries after timeouts amplify failure instead of restoring resilience."
* **Visual Style**: Deep red and orange alert accents, glowing feedback arrows, bold typography, clear failure amplification multiplier badges ($3\times \text{Load}$).
