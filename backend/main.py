import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Import the refactored function from your agent.py
from backend.agent import analyze_stock 

app = FastAPI(title="AI Stock Analysis API")

# 1. Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. API Endpoint for the Chatbot
@app.post("/analyze")
async def run_analysis(ticker: str):
    """
    Receives a ticker from the UI and returns the agent's analysis.
    """
    try:
        # Calls the refactored analyze_stock function in agent.py
        result = analyze_stock(ticker)
        return {"ticker": ticker.upper(), "analysis": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent Error: {str(e)}")

# 3. Serve Frontend Files
# Path setup to find the 'frontend' folder relative to this file
base_path = os.path.dirname(os.path.dirname(__file__))
frontend_path = os.path.join(base_path, "frontend")

# Mount the frontend directory to serve CSS/JS files
if os.path.exists(frontend_path):
    app.mount("/frontend", StaticFiles(directory=frontend_path), name="frontend")

# 4. Root Route: Serve index.html
@app.get("/")
async def read_index():
    """
    Serves the main chat UI at the root URL.
    """
    index_file = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"error": "Frontend index.html not found at /frontend/index.html"}
