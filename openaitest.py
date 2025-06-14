import openai
from config import apikey

openai.api_key = apikey

try:
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Write an email to my boss for resignation?",
        temperature=0.7,
        max_tokens=256,
        top_p=1
    )
    print(response["choices"][0]["text"].strip())
except Exception as e:
    print("API request failed:", e)
