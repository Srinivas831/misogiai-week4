import json
import uuid
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from typing import List

# ✅ 1. Define the input schema using Pydantic
class CreateMeetingInput(BaseModel):
    title: str = Field(..., description="Title of the meeting")
    participants: List[str] = Field(..., description="List of participant names")
    duration: int = Field(..., description="Duration of the meeting in minutes")
    start_time: str = Field(..., description="Start time in ISO format (e.g., '2025-07-07T14:00:00')")


# ✅ 2. Actual tool logic
def create_meeting(title: str, participants: List[str], duration: int, start_time: str) -> str:
    with open('data/meetings.json', 'r') as f:
        meetings = json.load(f)

    meeting_id = f"m{str(uuid.uuid4())[:6]}"
    start = datetime.fromisoformat(start_time)
    end = start + timedelta(minutes=duration)

    new_meeting = {
        "id": meeting_id,
        "title": title,
        "participants": participants,
        "start": start.isoformat(),
        "end": end.isoformat()
    }

    meetings.append(new_meeting)

    with open('data/meetings.json', 'w') as f:
        json.dump(meetings, f, indent=2)

    return f"✅ Meeting '{title}' scheduled from {start.isoformat()} to {end.isoformat()} with participants {participants}"


# ✅ 3. Package this as an MCP-compatible tool
create_meeting_tool = {
    "name": "create_meeting",
    "description": "Schedules a new meeting by saving it to the meetings database",
    "input_schema": CreateMeetingInput,
    "func": create_meeting
}