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
        You take the new message as the newest entry mentioned under the heading 'User activity', extract information from it.
        Return the response in the form of JSON with keys: 'activity', 'mood', 'duration_in_hours', 'activity_timestamp'.
        Please round off the duration to the closest half-hourly time period and convert it into 'duration_in_hours'.
        Calculate activity timestamp based on current_time and message content. current_time is: {current_time}.
        Do not use information outside of the messages and history known to you from the context, and the current prompt.
        
        If the user mentions multiple different activities in a single message, consider them as different activities.
        
        Even if you identify a single activity from the message, wrap it in a JSON object with 'activities' as the field which holds activities as an array.
        
        User activity:
        {activity}
        """
    )


def _get_activity_reporter_prompt():
    return PromptTemplate(
        input_variables=["question"],
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


prompt_factory = {
    PromptType.ACTIVITY_TRACKER: _get_activity_tracker_prompt,
    PromptType.ACTIVITY_REPORTER: _get_activity_reporter_prompt
}
