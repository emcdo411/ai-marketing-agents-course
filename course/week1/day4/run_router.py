# run_router.py
"""
CLI entrypoint to run Day 4 router with pretty output.
- Pretty-prints BI rows as a table if present
- Prints intent, confidence, and explanation clearly
"""

import argparse
import json
from tabulate import tabulate  # pip install tabulate

from build_router import build_router_app


def main():
    parser = argparse.ArgumentParser(description="Run Router -> (BI|Product|Email|Analyst) graph.")
    parser.add_argument("--q", type=str, required=True, help="User question to route.")
    args = parser.parse_args()

    app = build_router_app()
    state = {"question": args.q, "intent": "", "confidence": 0.0, "answer": ""}

    result = app.invoke(state)

    print("\n=== INTENT / CONFIDENCE ===")
    print(result.get("intent"), result.get("confidence"))

    # If BI, pretty print structured JSON
    if result.get("intent") == "BI":
        print("\n=== BI TEMPLATE / PARAMS ===")
        print("Template:", result.get("template"))
        print("Params:", json.dumps(result.get("params", {}), indent=2, ensure_ascii=False))
        print("Latency (s):", result.get("latency_s"))

        rows = result.get("rows", [])
        if rows:
            print("\n=== ROWS (first 10) ===")
            headers = list(rows[0].keys())
            table = [list(r.values()) for r in rows[:10]]
            print(tabulate(table, headers=headers, tablefmt="grid"))

        print("\n=== EXEC SUMMARY ===")
        print(result.get("explanation", ""))

    else:
        # Default to Analyst, Product, or Email results
        print("\n=== ANSWER ===")
        # Some nodes may already return a string under "answer"
        answer = result.get("answer", "")
        if isinstance(answer, dict):
            print(json.dumps(answer, indent=2, ensure_ascii=False))
        else:
            print(answer)


if __name__ == "__main__":
    main()
