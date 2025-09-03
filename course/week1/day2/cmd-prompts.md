REM 1) Seed the source tables
cd ai-marketing-agents-course\course\week1\day2
python seed_sample_data.py

REM 2) Build engineered features
python build_features.py

REM 3) Inspect the results (SQLite CLI optional)
sqlite3 ..\..\..\data\leads_scored_segmentation.db
.tables
SELECT * FROM customer_features LIMIT 10;
