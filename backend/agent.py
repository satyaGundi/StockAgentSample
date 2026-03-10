import os
import yfinance as yf
from dotenv import load_dotenv
from typing import Annotated, TypedDict, Any
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

# 1. Configuration & Setup
load_dotenv()

# Access the variable (works in local and Azure)
google_api_key = os.getenv("GOOGLE_API_KEY")
langsmith_tracing = os.getenv("LANGSMITH_TRACING")
langsmith_endpoint = os.getenv("LANGSMITH_ENDPOINT")
langsmith_api_key = os.getenv("LANGSMITH_API_KEY")
langsmith_project = os.getenv("LANGSMITH_PROJECT")


if google_api_key is None:
    print("Warning: GOOGLE_API_KEY not found!")
if langsmith_tracing is None:
    print("Warning: LANGSMITH_TRACING not found!")
if langsmith_endpoint is None:
    print("Warning: LANGSMITH_ENDPOINT not found!")
if langsmith_api_key is None:
    print("Warning: LANGSMITH_API_KEY not found!")
if langsmith_project is None:
    print("Warning: LANGSMITH_PROJECT not found!")


class StockAgentState(TypedDict):
    messages: Annotated[list, add_messages]

# 2. Tools
@tool
def get_current_stock_price(symbol: str) -> float:
    """Returns the current stock price for a given ticker symbol (e.g., 'AAPL')."""
    stock = yf.Ticker(symbol)
    return stock.info.get('currentPrice', 'N/A')

@tool
def get_stock_info_time_period(symbol: str, period: str) -> str:
    """Returns historical stock data. Valid periods: 1d, 5d, 1mo, 3mo, 6mo, 1y, ytd, max."""
    stock = yf.Ticker(symbol)
    hist = stock.history(period=period)
    if hist.empty:
        return f"No historical data available for {symbol} with period {period}."
    return f"Historical data for {symbol} over the last {period}:\n{hist.tail()}"

# 3. Graph Construction
def create_stock_graph():
    # llm = init_chat_model("google_genai:gemini-2.0-flash") # Updated to stable version string
    llm = init_chat_model("google_genai:gemini-2.5-flash")

    tools = [get_current_stock_price, get_stock_info_time_period]
    llm_with_tools = llm.bind_tools(tools)

    def chatbot_node(state: StockAgentState):
        return {"messages": [llm_with_tools.invoke(state["messages"])]}

    workflow = StateGraph(StockAgentState)
    workflow.add_node("agent", chatbot_node)
    workflow.add_node("tools", ToolNode(tools))

    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", tools_condition)
    workflow.add_edge("tools", "agent")
    
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)

# Initialize the graph once when the module loads
graph = create_stock_graph()

# 4. Helper Utilities
def extract_text_content(content: Any) -> str:
    if isinstance(content, str): return content
    if isinstance(content, list):
        return "\n".join([b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text"])
    return str(content)

# 5. The Public API Function
def analyze_stock(user_input: str, thread_id: str = "default_thread") -> str:
    """
    The main entry point for the FastAPI backend.
    """
    config = {"configurable": {"thread_id": thread_id}}
    
    # Invoke the graph with the new message
    input_state = {"messages": [{"role": "user", "content": user_input}]}
    output_state = graph.invoke(input_state, config=config)
    
    # Extract the last message content
    last_message = output_state["messages"][-1]
    
    if hasattr(last_message, 'content'):
        return extract_text_content(last_message.content)
    return str(last_message)
