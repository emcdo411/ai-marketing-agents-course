# 📦 Day 3 Demo Data (Trainer-Ready)

This guide walks you through setting up a **demo dataset** for Week 1 Day 3.  
The demo is designed so learners can run their **LangGraph + Claude node** against a realistic dataset without doing SQL setup manually.

---

## 🔍 What this does

When you run the demo script, it will:

1. Create (or overwrite) a SQLite database at:
data/leads_scored_segmentation.db

yaml
Copy code
2. Build two small source tables:
- `leads_scored` (5 rows) → customer scores & ratings  
- `transactions` (8 rows) → purchase history  
3. Call your Day 2 script to generate:
- `customer_features` (5 rows) → includes frequency, recency, and rating  
4. Print quick previews so you know it worked.  

---

## 📂 Where to put the script

The script file is already in the repo here:

ai-marketing-agents-course/
└─ course/
└─ week1/
└─ day3/
└─ seed_demo_data.py

yaml
Copy code

---

## ▶️ How to run (step-by-step, no coding)

### 1. Open your terminal and go to the repo root
```bash
cd ai-marketing-agents-course
2. Install the basics (only needed once)
bash
Copy code
pip install pandas sqlalchemy python-dotenv
3. Make sure you have an .env file at the repo root
Add this line (or rely on the default):

ini
Copy code
DATABASE_URL=sqlite:///data/leads_scored_segmentation.db
4. Run the demo seeder
bash
Copy code
python course/week1/day3/seed_demo_data.py
5. What you should see
✅ leads_scored and transactions tables created & filled

✅ customer_features table built

✅ Previews printed in your console

Example snippet:

pgsql
Copy code
✅ Seeded tables: leads_scored (5), transactions (8)
✅ Wrote 5 rows to table: customer_features
▶️ Run your Day 3 graph
After the demo data is loaded, test your Day 3 graph:

bash
Copy code
cd course/week1/day3
python run_graph.py --segment 2 --limit 50
Try changing the segment ID or row limit:

bash
Copy code
python run_graph.py --segment 0 --limit 25
🎓 Trainer Tips (for live sessions)
Timebox this step → it runs in just 1–2 seconds.

After the preview prints, ask learners:

“Which of these fields (frequency, recency, rating) would you show an executive first, and why?”

Then run the graph with different --segment values so learners see how summaries vary.

✅ You’re now ready to use the demo dataset for Day 3 LangGraph exercises.

yaml
Copy code

---

