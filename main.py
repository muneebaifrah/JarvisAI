import speech_recognition as sr
import os
import webbrowser
import openai
import datetime
import random
import pyttsx3
from config import apikey

# Setup for text-to-speech
engine = pyttsx3.init()
engine.setProperty('rate', 150)

chatStr = ""

def say(text):
    print(f"\nJarvis says: {text}")
    engine.say(text)
    engine.runAndWait()

def chat(query):
    global chatStr
    openai.api_key = apikey
    chatStr += f"Ifrah: {query}\nJarvis: "
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=chatStr,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        output = response["choices"][0]["text"].strip()
        say(output)
        chatStr += f"{output}\n"
        return output
    except Exception as e:
        say("Sorry, I couldn't process that.")
        print("OpenAI Error:", e)
        return ""

def ai(prompt):
    openai.api_key = apikey
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=256
        )
        text = response["choices"][0]["text"].strip()
        if not os.path.exists("Openai"):
            os.mkdir("Openai")
        filename = f"Openai/response-{random.randint(1, 99999)}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Prompt:\n{prompt}\n\nResponse:\n{text}")
        say("AI response saved successfully.")
    except Exception as e:
        say("Error saving AI response.")
        print("AI Save Error:", e)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        r.energy_threshold = 300
        say("Listening...")
        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=15)
            say("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"You said: {query}")
            return query
        except sr.WaitTimeoutError:
            say("Listening timed out.")
            return ""
        except sr.UnknownValueError:
            say("Sorry, I didn't catch that.")
            return ""
        except Exception as e:
            say("Microphone error.")
            print("Microphone Error:", e)
            return ""

if __name__ == '__main__':
    say("Jarvis A.I is now online.")
    print("Welcome to Jarvis A.I")

    while True:
        query = takeCommand().lower()

        if "open youtube" in query:
            say("Opening YouTube...")
            webbrowser.open("https://www.youtube.com")

        elif "open wikipedia" in query:
            say("Opening Wikipedia...")
            webbrowser.open("https://www.wikipedia.org")

        elif "open google" in query:
            say("Opening Google...")
            webbrowser.open("https://www.google.com")

        elif "open music" in query:
            say("Playing music online...")
            webbrowser.open("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")

        elif "the time" in query:
            now = datetime.datetime.now()
            time_str = now.strftime("%H bajke %M minutes")
            say(f"The time is {time_str}.")

        elif "using ai" in query or "using artificial intelligence" in query:
            ai(prompt=query)

        elif "end program" in query or "exit" in query or "stop" in query:
            say("Goodbye sir!")
            break

        elif "reset" in query:
            chatStr = ""
            say("Chat reset successfully.")

        elif query.strip() != "":
            chat(query)
