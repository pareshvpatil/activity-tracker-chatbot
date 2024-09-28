from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain_core.output_parsers import BaseOutputParser

from src.types import PromptType


def get_output_parser(prompt_type: PromptType) -> BaseOutputParser:
    return parser_factory[prompt_type]()


def _get_activity_tracker_output_parser():
    response_schemas = [
        ResponseSchema(name="activities", description="The wrapper array of activity summary object with fields 'activity', 'mood', 'duration_in_hours', 'activity_timestamp'")
    ]
    return StructuredOutputParser.from_response_schemas(response_schemas)


def _get_activity_reporter_output_parser():
    response_schemas = [
        ResponseSchema(name="activities", description="The wrapper array of activity summary object with fields 'activity', 'mood', 'duration_in_hours'"),
        ResponseSchema(name="total_time", description="The total time spent in activities, (optional)")
    ]
    return StructuredOutputParser.from_response_schemas(response_schemas)


parser_factory = {
    PromptType.ACTIVITY_TRACKER: _get_activity_tracker_output_parser,
    PromptType.ACTIVITY_REPORTER: _get_activity_reporter_output_parser
}
