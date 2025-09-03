# 📘 Week 1 — Day 2  
**Topic:** Database Connections & Feature Engineering for AI Systems  

---

## 🎯 Learning Objectives
- Connect to relational databases (SQLite → Postgres).  
- Perform basic **feature engineering**:  
  - `purchase_frequency`  
  - `recency_days`  
  - `member_rating`  
- Store engineered features in a **SQLite feature store**.  
- Build foundations for **Claude-powered BI/Analytics nodes** later in the week.  

---

## 🗂 Agenda
1. **Database Setup**  
   - Install dependencies:  
     ```bash
     pip install sqlalchemy psycopg2 pandas
     ```
   - Create a local SQLite DB (`data/leads_scored_segmentation.db`).  
   - (Optional) Connect to Postgres with DSN string:  
     ```
     postgresql+psycopg2://user:password@localhost:5432/dbname
     ```

2. **Feature Engineering Basics**  
   - `purchase_frequency`: # of transactions per user.  
   - `recency_days`: days since last transaction.  
   - `member_rating`: imported from leads table.  

3. **Feature Store Creation**  
   - Merge features into one DataFrame.  
   - Save to `customer_features` table in SQLite.  

---

## 🧑‍💻 Exercises
1. **SQLite Primer**  
   - Open SQLite shell:  
     ```bash
     sqlite3 data/leads_scored_segmentation.db
     ```
   - Run:  
     ```sql
     .tables
     SELECT * FROM leads_scored LIMIT 5;
     ```

2. **Build Feature Store**  
   - Run `build_features.py` to generate `customer_features` table.  
   - Inspect table in SQLite:  
     ```sql
     SELECT user_email, purchase_frequency, recency_days, member_rating
     FROM customer_features LIMIT 10;
     ```

3. **Query with Pandas**  
   - Use `pd.read_sql` to preview engineered features.  
   - Verify nulls are filled (`0` for frequency, `365` for recency).  

---

## 📊 Business Context
- **Why features matter:**  
  - Segmentation = better targeting for BI & marketing co-bots.  
  - Executives care about *frequency*, *recency*, and *rating* → they’re interpretable and actionable.  
- By the end of Day 2, you’ll have a **working feature store** that Claude can analyze in Day 3.  

---

## ✅ Deliverables
- `course/week1/day2/build_features.py` → builds & writes `customer_features` to SQLite.  
- Updated SQLite DB with `customer_features` table.  

---

## 📌 Next (Day 3 Preview)
- Learn LangGraph nodes in depth.  
- Implement `segment_analyzer` that ingests features and outputs exec insights.  
- Build a working START → Node → END pipeline.  

