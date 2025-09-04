# run_bi.py
"""
CLI entrypoint for BI template runner.

Examples:
  python run_bi.py --q "What's the average p1 by segment for the last 90 days?"
  python run_bi.py --q "How many users per member rating?"
"""
import argparse, json
from bi_templates_runner import exec_bi

def main():
    ap = argparse.ArgumentParser(description="Run BI co-bot (template-driven).")
    ap.add_argument("--q", type=str, required=True, help="BI question in natural language")
    args = ap.parse_args()

    result = exec_bi(args.q)
    print("\n=== TEMPLATE ===", result["template"])
    print("=== PARAMS ===", result["params"])
    print("=== LATENCY (s) ===", result["latency_s"])
    print("\n=== ROWS (JSON) ===")
    print(json.dumps(result["rows"], indent=2, ensure_ascii=False))
    print("\n=== EXEC SUMMARY ===\n", result["explanation"])

if __name__ == "__main__":
    main()
