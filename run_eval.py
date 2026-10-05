import asyncio
import json
import re
from tasks import evaluate_financial_summary

async def run_local_test():
    print("Starting local test for evaluate_financial_summary...")

    task_gen = evaluate_financial_summary.__wrapped__(company_name="Test Corp")

    prompt = await task_gen.__anext__()
    print("\n[Yield 1] Task Prompt generated:\n", prompt)

    print("\n[Simulating Agent Action] Writing output to 'summary.json'...")

    with open("input_financials.json", "r") as f:
        input_data = json.load(f)
    
    total_rev = (
        input_data["Q1_Revenue"] + input_data["Q2_Revenue"] + input_data["Q3_Revenue"] + input_data["Q4_Revenue"]
    )

    margin_match = re.search(r"profit margin of ([0-9.]+)%", prompt)
    margin_pct = float(margin_match.group(1)) / 100.0 if margin_match else 0.20
    net_profit = round(total_rev * margin_pct, 2)

    summary_output = {
        "total_revenue": total_rev,
        "net_profit": net_profit
    }

    with open("summary.json", "w") as f:
        json.dump(summary_output, f, indent=2)

    print(f"\n[Agent Action] Output written to 'summary.json' with total_revenue: {total_rev}, net_profit: {net_profit}")

    try:
        reward = await task_gen.asend("Action completed")
    except StopAsyncIteration as e:
        reward = e.value

    print(f"\n[Yield 2] final reward received: {reward}/1.0")

if __name__ == "__main__":
    asyncio.run(run_local_test())