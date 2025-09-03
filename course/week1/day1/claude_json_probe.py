# claude_json_probe.py
import json
from anthropic_client import ClaudeClient

SYSTEM = "You are a strict JSON generator. Only output valid JSON."
USER = """
Return: {"response": string, "insights": [string], "summary_table":[{"metric":string,"value":string}]}
Use short, business-friendly wording. No extra keys.
"""

if __name__ == "__main__":
    client = ClaudeClient()
    out = client.json_call(SYSTEM, USER, max_tokens=400)
    try:
        parsed = json.loads(out)
        print(json.dumps(parsed, indent=2))
    except Exception:
        print("Raw model output (not JSON):")
        print(out)
