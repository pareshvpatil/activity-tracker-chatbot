from datetime import datetime

import uvicorn
from fastapi import FastAPI

from src.bots.activity_reporter import get_activity_reporter
from src.bots.activity_tracker import get_activity_tracker
from src.bots.llm_factory import ActivityBot
from src.types import ActivityInput, ReportInput

app = FastAPI(
    title="Activity Assistant",
    version="1.0",
    description="Your personal activity assistant"
)


@app.post("/track-activity/{user_id}")
async def track_activity(user_id: str, body: ActivityInput):
    return get_activity_tracker(user_id).invoke({
        "activity": body.text,
        "current_time": datetime.now().isoformat()
    })


@app.post("/activity-report/{user_id}")
async def track_activity(user_id: str, body: ReportInput):
    return get_activity_reporter(user_id).invoke({
        "question": body.text,
        "current_time": datetime.now().isoformat()
    })


@app.delete("/clear-history/{user_id}")
async def clear_history(user_id: str):
    chat_history = ActivityBot.get_chat_history(user_id)
    chat_history.clear()

    return {
        "message": f"user history cleared for: {user_id}"
    }


uvicorn.run(app, host="localhost", port=8000)
