from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI

from src.config import get_db_connection_url


class ActivityBot:
    llm_dict = {}

    @staticmethod
    def get_instance(apikey: str, model_name: str = "gpt-4o-mini", temperature: float = 0.5) -> BaseChatModel:
        if model_name not in ActivityBot.llm_dict:
            ActivityBot.llm_dict[model_name] = ChatOpenAI(
                model=model_name,
                openai_api_key=apikey,
                temperature=temperature
            )
            return ActivityBot.llm_dict[model_name]
        else:
            return ActivityBot.llm_dict[model_name]

    @staticmethod
    def get_chat_history(user_id: str):
        return SQLChatMessageHistory(
            session_id=user_id, connection_string=get_db_connection_url()
        )
