# 📘 Week 1 — Day 1  
**Topic:** Setting Up Claude Client, LangGraph Basics, and JSON Output Discipline  

---

## 🎯 Learning Objectives
- Install and configure Anthropic’s Claude API client.  
- Understand environment variables and `.env` usage.  
- Create a reusable `ClaudeClient` wrapper class.  
- Ensure outputs are **strict JSON** for downstream reliability.  
- Run your first **LangGraph node** with START → END.  

---

## 🗂 Agenda
1. **Environment Setup**  
   - Install dependencies:  
     ```bash
     pip install anthropic langgraph langchain-core langchain-anthropic python-dotenv
     ```
   - Create `.env` with:
     ```ini
     ANTHROPIC_API_KEY=your_api_key_here
     CLAUDE_MODEL=claude-3-5-sonnet-latest
     ```

2. **Claude Client “Hello World”**  
   - Build a wrapper (`anthropic_client.py`) that enforces JSON-only responses.  
   - Test with `claude_json_probe.py`.

3. **LangGraph Primer**  
   - Define a minimal state.  
   - Add a node → connect START → END.  
   - Print the results.  

---

## 🧑‍💻 Exercises
1. **Environment Check**  
   - Run `pip list | findstr anthropic` to confirm Anthropic SDK is installed.  
   - Verify `.env` loads with `python -m dotenv`.

2. **JSON Probe**  
   - Run:  
     ```bash
     python claude_json_probe.py
     ```  
   - Confirm it prints valid JSON like:
     ```json
     {
       "response": "Short exec summary",
       "insights": ["Point A", "Point B"],
       "summary_table": [{"metric": "avg_p1", "value": "0.85"}]
     }
     ```

3. **LangGraph Mini Node**  
   - Build a `segment_analyzer` node that just echoes input data.  
   - Run graph with:
     ```bash
     python segment_analyzer_node.py
     ```

---

## 📊 Business Context
- Enterprise AI must **always output parseable JSON** (no “chatty” text).  
- Claude Code + LangGraph = reliable, auditable workflows.  
- Today’s lesson builds the foundation for **multi-agent orchestration** later in the week.

---

## ✅ Deliverables
- `course/week1/day1/anthropic_client.py`  
- `course/week1/day1/claude_json_probe.py`  
- `course/week1/day1/segment_analyzer_node.py`  

---

## 📌 Next (Day 2 Preview)
- Build a **feature store** (purchase frequency, recency).  
- Create a **bot harness** that runs prompts through Claude + validates JSON outputs.  
- Learn how to measure **latency + reliability** → foundations for “10x the bot” engineering.  

