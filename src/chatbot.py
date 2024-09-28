from datetime import datetime

from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

from src.config.config import getconfig

activity_prompt_template = PromptTemplate(
    input_variables=["activity", "history", "current_time"],
    template="""
     You are an assistant that helps the user track their activities, 
     identify moods from their message, and provides them with a structured response.
     You additionally only look at the information from the previous activities provided to you from the conversation history.
     You take the new message as the newest entry mentioned under the heading 'User activity', extract information from it.
     Return the response in the form of JSON with keys: 'activity', 'mood', 'duration_in_hours', 'activity_timestamp'.
     Please round off the duration to the closest half-hourly time period and convert it into 'duration_in_hours'.
     Calculate activity timestamp based on current_time and message content. current_time is: {current_time}.
     Do not use information outside of the messages and history known to you from the context, and the current prompt.

     If the user mentions multiple different activities in a single message, consider them as different activities.
 
     Even if you identify a single activity from the message, 
     wrap it in a JSON object with 'activities' as the field which holds activities as an array.

     User activity:
     {activity}
     """
)

activity_analysis_prompt_template = PromptTemplate(
    input_variables=["question", "current_time"],
    template="""
    You are an assistant that helps the user track their activities, 
    identify moods from their message, and provides them with a structured response.
    Please consider only the conversation history available to you from the context, 
    and provide activity summary as the response in a JSON structure with attributes:
    'activity', 'mood', 'duration_in_hours'.
    Wrap an activity json object under a single key: 'activities' as an array 
    and do include the total time spent in activities as well in the field: 'total_time'.
    
    Summarise activities and moods separately in the response.
    
    Calculate the summary based on current_time and question content. current_time is: {current_time}.
    
    {question}
    """
)

response_schemas = [
    ResponseSchema(name="activities", description="The wrapper array of activity summary object with fields 'activity', 'mood', 'duration_in_hours', 'activity_timestamp'")
]

output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=getconfig("openai:apikey"), temperature=1)
llm_chain = activity_prompt_template | llm

analysis_chain = activity_analysis_prompt_template | llm

def load_history(user_id: str):
    chat_message_history = SQLChatMessageHistory(
        session_id=user_id, connection_string="sqlite:///chat_history.db"
    )
    return chat_message_history.messages

def print_history(user_id: str):
    chat_message_history = SQLChatMessageHistory(
        session_id=user_id, connection_string="sqlite:///chat_history.db"
    )
    print(f"=========== history for user: {user_id} is: {len(chat_message_history.get_messages())}\n\n\n")

def log_activity(activity: str, user_id: str) -> dict:
    chain_with_history = RunnableWithMessageHistory(
        llm_chain,
        lambda: SQLChatMessageHistory(
            session_id=user_id, connection_string="sqlite:///chat_history.db"
        ),
        input_messages_key="activity",
        history_messages_key="history"
    )

    response = (chain_with_history | output_parser).invoke({
        "activity": activity,
        "current_time": datetime.now().isoformat()
    })

    return response

def get_activity_summary(question: str, user_id: str):
    history = SQLChatMessageHistory(
        session_id=user_id, connection_string="sqlite:///chat_history.db"
    )

    chain_with_history = RunnableWithMessageHistory(
        analysis_chain,
        get_session_history=lambda: history,
        input_messages_key="question"
    )

    parser = StructuredOutputParser.from_response_schemas([
        ResponseSchema(name="activities", description="The wrapper array of activity summary object with fields 'activity', 'mood', 'duration_in_hours'"),
        ResponseSchema(name="total_time", description="The total time spent in hours, (optional)")
    ])

    response = (chain_with_history | parser).invoke({
        "question": question,
        "current_time": datetime.now().isoformat()
    })

    return response
#
# print(
#     "response from the model: ",
#     log_activity("Today I did surya namaskar and other exercises from 7 to 9 in the morning", "user 1")
# )
#
# print(
#     "response from the model: ",
#     log_activity("I went for a 30 minute run and then did 20 minutes of yoga.", "user 1")
# )

# print(
#     "response from the model: ",
#     log_activity("Yesterday, I felt happy and excited in the morning", "user 1")
# )

print(
    "response from the analysis: ",
    get_activity_summary("What all did I do in the last 10 minutes?", "user 1")
)
