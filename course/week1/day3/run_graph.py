# run_graph.py
"""
CLI entrypoint to run Day 3 segment analysis.

Examples:
    python run_graph.py --segment 2 --limit 50
"""
import argparse
from build_graph import invoke_segment_analysis

def main():
    parser = argparse.ArgumentParser(description="Run START->segment_analyzer->END graph.")
    parser.add_argument("--segment", type=int, default=2, help="Segment ID (if your table has 'segment'; otherwise just for context).")
    parser.add_argument("--limit", type=int, default=50, help="Row preview limit for the LLM prompt.")
    args = parser.parse_args()

    result = invoke_segment_analysis(segment_id=args.segment, limit=args.limit)

    print("\n=== RESPONSE ===\n", result.get("response", ""))
    print("\n=== INSIGHTS ===\n", result.get("insights", ""))
    print("\n=== SUMMARY TABLE ===\n", result.get("summary_table", ""))

if __name__ == "__main__":
    main()
