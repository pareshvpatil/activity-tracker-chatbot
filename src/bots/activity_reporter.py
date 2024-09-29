from langchain_core.runnables import RunnableWithMessageHistory

from src.bots.llm_factory import ActivityBot
from src.config import getconfig
from src.parsers.output_parsers import get_output_parser
from src.prompts.templates import get_prompt_template
from src.types import PromptType


def get_activity_reporter(user_id: str):
    prompt_template = get_prompt_template(PromptType.ACTIVITY_REPORTER)

    chain_with_history = RunnableWithMessageHistory(
        (prompt_template | ActivityBot.get_instance(apikey=getconfig("openai:apikey"), model_name=getconfig("ai_model"))),
        get_session_history=lambda: ActivityBot.get_chat_history(user_id),
        input_messages_key="question"
    )

    return chain_with_history | get_output_parser()
