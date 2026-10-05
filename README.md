# FinEval-Bench: AI Agent RL Evaluation & Verifier Suite

`FinEval-Bench` is an interactive evaluation environment built using the **HUD Python SDK (`hud`)**. It models financial data workflows for AI agents, replacing static text benchmarks with programmatic assertion verifiers and state-diff tracking to evaluate agent performance and prevent reward hacking.

## Problem Statement
Static LLM benchmarks evaluate outputs using fixed string matching, making them susceptible to:
1. **Reward Hacking:** Agents generating valid-looking JSON outputs without actually reading or computing inputs.
2. **Brittle Verifiers:** Failing agents due to minor formatting discrepancies despite correct mathematical logic.

## Solution Architecture
Built on HUD's **two-yield template pattern**:
* **Yield 1 (State Initialization):** Dynamically generates quarterly balance sheet data, writes `input_financials.json`, and yields the prompt to the agent.
* **Yield 2 (Programmatic Verifier):** Inspects the environment state (`summary.json`), checks calculation logic, handles float tolerance, and assigns a reward score between `0.0` and `1.0`.

## Directory Structure
fineval-bench/
├── tasks.py         # HUD Environment definition & verifier logic
├── run_eval.py      # Local single-execution harness
├── batch_eval.py    # Multi-agent simulation (Compliant vs Flawed vs Corrupt)
└── README.md        # Project documentation

## Quickstart

### 1. Setup Environment
```cmd
py -3.12 -m venv venv
.\venv\Scripts\activate
pip install hud pandas faker
```
### 2. Run Multi-Agent Benchmark Suite

```cmd
python batch_eval.py
```

