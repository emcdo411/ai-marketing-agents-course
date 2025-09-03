REM Ensure dependencies
pip install langgraph pandas sqlalchemy python-dotenv anthropic

REM From repo root or day3 folder:
cd ai-marketing-agents-course\course\week1\day3

REM Run with a segment preview of 50 rows
python run_graph.py --segment 2 --limit 50
If your customer_features table doesn’t yet have a segment column, the code will automatically fall back to a simple LIMIT sample. (You’ll add segments when you run your KMeans process later.)

Want me to proceed to Day 4 next (Router node + conditional edges + “BI/Product/Email/Analyst” stubs), also all in .py with a clean README?
