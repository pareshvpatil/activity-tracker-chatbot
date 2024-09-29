from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI


class ActivityBot:
    llm_dict = {}

    @staticmethod
    def get_instance(apikey: str, model_name: str = "gpt-4o-mini", temperature: float = 0.5) -> BaseChatModel:
        if model_name not in ActivityBot.llm_dict:
            ActivityBot.llm_dict[model_name] = ChatOpenAI(model=model_name, openai_api_key=apikey,
                                                          temperature=temperature)
            return ActivityBot.llm_dict[model_name]
        else:
            return ActivityBot.llm_dict[model_name]
