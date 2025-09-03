REM ensure deps
pip install anthropic langgraph pandas sqlalchemy python-dotenv

REM run examples
cd ai-marketing-agents-course\course\week1\day4
python run_router.py --q "What is the average p1 by member_rating for the last 60 days?"
python run_router.py --q "Which features should we highlight for high-frequency buyers?"
python run_router.py --q "Draft a short outreach email to Segment 2 about renewals."
python run_router.py --q "Give me a quick summary of Segment 1 behavior."
