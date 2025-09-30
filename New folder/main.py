from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import asyncio
from datetime import datetime
import os

from app.agents.orchestrator import OrchestratorAgent
from app.models.test_case import TestReport

# Create FastAPI app
app = FastAPI(title="Multi-Agent Game Tester", version="2.0.0")

# Mount frontend and artifacts
app.mount("/static", StaticFiles(directory="frontend"), name="static")
app.mount("/artifacts", StaticFiles(directory="artifacts"), name="artifacts")

# Global orchestrator
orchestrator = OrchestratorAgent()

class TestRequest(BaseModel):
    target_url: str = "https://play.ezygamers.com"
    test_count: int = 10  # Reduced default for faster testing
    execute_top_n: int = 5

class TestResponse(BaseModel):
    task_id: str
    status: str
    message: str

# Store reports (in production, use database)
reports_storage: dict = {}

@app.get("/")
async def root():
    return {
        "message": "🎮 Multi-Agent Game Tester v2.0", 
        "status": "running",
        "features": [
            "Real browser automation with Playwright",
            "SumLink game-specific test cases", 
            "Multi-language testing support",
            "Comprehensive artifact capture",
            "Enhanced reporting with performance metrics"
        ]
    }

@app.get("/artifacts/{task_id}/screenshots")
async def list_screenshots(task_id: str):
    """List all screenshots for a task"""
    screenshots_dir = f"artifacts/screenshots"
    if not os.path.exists(screenshots_dir):
        return {"screenshots": []}
    
    screenshots = []
    for filename in os.listdir(screenshots_dir):
        if task_id in filename and filename.endswith('.png'):
            screenshots.append({
                "filename": filename,
                "url": f"/artifacts/screenshots/{filename}"
            })
    
    return {"screenshots": screenshots}

# ... rest of your existing endpoints ...
