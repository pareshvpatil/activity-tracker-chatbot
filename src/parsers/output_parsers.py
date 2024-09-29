from typing import List

from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


class Activity(BaseModel):
    activity: str = Field("the activity done by the user")
    mood: str = Field("the mood extracted from the activity or the message")
    duration_in_hours: float = Field(
        "duration of the activity if provided or identifiable, else 0. Duration is rounded off to closes two digits in hours as a float number.")
    activity_timestamp: str = Field("time when the activity was performed")


class Activities(BaseModel):
    activities: List[Activity] = Field(
        "The wrapper array of activity summary object with fields 'activity', 'mood', 'duration_in_hours', 'activity_timestamp'")

    total_time: float = Field(description="The total time done in the activity in summary", default=None)


def get_output_parser():
    return PydanticOutputParser(pydantic_object=Activities)
