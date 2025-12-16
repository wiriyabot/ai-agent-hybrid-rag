from typing import TypedDict
from langchain_community.agent_toolkits import create_sql_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END
from src.database import llm, db, retriever

class AgentState(TypedDict):
    question: str
    route: str
    sql_result: str
    vector_result: str
    final_answer: str


def router_node(state: AgentState):
    question = state["question"]
    system_prompt = """You are a router. Your ONLY job is to output one of these three words: 'sql', 'vector', or 'both'.
    RULES: Just output the word. No explanation."""
    
    route = (ChatPromptTemplate.from_template(system_prompt) | llm | StrOutputParser()).invoke({"question": question})
    if route not in ["sql", "vector", "both"]:
        route = "vector"
        
    return {"route": route, } 


def sql_node(state: AgentState):
    suffix = """
    I have a table called 'sales_transactions'.
    IMPORTANT: 'total sales' = sum(total_amount). 'date' is YYYY-MM-DD.
    """
    agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=False, suffix=suffix)
    result = agent_executor.invoke({"input": state["question"]})
    output = result['output']
        
    return {"sql_result": output} 


def vector_node(state: AgentState):
    docs = retriever.invoke(state["question"])
    context = "\n".join([f"- {d.page_content}" for d in docs])
    return {"vector_result": context}


def synthesizer_node(state: AgentState):
    prompt = f"""
    User Question: {state['question']}
    SQL Data: {state.get('sql_result', 'N/A')}
    Vector Data: {state.get('vector_result', 'N/A')}
    Please answer based on data above in THAI language nicely.
    """
    response = llm.invoke(prompt)
    return {"final_answer": response.content} 


def build_graph():
    workflow = StateGraph(AgentState)
    workflow.add_node("router", router_node)
    workflow.add_node("sql_agent", sql_node)
    workflow.add_node("vector_agent", vector_node)
    workflow.add_node("synthesizer", synthesizer_node)
    workflow.set_entry_point("router")

    workflow.add_conditional_edges(
        "router", 
        lambda state: state["route"], 
        {"sql": "sql_agent", "vector": "vector_agent", "both": "sql_agent"}
    )

    def post_sql_logic(state):
        return "vector_agent" if state["route"] == "both" else "synthesizer"

    workflow.add_conditional_edges("sql_agent", post_sql_logic, {"vector_agent": "vector_agent", "synthesizer": "synthesizer"})
    workflow.add_edge("vector_agent", "synthesizer")
    workflow.add_edge("synthesizer", END)

    return workflow.compile()


agent_app = build_graph()