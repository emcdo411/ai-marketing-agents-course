# run_router.py
"""
CLI entrypoint to run Day 4 router.

Examples:
    python run_router.py --q "What is the average p1 by member_rating for the last 60 days?"
"""
import argparse
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
    print("\n=== ANSWER ===")
    print(result.get("answer", ""))

if __name__ == "__main__":
    main()
