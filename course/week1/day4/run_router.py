# run_router.py
"""
CLI entrypoint to run Day 4 router with dual output modes:
- Default: pretty CLI output (tables for BI)
- --json: dump full structured JSON payload

Examples:
  python run_router.py --q "What's the average p1 by segment for the last 90 days?"
  python run_router.py --q "Draft a short outreach email to Segment 2 about renewals."
  python run_router.py --q "Give me a quick summary of Segment 1 behavior." --json
"""

import argparse
import json

from build_router import build_router_app

# Try to import tabulate for pretty tables; degrade gracefully if missing
try:
    from tabulate import tabulate  # pip install tabulate
    HAVE_TABULATE = True
except Exception:
    HAVE_TABULATE = False


def print_pretty(result: dict) -> None:
    """Human-friendly printing for router results."""
    intent = result.get("intent")
    conf = result.get("confidence")
    print("\n=== INTENT / CONFIDENCE ===")
    print(intent, conf)

    if intent == "BI":
        print("\n=== BI TEMPLATE / PARAMS ===")
        print("Template:", result.get("template"))
        print("Params:", json.dumps(result.get("params", {}), indent=2, ensure_ascii=False))
        print("Latency (s):", result.get("latency_s"))

        rows = result.get("rows", [])
        if rows:
            print("\n=== ROWS (first 10) ===")
            if HAVE_TABULATE:
                headers = list(rows[0].keys())
                table = [list(r.values()) for r in rows[:10]]
                print(tabulate(table, headers=headers, tablefmt="grid"))
            else:
                # Fallback if tabulate is not installed
                print(json.dumps(rows[:10], indent=2, ensure_ascii=False))

        print("\n=== EXEC SUMMARY ===")
        print(result.get("explanation", ""))

    else:
        print("\n=== ANSWER ===")
        answer = result.get("answer", "")
        # Some nodes may return dicts instead of strings
        if isinstance(answer, dict):
            print(json.dumps(answer, indent=2, ensure_ascii=False))
        else:
            print(answer)


def main():
    parser = argparse.ArgumentParser(description="Run Router -> (BI|Product|Email|Analyst) graph.")
    parser.add_argument("--q", type=str, required=True, help="User question to route.")
    parser.add_argument("--json", action="store_true", help="Output full structured JSON instead of pretty text.")
    args = parser.parse_args()

    app = build_router_app()
    state = {"question": args.q, "intent": "", "confidence": 0.0, "answer": ""}

    result = app.invoke(state)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print_pretty(result)


if __name__ == "__main__":
    main()
