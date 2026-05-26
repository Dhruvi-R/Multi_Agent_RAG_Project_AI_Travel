# Multi_Agent_RAG_Project_AI_Travel

A Multi-Agent AI Travel Planner built using LangGraph, Groq LLM, Tavily Search, AviationStack API, PostgreSQL, and Streamlit.

---

# Features

- Flight Search using AviationStack API
- Hotel Search using Tavily API
- AI Travel Itinerary Generation
- PostgreSQL Memory Checkpoints
- Streamlit Web Interface
- Logging System

---

# Tech Stack

- Python
- LangGraph
- LangChain
- Groq
- PostgreSQL
- Streamlit

---

# Project Structure

```bash
Multi_Agent_RAG_Project_AI_Travel/
│
├── main.py
├── streamlit.py
├── requirements.txt
├── .env
├── travel_app.log
│
├── tools/
│   ├── flight_tool.py
│   └── tavily_tool.py
```

---

# Installation

## Clone Repository

```bash
git clone <repo_link>

cd Multi_Agent_RAG_Project_AI_Travel
```

---

## Create Virtual Environment

### Linux / Mac

```bash
python3 -m venv myenv

source myenv/bin/activate
```

### Windows

```bash
python -m venv myenv

myenv\Scripts\activate
```

---

## Install Requirements

```bash
pip install -r requirements.txt
```

---

# PostgreSQL Setup

Install PostgreSQL and create database:

```sql
CREATE DATABASE langgraph_memory;
```

---

# Environment Variables

Create `.env` file in project root:

```env
GROQ_API_KEY=your_groq_api_key

TAVILY_API_KEY=your_tavily_api_key

AVIATIONSTACK_API_KEY=your_aviationstack_api_key

DATABASE_URL=postgresql://postgres:password@localhost:5432/langgraph_memory
```

---

# Run Project

## Streamlit Web App

```bash
streamlit run streamlit.py
```

---

## Terminal Version

```bash
python3 main.py
```

---

# Logging

Logs are stored in:

```bash
travel_app.log
```

Example logs:

```text
Flight Agent Started
Hotel Agent Completed
Itinerary Generated Successfully
```

---

# Memory

The project uses PostgreSQL checkpoints for long-term memory.

Checkpoint tables are automatically created inside PostgreSQL.

---

# APIs Used

## Tavily API
https://www.tavily.com/

## AviationStack API
https://aviationstack.com/

## Groq API
https://console.groq.com/

---

# Author

Dhruvi Rupera
