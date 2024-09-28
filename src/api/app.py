import uvicorn
from fastapi import FastAPI

from src.bots.activity_reporter import get_activity_reporter
from src.bots.activity_tracker import get_activity_tracker
from src.types import ActivityInput, ReportInput

app = FastAPI(
    title="Activity Assistant",
    version="1.0",
    description="Your personal activity assistant"
)

@app.post("/track-activity/{user_id}")
async def track_activity(user_id: str, body: ActivityInput):
    return get_activity_tracker(user_id).invoke({
        "activity": body.text
    })

@app.post("/activity-report/{user_id}")
async def track_activity(user_id: str, body: ReportInput):
    return get_activity_reporter(user_id).invoke({
        "question": body.text
    })

uvicorn.run(app, host="localhost", port=8000)
