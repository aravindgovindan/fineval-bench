import asyncio
import json
import os
import re
from tasks import evaluate_financial_summary

async def run_agent_simulation(agent_type: str, company_name: str):
    print(f"Testing agent type: {agent_type} for company: {company_name}")

    task_gen = evaluate_financial_summary.__wrapped__(company_name=company_name)
    prompt = await task_gen.__anext__()

    if agent_type == "Compliant Agent":
        with open("input_financials.json", "r") as f:
            data = json.load(f)
        total_rev = sum(data.values())
        margin_match = re.search(r"profit margin of ([0-9.]+)%", prompt)
        margin_pct = float(margin_match.group(1)) / 100.0 if margin_match else 0.20
        net_profit = round(total_rev * margin_pct, 2)

        output = {"total_revenue": total_rev, "net_profit": net_profit}

    elif agent_type == "Flawed Logic Agent":
        with open("input_financials.json", "r") as f:
            data = json.load(f)
        total_rev = sum(data.values())
        net_profit = 99999.99  # Incorrectly using a fixed 15% margin

        output = {"total_revenue": total_rev, "net_profit": net_profit}

    elif agent_type == "Reward Hacker/Corrupt Agent":
        output = {"status": "complete", "total_revenue": 9999999, "net_profit": 9999999}  # Arbitrary high values
    
    with open("summary.json", "w") as f:
        json.dump(output, f, indent=2)

    try:
        reward = await task_gen.asend("Action completed")
    except StopAsyncIteration as e:
        reward = e.value

    print(f"Agent type: {agent_type}, Reward received: {reward}/1.0\n")

    return {"agent_type": agent_type, "reward": reward}


async def main():
    agents = ["Compliant Agent", "Flawed Logic Agent", "Reward Hacker/Corrupt Agent"]
    results = []
    for idx, agent in enumerate(agents):
        res = await run_agent_simulation(agent, f"Company_{idx+1}")
        results.append(res)

    print("\n" + "="*45)
    print("Summary of Agent Simulation Results:")
    print("="*45)

    for res in results:
        status = "PASSED" if res["reward"] == 1.0 else ("PARTIAL" if res["reward"] == 0.5 else "FAILED")
        print(f"Agent Type: {res['agent_type']}, Reward: {res['reward']}/1.0, Status: {status}")
        print("="*45)

if __name__ == "__main__":
    asyncio.run(main())