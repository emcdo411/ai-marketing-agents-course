# 🎤 Trainer’s Script — Week 1 Day 3  
**Topic:** LangGraph Deep Dive — State, Nodes, and Executable Graphs (Claude-powered)  

---

## 🕒 Suggested Timing
- Intro & Context: **10 min**  
- Step 1 (State): **15 min**  
- Step 2 (Node): **20 min**  
- Step 3 (Build Graph): **20 min**  
- Step 4 (CLI Run & Discussion): **25 min**  
- Wrap-Up & Q&A: **10 min**  

Total: **~100 minutes (1h 40m)**  

---

## 🎯 Trainer Goals
- Help learners **see LangGraph as a workflow tool, not just code**.  
- Reinforce the importance of **typed state** (predictability).  
- Show how Claude can return **structured insights**, not just chatty text.  
- Build confidence by running a graph **end-to-end** with real DB data.  

---

## 🧩 Teaching Steps

### 1. Context Setting (10 min)
**Say this:**  
> “Today we’re going to connect all the pieces we’ve been building: the database features from Day 2, and the Claude client from Day 1.  
> The goal is to build a simple pipeline: START → ANALYZE → END. This is our first real AI workflow.”

**Ask learners:**  
- “Why do you think it’s useful to have AI return JSON instead of free text?”  
- “What problems might happen if the output format changes unpredictably?”  

---

### 2. Step 1 — Define the State (15 min)
**Explain:**  
- State = a common format that flows through the graph.  
- Think of it as a **form** that every node agrees to fill out.  

**Action:**  
- Show `state_types.py`.  
- Walk through each field (`segment_id`, `sample_df_json`, `response`, `insights`, `summary_table`).  

**Prompt learners:**  
- “Which of these fields do you think executives would find most useful?”  
- “If we added one more field, what would it be?” (chart_json is optional).  

---

### 3. Step 2 — Build the Segment Analyzer Node (20 min)
**Explain:**  
- This is the Claude-powered step.  
- It takes a JSON preview of a segment and returns **structured insights**.  

**Action:**  
- Open `segment_analyzer_node.py`.  
- Highlight how it calls Claude and enforces JSON output.  

**Prompt learners:**  
- “Why might we only send a preview of the data, not the whole table?”  
- “What risks do we reduce by sending a sample?”  

---

### 4. Step 3 — Build the Graph (20 min)
**Explain:**  
- LangGraph is just a way to connect steps into a **flowchart in code**.  
- We define START, connect to the node, and then END.  

**Action:**  
- Show `build_graph.py`.  
- Point out how edges are wired.  

**Prompt learners:**  
- “If you had multiple nodes, how would you decide which comes first?”  
- “Can you think of another use case for START → END graphs outside AI?”  

---

### 5. Step 4 — Run the Graph from CLI (25 min)
**Explain:**  
- We’ll run the graph like a mini-application.  
- `run_graph.py` lets us test with real inputs (segment ID + row limit).  

**Action:**  
- Demo:  
  ```bash
  python run_graph.py --segment 2 --limit 50
````

* Show the output: RESPONSE, INSIGHTS, SUMMARY TABLE.

**Prompt learners:**

* “Does this look like something you could hand directly to an executive?”
* “How is this different from a normal ChatGPT answer?”

---

## 📊 Wrap-Up (10 min)

**Summarize:**

* State = reliability.
* Node = reusable building block.
* Graph = flow from START to END.
* CLI = practical way to test and integrate.

**Preview Day 4:**

> “Tomorrow we’ll add a **Router Node** — instead of one path, the graph will branch into BI, Product, or Email analysis automatically. That’s the start of multi-agent orchestration.”

---

## 🎤 Tips for Trainers

* Keep emphasizing **business relevance** — this isn’t just “toy code.”
* Pause after each code walkthrough and ask: *“How would you explain this to a non-technical exec?”*
* Encourage learners to **experiment with segment IDs** — each run should look a little different.
