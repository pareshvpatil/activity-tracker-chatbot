pip install -r requirements.txt

EXPORT openai__apikey=$1
EXPORT ai_model="$1:-gpt-4o-mini"

python3 src/app.py
