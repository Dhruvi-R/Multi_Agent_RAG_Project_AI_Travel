'''
# pip install langgraph langchain langchain-openai langchain-groq langchain-community langchain-tavily psycopg[binary] psycopg_pool python-dotenv tavily-python requests streamlit

# install PostgreSQL and create database

CREATE DATABASE langgraph_memory;

( or open pgadmin4 and create database there )
'''

# LangGraph Multi-Agent Travel Booking System with Long-Term Memory

# main.py

import os
from typing import TypedDict, Annotated
import operator
import logging
import psycopg

from langgraph.graph import (
    StateGraph,
    START,
    END
)

from langgraph.checkpoint.postgres import (
    PostgresSaver
)

from langchain_core.messages import (
    AnyMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
)

from langchain_groq import ChatGroq

from tools.tavily_tool import tavily_search
from tools.flight_tool import search_flights

from dotenv import load_dotenv

load_dotenv()

# ====================================================
# LOGGING
# ====================================================

logging.basicConfig(

    filename="travel_app.log",

    level=logging.INFO,

    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# ====================================================
# DATABASE
# ====================================================

DATABASE_URL = os.getenv(
    "DATABASE_URL"
)

# ====================================================
# LLM
# ====================================================

llm = ChatGroq(
    model="llama-3.3-70b-versatile"
)

# ====================================================
# STATE
# ====================================================

class TravelState(TypedDict):

    messages: Annotated[
        list[AnyMessage],
        operator.add
    ]

    user_query: str

    flight_results: str

    hotel_results: str

    itinerary: str

    llm_calls: int

# ====================================================
# FLIGHT AGENT
# ====================================================

def flight_agent(state: TravelState):

    logger.info(
        f"Flight Agent Started | Query: {state['user_query']}"
    )

    query = state["user_query"]

    flight_data = search_flights(
        query
    )

    logger.info(
        "Flight Agent Completed"
    )

    return {

        "flight_results":
            flight_data,

        "messages": [

            AIMessage(
                content="Flight results fetched"
            )
        ],

        "llm_calls":
            state.get("llm_calls", 0) + 1
    }

# ====================================================
# HOTEL AGENT
# ====================================================

def hotel_agent(state: TravelState):

    query = f"""
Best hotels for
{state['user_query']}
"""

    logger.info(
        f"Hotel Agent Started | Query: {query}"
    )

    hotel_results = tavily_search(
        query
    )

    logger.info(
        "Hotel Agent Completed"
    )

    return {

        "hotel_results":
            hotel_results,

        "messages": [

            AIMessage(
                content="Hotel information fetched"
            )
        ],

        "llm_calls":
            state.get("llm_calls", 0) + 1
    }

# ====================================================
# ITINERARY AGENT
# ====================================================

def itinerary_agent(state: TravelState):

    logger.info(
        "Itinerary Agent Started"
    )

    prompt = f"""
Create a travel itinerary.

User Query:
{state['user_query']}

Flight Results:
{state['flight_results']}

Hotel Results:
{state['hotel_results']}
"""

    response = llm.invoke([

        SystemMessage(
            content="You are an expert travel planner"
        ),

        HumanMessage(
            content=prompt
        )
    ])

    logger.info(
        "Itinerary Generated Successfully"
    )

    return {

        "itinerary":
            response.content,

        "messages":
            [response],

        "llm_calls":
            state.get("llm_calls", 0) + 1
    }

# ====================================================
# FINAL AGENT
# ====================================================

def final_agent(state: TravelState):

    logger.info(
        "Final Agent Started"
    )

    final_prompt = f"""
Generate final travel response.

Flights:
{state['flight_results']}

Hotels:
{state['hotel_results']}

Itinerary:
{state['itinerary']}
"""

    response = llm.invoke([

        HumanMessage(
            content=final_prompt
        )
    ])

    logger.info(
        "Final Response Generated"
    )

    return {

        "messages":
            [response],

        "llm_calls":
            state.get("llm_calls", 0) + 1
    }

# ====================================================
# GRAPH
# ====================================================

graph = StateGraph(
    TravelState
)

graph.add_node(
    "flight_agent",
    flight_agent
)

graph.add_node(
    "hotel_agent",
    hotel_agent
)

graph.add_node(
    "itinerary_agent",
    itinerary_agent
)

graph.add_node(
    "final_agent",
    final_agent
)

graph.add_edge(
    START,
    "flight_agent"
)

graph.add_edge(
    "flight_agent",
    "hotel_agent"
)

graph.add_edge(
    "hotel_agent",
    "itinerary_agent"
)

graph.add_edge(
    "itinerary_agent",
    "final_agent"
)

graph.add_edge(
    "final_agent",
    END
)

# ====================================================
# POSTGRES CHECKPOINT
# ====================================================

_conn = psycopg.connect(

    DATABASE_URL,

    autocommit=True
)

checkpointer = PostgresSaver(
    _conn
)

checkpointer.setup()

# ====================================================
# COMPILE APP
# ====================================================

app = graph.compile(
    checkpointer=checkpointer
)

# ====================================================
# TERMINAL TEST
# ====================================================

if __name__ == "__main__":

    config = {

        "configurable": {

            "thread_id":
                "user_dhruvi"
        }
    }

    user_input = input(
        "Enter travel request: "
    )

    result = app.invoke(

        {

            "messages": [

                HumanMessage(
                    content=user_input
                )
            ],

            "user_query":
                user_input,

            "flight_results":
                "",

            "hotel_results":
                "",

            "itinerary":
                "",

            "llm_calls":
                0
        },

        config=config
    )

    print("\nFINAL RESPONSE:\n")

    for msg in result["messages"]:

        print(
            msg.content
        )