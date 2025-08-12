import openai
import os
import datetime
import random

openai.api_key = os.getenv("OPENAI_API_KEY")
chatStr = ""

def say(text):
    print(f"Jarvis says: {text}")
    return text

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

def process_command(query):
    query = query.lower()

    if "open youtube" in query:
        return say("Opening YouTube... (functionality not implemented in script)")
    elif "open wikipedia" in query:
        return say("Opening Wikipedia... (functionality not implemented in script)")
    elif "open google" in query:
        return say("Opening Google... (functionality not implemented in script)")
    elif "open music" in query:
        return say("Playing music online... (functionality not implemented in script)")
    elif "the time" in query:
        now = datetime.datetime.now()
        time_str = now.strftime("%H:%M")
        return say(f"The time is {time_str}.")
    elif "using ai" in query or "using artificial intelligence" in query:
        return ai(prompt=query)
    elif "reset" in query:
        global chatStr
        chatStr = ""
        return say("Chat reset successfully.")
    elif "exit" in query or "stop" in query:
        say("Goodbye!")
        exit(0)
    elif query.strip() != "":
        return chat(query)
    else:
        return say("No command detected.")

if __name__ == "__main__":
    print("Jarvis AI started. Type your commands (type 'exit' to quit).")
    while True:
        user_input = input("You: ")
        process_command(user_input)
