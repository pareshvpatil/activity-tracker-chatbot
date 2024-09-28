from enum import Enum

from langserve import CustomUserType


class PromptType(Enum):
    ACTIVITY_TRACKER = "activity_tracker"
    ACTIVITY_REPORTER = "activity_reporter"


class ActivityInput(CustomUserType):
    text: str

class ReportInput(CustomUserType):
    text: str
