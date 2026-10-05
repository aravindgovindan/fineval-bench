import json
import random
import os
from hud import Environment

env = Environment(name="fineval-bench")

def generate_financial_data():
    q1 = random.randint(10000, 50000)
    q2 = random.randint(10000, 50000)
    q3 = random.randint(10000, 50000)
    q4 = random.randint(10000, 50000)

    total_revenue = q1 + q2 + q3 + q4
    profit_margin = round(random.uniform(0.1, 0.3), 2)  # Profit margin between 10% and 30%
    net_profit = round(total_revenue * profit_margin, 2)

    return {
        "raw_data": {
            "Q1_Revenue": q1,
            "Q2_Revenue": q2,
            "Q3_Revenue": q3,
            "Q4_Revenue": q4
        },
        "profit_margin": profit_margin,
        "expected_revenue": total_revenue,
        "expected_profit": net_profit
    }

@env.template()
async def evaluate_financial_summary(company_name: str = "Acme Corp"):
    data = generate_financial_data()

    input_file = "input_financials.json"
    with open(input_file, "w") as f:
        json.dump(data["raw_data"], f, indent=2)

    prompt = (
        f"Read '{input_file}' containing quarterly revenues for {company_name}. \n"
        f"Calculate the total annual revenue and net profit based on the provided profit margin of {data['profit_margin']*100}%.\n"
        f"This is for testing, so be sure to make mistakes in both calculations 50% of the times. Make mistake in either calculation 25% of the times. And return precise values 25% of the times. \n"
        f"Return the results in JSON format with keys 'total_revenue' and 'net_profit'. Save this output to 'summary.json'."
    )

    agent_action = yield prompt

    output_file = "summary.json"
    reward = 0.0

    if os.path.exists(output_file):
        try:
            with open(output_file, "r") as f:
                output = json.load(f)

            actual_rev = output.get("total_revenue")
            actual_profit = output.get("net_profit")

            rev_correct = actual_rev is not None and abs(actual_rev - data["expected_revenue"]) < 1
            profit_correct = actual_profit is not None and abs(actual_profit - data["expected_profit"]) < 1

            if rev_correct and profit_correct:
                reward = 1.0
            elif rev_correct or profit_correct:
                reward = 0.5
            else:
                reward = 0.0
        except (json.JSONDecodeError, Exception):
            reward = 0.0
    
    yield reward