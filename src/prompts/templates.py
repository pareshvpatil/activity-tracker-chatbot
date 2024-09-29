from langchain_core.prompts import PromptTemplate

from src.types import PromptType


def get_prompt_template(prompt_type: PromptType) -> PromptTemplate:
    return prompt_factory[prompt_type]()


def _get_activity_tracker_prompt():
    return PromptTemplate(
        input_variables=["activity", "history"],
        template="""
        You are an assistant that helps the user track their activities, 
        identify moods from their message, and provides them with a structured response.
        You additionally only look at the information from the previous activities provided to you from the conversation history.
        You take the new message under the heading 'User activity', extract information from it.
        Return the response in the form of JSON with keys: 'activity', 'mood', 'duration_in_hours', 'activity_timestamp'.
        Please round off the duration to the closest half-hourly time period and convert it into 'duration_in_hours'.
        Calculate activity timestamp based on current_time and message content. current_time is: {current_time}.
        Do not use any information outside of the messages, history known to you from the context, and the current prompt.
        
        If the user mentions multiple different activities in a single message, consider them as separate activities.
        
        Even if you identify a single activity from the message, wrap it in a JSON object with 'activities' as the field which holds activities as an array.
        
        User activity:
        {activity}
        """
    )


def _get_activity_reporter_prompt():
    return PromptTemplate(
        input_variables=["question", "current_time"],
        template="""
        You are an assistant that helps the user track their activities, 
        identify moods from their message, and provides them with a structured response.
        You are building an activity report filtered by the 'activity_timestamp' by considering the chat history you have.
        Provide the response with the following fields in a JSON format:
        'activity', 'mood', 'duration_in_hours', 'activity_timestamp'.
        Wrap the activity json object under a single key: 'activities' as an array and include the total time spent in activities in the field: 'total_time'.
        
        Also, do not consider the summary request messages from the conversation history, only consider the activity messages.
        
        Only consider the activities whose 'activity_timestamp' lies within the time period asked in the activity report question.
        To come up with the time period to filter the activities, consider the current_time provided, and build the relative time period from the question.
        
        The current_time is: {current_time}.
        
        The question is:
        {question}
        """
    )


prompt_factory = {
    PromptType.ACTIVITY_TRACKER: _get_activity_tracker_prompt,
    PromptType.ACTIVITY_REPORTER: _get_activity_reporter_prompt
}
