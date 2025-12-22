# 🧠 Agent-to-Agent (A2A) Workflow using LangGraph + MCP

This project demonstrates a **simple Agent-to-Agent (A2A) system** built using:

- **LangChain Agents**
- **LangGraph** for orchestration
- **MCP (Model Context Protocol)** servers as tools
- **OpenAI models**

Two agents share state, call tools via MCP, and collaboratively solve a task.

---

## 📦 What This Project Does

- Runs a **local MCP math server** (add, multiply)
- Converts MCP tools into **LangChain tools**
- Creates **two independent agents**:
  - Agent 1 solves the task
  - Agent 2 reviews / extends the solution
- Orchestrates them using **LangGraph**
- Tracks **tool calls** using callbacks
- Shares context between agents via a **shared state**

---

## 🗂️ Project Structure

```text
.
├── agent.py           # Builds and exports agent1 and agent2
├── mcp_server.py      # MCP math server (add, multiply)
├── workflow.py        # LangGraph A2A workflow
├── .env               # OpenAI API key
├── requirements.txt   # Dependencies
└── README.md
```

---

## 🔧 Core Components Explained

### 1️⃣ MCP Server (`mcp_server.py`)

This is a **local tool server** that exposes math operations:

- `add(a, b)`
- `multiply(a, b)`

Agents call these tools **indirectly** via MCP.

---

### 2️⃣ Agents (`agent.py`)

- Uses `MultiServerMCPClient` to discover tools
- Converts MCP tools into LangChain tools
- Creates **two agents** using the same model and tools
- Exports them for reuse

```python
from agent import agent1, agent2
```

Agents are built **once**, not per request.

---

### 3️⃣ Workflow (`workflow.py`)

The workflow is defined using **LangGraph**.

#### Agent responsibilities:
- **Agent 1**
  - Receives the user question
  - Solves it using tools if needed
- **Agent 2**
  - Receives Agent 1’s output
  - Validates, analyzes, or extends the answer

#### Shared state:
```python
{
  "question": "...",
  "responses": [...]
}
```

Agents read from and write to this state.

---

### 4️⃣ Tool Callback

A callback prints tool usage in real time:

```text
🔧 Tool started → add
🔧 Tool started → multiply
```

This helps you understand:
- When tools are invoked
- Which agent is calling which tool

---

## 🚀 Getting Started

### 1️⃣ Clone the repository

```bash
git clone <your-repo-url>
cd a2a_agent
```

---

### 2️⃣ Create and activate a virtual environment

```bash
python -m venv venv
venv\\Scripts\\activate   # Windows
```

---

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Set your OpenAI API key

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

---

## ▶️ Running the Workflow

```bash
python workflow.py
```

---

## 🧪 Example Output

```text
🧠 AGENT 1
📥 Question:
  Add 3 and 5, then multiply by 12
🔧 Tool started → add
🔧 Tool started → multiply
📤 Agent 1 Response:
  The sum is 8, multiplied by 12 gives 96.

🧠 AGENT 2
📥 Context Prompt:
  User Asked + Agent 1 Response
🔧 Tool started → multiply
📤 Agent 2 Final Response:
  The calculation is correct. Final answer: 96.
```

---

## 🧭 How to Understand the Workflow

1. **Entry Point**
   - User question enters the graph

2. **Agent 1 Node**
   - Receives the question
   - Calls MCP tools
   - Writes its response to shared state

3. **Agent 2 Node**
   - Reads Agent 1’s response
   - Validates or extends it
   - Writes final output

4. **Graph Ends**
   - Workflow completes after Agent 2

---

## 🧠 Key Concepts Demonstrated

- Agent-to-Agent (A2A) communication
- MCP as a tool abstraction layer
- LangGraph state-based orchestration
- Tool-calling via LLMs
- Callback-based observability

---

## 🔜 Possible Extensions

- Conditional routing between agents
- Supervisor agent pattern
- Role-based tool access
- RAG as an MCP server
- Tool usage auditing
- Multi-agent debate workflows

---

## ✅ Summary

This project is a **minimal but production-style example** of:

> Agents + Tools + Shared State + Graph-based orchestration

Ideal for learning **modern multi-agent systems** with LangChain + LangGraph + MCP.

