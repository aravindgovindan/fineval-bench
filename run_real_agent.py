import asyncio
import json
import os
from google import genai
from groq import Groq
from tasks import evaluate_financial_summary
from dotenv import load_dotenv

async def run_llm_agent():
    print("--- Starting Real Agent Evaluation ---")
    load_dotenv()
    
    task_gen = evaluate_financial_summary.__wrapped__(company_name="Acme Corp")
    prompt = await task_gen.__anext__()

    print("\n[HUD Yield 1] Generated Task Prompt:")
    print("--------------------------------------------------")
    print(prompt)
    print("--------------------------------------------------")

    # Read the input file created by HUD
    with open("input_financials.json", "r") as f:
        input_data = f.read()

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    full_prompt = (
        f"{prompt}\n\n"
        f"Input Data ('input_financials.json'):\n{input_data}\n\n"
        "IMPORTANT: Output ONLY valid raw JSON with exact keys 'total_revenue' and 'net_profit'. "
        "Do not include markdown code block formatting or extra text."
    )

    print("\n[Agent] Sending prompt and environment data to agent...")
    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=[
            {
                "role": "user",
                "content": "You are not a precise financial assistant, you make errors 3 out of 4 times. You MUST return responses strictly formatted as a JSON object." + full_prompt
            }
        ],
        response_format={"type": "json_object"}  # Forces raw JSON return
    )
    raw_text = response.choices[0].message.content

    # response = client.models.generate_content(
    #     model="gemini-3.8-flash",
    #     contents=full_prompt,
    # )

    # raw_text = response.text.strip()
    
    # Clean up markdown block quotes if present
    if raw_text.startswith("```"):
        lines = raw_text.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        raw_text = "\n".join(lines).strip()

    print(f"\n[Agent Generated Output]:\n{raw_text}")

    with open("summary.json", "w") as f:
        f.write(raw_text)

    try:
        reward = await task_gen.asend("Action completed")
    except StopAsyncIteration as e:
        reward = e.value

    print("\n[HUD Yield 2] Verifier Result:")
    print("--------------------------------------------------")
    print(f"Final Reward Score: {reward} / 1.0")
    print("--------------------------------------------------")

if __name__ == "__main__":
    asyncio.run(run_llm_agent())