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

### Instructions
- Set up a virtual environment on the repository
- Install the required dependencies using the [`requirements.txt`](./requirements.txt) file provided in the repo
- Create a python run configuration in your IDE
  - Required environment variables:
  1. openai__apikey: This is your Open AI API Key
  2. ai_model: This is the AI model you want to use. Default is: `gpt-4o-mini`
- Use src/app.py as the entrypoint file
  - This file creates a FastAPI server on your local @ `http://localhost:8000`


## Limitations

This code only instantiates an OpenAI Chatbot model instance from Langchain. Further developments will bring in support for other AI platforms.
