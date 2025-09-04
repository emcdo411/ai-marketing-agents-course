## 📘 Week 1 — Day 1: Step-by-Step Instructions

**Topic:** Setting Up Claude Client, LangGraph Basics, and JSON Output Discipline

---

### 1. Get Your Tools Ready

Think of this as gathering your “workbench.”

1. Open your terminal (Command Prompt or PowerShell on Windows, Terminal on Mac).
2. Type the following to install the tools you’ll need:

   ```bash
   pip install anthropic langgraph langchain-core langchain-anthropic python-dotenv
   ```

   * `anthropic`: lets you talk to Claude (AI model).
   * `langgraph`: helps connect steps together in a workflow.
   * `python-dotenv`: makes sure your secret keys don’t go into your code directly.

---

### 2. Save Your Secret Key

This is like giving your project the “password” to talk to Claude.

1. In the root of your project, create a new file called **`.env`**.
2. Paste in the following, replacing `your_api_key_here` with your actual Anthropic API key:

   ```ini
   ANTHROPIC_API_KEY=your_api_key_here
   CLAUDE_MODEL=claude-3-5-sonnet-latest
   ```
3. Save and close the file.

---

### 3. Say Hello to Claude (JSON Only)

You’re now going to build a tiny helper file that makes sure Claude speaks **only in clean, structured answers** (JSON).

1. In `course/week1/day1/`, create a file called **`anthropic_client.py`**.
2. Paste in the code your instructor provided — this creates a **ClaudeClient** that always enforces JSON rules.

---

### 4. Run Your First Probe

Now let’s test if Claude will follow the JSON rules.

1. In `course/week1/day1/`, create another file called **`claude_json_probe.py`**.
2. Add the probe code (it just asks Claude to respond in JSON).
3. In your terminal, run:

   ```bash
   python course/week1/day1/claude_json_probe.py
   ```
4. You should see an answer that looks like:

   ```json
   {
     "response": "Short exec summary",
     "insights": ["Point A", "Point B"],
     "summary_table": [{"metric": "avg_p1", "value": "0.85"}]
   }
   ```

---

### 5. Create Your First Node (LangGraph)

Think of a node as a single step in a flowchart. Today, the node will just **echo back some input**.

1. In `course/week1/day1/`, create a file called **`segment_analyzer_node.py`**.
2. Paste in the starter code that sets up:

   * A `START` state.
   * A `segment_analyzer` node (simple function).
   * An `END` state.
3. Run it with:

   ```bash
   python course/week1/day1/segment_analyzer_node.py
   ```
4. You should see the input and output printed out — proving that LangGraph is wired up.

---

### 6. Business Context (Why This Matters)

* AI in companies must produce **clean, reliable JSON**, not chatty text.
* Today you set up the foundation: Claude + LangGraph + JSON discipline.
* This foundation is what lets you later build **multi-step, multi-agent AI systems** that can be trusted in business.

---

### ✅ By the End of Day 1 You Should Have

* ✔️ `anthropic_client.py` (Claude wrapper).
* ✔️ `claude_json_probe.py` (test Claude outputs JSON).
* ✔️ `segment_analyzer_node.py` (your first LangGraph node).
* ✔️ A working `.env` file with your Anthropic key.

---

👉 Next, in **Day 2**, you’ll build a **feature store** (like a mini database of customer traits) and connect it to Claude for richer insights.

---

Would you like me to also produce a **friendly checklist format** (like “tick boxes” ✅ you can mark off as you go), so you can use it directly during your Day 1 session?


