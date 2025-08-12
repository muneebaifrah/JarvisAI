from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
import datetime
import random
import webbrowser  # won't actually open in server environment, but we can log instead

# Environment variable for API key
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()
chatStr = ""

# Request schema
class Command(BaseModel):
    query: str

# Helper: AI speak (just return text instead of pyttsx3)
def say(text):
    print(f"Jarvis says: {text}")
    return text

# Chat function
def chat(query):
    global chatStr
    chatStr += f"Ifrah: {query}\nJarvis: "
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=chatStr,
            temperature=0.7,
            max_tokens=256
        )
        output = response["choices"][0]["text"].strip()
        chatStr += f"{output}\n"
        return say(output)
    except Exception as e:
        print("OpenAI Error:", e)
        return say("Sorry, I couldn't process that.")

# AI save-to-file function
def ai(prompt):
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=256
        )
        text = response["choices"][0]["text"].strip()
        filename = f"response-{random.randint(1, 99999)}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Prompt:\n{prompt}\n\nResponse:\n{text}")
        return say("AI response saved successfully.")
    except Exception as e:
        print("AI Save Error:", e)
        return say("Error saving AI response.")

# API endpoint
@app.post("/jarvis")
def jarvis_command(cmd: Command):
    query = cmd.query.lower()
    
    if "open youtube" in query:
        return {"response": say("Opening YouTube...")}
    elif "open wikipedia" in query:
        return {"response": say("Opening Wikipedia...")}
    elif "open google" in query:
        return {"response": say("Opening Google...")}
    elif "open music" in query:
        return {"response": say("Playing music online...")}
    elif "the time" in query:
        now = datetime.datetime.now()
        time_str = now.strftime("%H:%M")
        return {"response": say(f"The time is {time_str}.")}
    elif "using ai" in query or "using artificial intelligence" in query:
        return {"response": ai(prompt=query)}
    elif "reset" in query:
        global chatStr
        chatStr = ""
        return {"response": say("Chat reset successfully.")}
    elif "exit" in query or "stop" in query:
        return {"response": say("Goodbye!")}
    elif query.strip() != "":
        return {"response": chat(query)}
    else:
        return {"response": "No command detected."}

