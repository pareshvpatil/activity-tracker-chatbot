# Activity Tracker Chatbot with Open AI

Simple AI-backed activity tracker.

Use the API interface to send your activities to it.
The model will understand your activities, detect moods, and provide you with a structured summary.

## Tech stack

- Langchain
  - langchain-core
  - langchain-community
  - langchain-openai
- Pconf
- FastAPI
- Sqlite


## Run locally

This code does not need any additional infrastructure on your machine except for the API Keys.

### Setup Instructions
- Set up a virtual environment on the repository
- Install the required dependencies using the [`requirements.txt`](./requirements.txt) file provided in the repo
- Create a python run configuration in your IDE


- Use src/app.py as the python file
  - This file creates a FastAPI server on your local @ `http://localhost:8000`


- There are three POST APIs exposed by the bot service
  - `http://localhost:8000/track-activity/{user_id}`
  - `http://localhost:8000/activity-report/{user_id}`
  - `http://localhost:8000/clear-history/{user_id}`


- Use the `/clear-history` API to clear the chat history and begin again.
 

- Required environment variables:
  1. `OPENAI__APIKEY`: This is your Open AI API Key
  2. `AI_MODEL`: This is the AI model you want to use. It's optional, the default is: `gpt-4o-mini`


- For linux and MacOS users, execute the [`startup.sh`](./startup.sh) shell file to install the requirements, set the variables and run the service locally.
- For Windows users, copy the contents from the [`startup.bat`](./startup.bat) file line by line, and paste it into your CMD to run the app.
  - **IMPORTANT**: Do not forget to change the OpenAI api key before starting the application.
- Import the [postman collection](./chatbot_apis.postman_collection) available in the repository to call the service using Postman. The collection includes example requests for easier testing.


## Limitations

This code only instantiates an OpenAI Chatbot model instance from Langchain. Further developments will bring in support for other AI platforms.
