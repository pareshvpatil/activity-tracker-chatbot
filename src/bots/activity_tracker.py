from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

from src.config.config import getconfig
from src.types import PromptType
from src.parsers.output_parsers import get_output_parser
from src.prompts.templates import get_prompt_template


def get_activity_tracker(user_id: str):
    prompt_template = get_prompt_template(PromptType.ACTIVITY_TRACKER)
    llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=getconfig("openai:apikey"), temperature=1)

    chain_with_history = RunnableWithMessageHistory(
        (prompt_template | llm),
        lambda: SQLChatMessageHistory(
            session_id=user_id, connection_string="sqlite:///chat_history.db"
        ),
        input_messages_key="activity",
        history_messages_key="history"
    )

    return chain_with_history | get_output_parser(PromptType.ACTIVITY_TRACKER)
