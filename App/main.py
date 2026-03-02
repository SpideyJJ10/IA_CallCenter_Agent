from fastapi import FastAPI, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from App.agent import CallCenterAgent
from typing import List, Dict

app = FastAPI(title="Connecta Solutions API")
agent = CallCenterAgent()

@app.post("/chat")
async def chat(
    message: str = Body(..., embed=True),
    history: List[Dict] = Body([], embed=True)
):
    """
    Principal endpoint for chat interactions.
    """
    result = await agent.generate_response(message, history=history)
    return {
        "response": result.content,
        "latency_seconds": result.latency,
        "transfer": result.transfer if result.transfer else False
    }

# Serve static files (CSS, JS, Images)
app.mount("/static", StaticFiles(directory="App/static"), name="static")

@app.get("/")
async def read_index():
    """
    Serves the main frontend application.
    """
    return FileResponse("App/templates/index.html")