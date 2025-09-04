# eval_harness.py
"""
Tiny evaluation harness:
- Golden cases (question -> expected template)
- Measures template selection accuracy and latency

Run:
  python eval_harness.py
"""
from __future__ import annotations
import time, json
from typing import List, Dict

from bi_templates_runner import pick_template, exec_bi

GOLDENS: List[Dict[str, str]] = [
    {"q": "What's the average p1 by segment for the last 60 days?", "expected": "avg_p1_by_segment"},
    {"q": "How many users per member rating?", "expected": "count_by_member_rating"},
    {"q": "Show top purchase frequency by segment in the last 30 days", "expected": "top_purchase_frequency_by_segment"},
    {"q": "Average p1 by member rating over recent users", "expected": "avg_p1_by_member_rating"},
]

def main():
    correct = 0
    latencies = []
    results = []

    for case in GOLDENS:
        t0 = time.time()
        chosen = pick_template(case["q"])
        dt = time.time() - t0
        latencies.append(dt)
        ok = int(chosen == case["expected"])
        correct += ok
        results.append({"q": case["q"], "expected": case["expected"], "chosen": chosen, "ok": ok, "latency_s": round(dt, 3)})

    acc = correct / len(GOLDENS)
    print(f"\nTemplate selection accuracy: {acc:.2%}")
    print("Avg selection latency (s):", round(sum(latencies)/len(latencies), 3))
    print("\nPer-case results:")
    for r in results:
        print(json.dumps(r, ensure_ascii=False))

    # Optional: run one full BI execution to ensure E2E works
    print("\n--- E2E Sample ---")
    sample = exec_bi("What's the average p1 by segment for the last 90 days?")
    print(json.dumps({
        "template": sample["template"],
        "params": sample["params"],
        "latency_s": sample["latency_s"],
        "rows_preview": sample["rows"][:3],
        "summary": sample["explanation"][:250]
    }, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
