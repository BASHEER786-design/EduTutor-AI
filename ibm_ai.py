import os
from dotenv import load_dotenv
from openai import OpenAI

# Load .env file
load_dotenv()

# Read API key from environment
api_key = os.getenv("GROQ_API_KEY")

# Check for API key
if not api_key:
    raise ValueError("GROQ_API_KEY is missing in your .env file")

# ✅ Create OpenAI client with correct Groq base_url
client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

# Function to get response from Groq's Mixtral model
def get_ai_response(user_input):
    response = client.chat.completions.create(
        model="llama3-70b-8192",  # ✅ Replace this line
        messages=[
            {"role": "system", "content": "You are a helpful AI tutor for students."},
            {"role": "user", "content": user_input}
        ],
        temperature=0.7,
        max_tokens=1500
    )
    return response.choices[0].message.content.strip()

