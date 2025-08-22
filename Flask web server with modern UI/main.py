#!/usr/bin/env python3
"""
JarvisAI - A Free Local AI Assistant (Standalone Version)
No paid APIs required - uses local processing and free services
"""

import os
import json
import datetime
import webbrowser
import subprocess
import platform
import requests
import random
import time
import ast
import operator
import math
from pathlib import Path

# Try to import optional dependencies with graceful fallbacks
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    print("⚠️  Speech Recognition not available. Install with: pip install SpeechRecognition")

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("⚠️  Text-to-Speech not available. Install with: pip install pyttsx3")

try:
    import wikipedia
    WIKIPEDIA_AVAILABLE = True
except ImportError:
    WIKIPEDIA_AVAILABLE = False
    print("⚠️  Wikipedia not available. Install with: pip install wikipedia")

class JarvisAI:
    def __init__(self):
        self.name = "Jarvis"
        self.conversation_history = []
        self.data_dir = Path("jarvis_data")
        self.data_dir.mkdir(exist_ok=True)
        self.voice_enabled = False
        self.setup_voice()
        
        # Knowledge base for responses
        self.responses = {
            "greeting": [
                "Hello! I'm Jarvis, your AI assistant. How can I help you today?",
                "Hi there! Ready to assist you with anything you need.",
                "Greetings! What can I do for you today?",
            ],
            "farewell": [
                "Goodbye! Have a great day!",
                "See you later! Take care!",
                "Until next time! Stay awesome!",
            ],
            "unknown": [
                "I'm not sure I understand. Could you rephrase that?",
                "That's an interesting question. Let me think about it differently.",
                "I don't have a specific answer for that, but I'm here to help however I can.",
            ]
        }
        
        # Commands mapping
        self.commands = {
            'time': self.get_time,
            'date': self.get_date,
            'weather': self.get_weather,
            'search': self.web_search,
            'wiki': self.wikipedia_search,
            'news': self.get_news,
            'joke': self.tell_joke,
            'quote': self.get_quote,
            'open': self.open_application,
            'save': self.save_response,
            'history': self.show_history,
            'clear': self.clear_history,
            'help': self.show_help,
            'voice': self.toggle_voice,
            'calculate': self.calculate,
            'system': self.system_info,
        }

        # Safe operators for math evaluation
        self.operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.BitXor: operator.xor,
            ast.USub: operator.neg,
        }

    def setup_voice(self):
        """Setup text-to-speech engine"""
        if TTS_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                self.tts_engine.setProperty('rate', 200)
                voices = self.tts_engine.getProperty('voices')
                if voices:
                    self.tts_engine.setProperty('voice', voices[0].id)
                print("🎤 Voice support initialized")
            except Exception as e:
                print(f"⚠️  Voice support error: {e}")
                self.tts_engine = None
        else:
            self.tts_engine = None

    def speak(self, text):
        """Text-to-speech output"""
        if self.voice_enabled and self.tts_engine:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"⚠️  TTS Error: {e}")

    def listen(self):
        """Speech-to-text input"""
        if not self.voice_enabled or not SPEECH_RECOGNITION_AVAILABLE:
            return None
            
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("🎤 Listening...")
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source, timeout=3, phrase_time_limit=5)
                text = r.recognize_google(audio)
                print(f"👤 You said: {text}")
                return text
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            print("⚠️  Could not understand audio")
            return None
        except Exception as e:
            print(f"⚠️  Speech recognition error: {e}")
            return None

    def get_time(self, *args):
        """Get current time"""
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}"

    def get_date(self, *args):
        """Get current date"""
        current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        return f"Today's date is {current_date}"

    def get_weather(self, city=None):
        """Get weather information"""
        if city and len(city) > 0:
            city_name = ' '.join(city)
        else:
            city_name = "your location"
        
        return f"Weather feature: For {city_name}, please check weather.com, accuweather.com, or your local weather service!"

    def web_search(self, query):
        """Open web search in browser"""
        if not query:
            return "Please provide a search query"
        
        query_str = ' '.join(query)
        search_url = f"https://www.google.com/search?q={'+'.join(query_str.split())}"
        try:
            webbrowser.open(search_url)
            return f"Opening web search for: {query_str}"
        except Exception as e:
            return f"Could not open browser: {e}"

    def wikipedia_search(self, query):
        """Search Wikipedia"""
        if not WIKIPEDIA_AVAILABLE:
            return "Wikipedia search unavailable. Install with: pip install wikipedia"
        
        if not query:
            return "Please provide a search query"
        
        try:
            wikipedia.set_lang("en")
            query_str = ' '.join(query)
            summary = wikipedia.summary(query_str, sentences=2)
            return f"Wikipedia says: {summary}"
        except wikipedia.exceptions.DisambiguationError as e:
            options = ', '.join(e.options[:5])
            return f"Multiple results found. Try being more specific. Options: {options}"
        except wikipedia.exceptions.PageError:
            return f"No Wikipedia page found for '{query_str}'"
        except Exception as e:
            return f"Wikipedia search error: {e}"

    def get_news(self, *args):
        """Get news headlines"""
        news_sources = [
            "📰 BBC News: bbc.com/news",
            "📰 Reuters: reuters.com", 
            "📰 CNN: cnn.com",
            "📰 AP News: apnews.com",
            "📰 NPR: npr.org"
        ]
        return f"Latest news sources:\n" + "\n".join(news_sources)

    def tell_joke(self, *args):
        """Tell a random joke"""
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? He was outstanding in his field!",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "What do you call a fake noodle? An impasta!",
            "Why did the coffee file a police report? It got mugged!",
            "Why don't programmers like nature? It has too many bugs!",
            "How many programmers does it take to change a light bulb? None, that's a hardware problem!",
        ]
        return random.choice(jokes)

    def get_quote(self, *args):
        """Get an inspirational quote"""
        quotes = [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Innovation distinguishes between a leader and a follower. - Steve Jobs", 
            "Life is what happens to you while you're busy making other plans. - John Lennon",
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
            "It is during our darkest moments that we must focus to see the light. - Aristotle",
            "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
        ]
        return random.choice(quotes)

    def open_application(self, app_name):
        """Open applications"""
        if not app_name:
            return "Please specify an application to open"
        
        app = ' '.join(app_name).lower()
        system = platform.system().lower()
        
        try:
            if system == "windows":
                if "browser" in app or "chrome" in app:
                    subprocess.run(["start", "chrome"], shell=True)
                elif "notepad" in app:
                    subprocess.run(["notepad"])
                elif "calculator" in app:
                    subprocess.run(["calc"])
                elif "explorer" in app:
                    subprocess.run(["explorer"])
                else:
                    subprocess.run(["start", app], shell=True)
            elif system == "darwin":  # macOS
                if "browser" in app or "safari" in app:
                    subprocess.run(["open", "-a", "Safari"])
                elif "finder" in app:
                    subprocess.run(["open", "-a", "Finder"])
                elif "calculator" in app:
                    subprocess.run(["open", "-a", "Calculator"])
                else:
                    subprocess.run(["open", "-a", app])
            else:  # Linux
                if "browser" in app or "firefox" in app:
                    subprocess.run(["firefox"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                elif "terminal" in app:
                    subprocess.run(["gnome-terminal"])
                elif "calculator" in app:
                    subprocess.run(["gnome-calculator"])
                else:
                    subprocess.run([app], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            return f"Opening {app}..."
        except Exception as e:
            return f"Could not open {app}: {e}"

    def safe_eval(self, node):
        """Safely evaluate mathematical expressions"""
        if isinstance(node, ast.Num):  # Python < 3.8
            return node.n
        elif isinstance(node, ast.Constant):  # Python >= 3.8
            return node.value
        elif isinstance(node, ast.BinOp):
            left = self.safe_eval(node.left)
            right = self.safe_eval(node.right)
            return self.operators[type(node.op)](left, right)
        elif isinstance(node, ast.UnaryOp):
            operand = self.safe_eval(node.operand)
            return self.operators[type(node.op)](operand)
        else:
            raise TypeError(f"Unsupported operation: {type(node)}")

    def calculate(self, expression):
        """Perform safe calculations"""
        if not expression:
            return "Please provide a mathematical expression"
        
        try:
            expr = ' '.join(expression) if isinstance(expression, list) else expression
            expr = expr.strip()
            
            # Replace common patterns
            expr = expr.replace('^', '**')  # Power operator
            
            # Check for dangerous patterns
            dangerous_patterns = ['import', 'exec', 'eval', '__', 'open', 'file']
            if any(pattern in expr.lower() for pattern in dangerous_patterns):
                return "Invalid expression: potentially dangerous operation"
            
            # Parse and evaluate safely
            tree = ast.parse(expr, mode='eval')
            result = self.safe_eval(tree.body)
            
            # Handle edge cases
            if isinstance(result, float):
                if math.isnan(result):
                    return "Calculation error: Result is not a number"
                elif math.isinf(result):
                    return "Calculation error: Result is infinity"
                else:
                    result = round(result, 10)
            
            return f"{expr} = {result}"
        except ZeroDivisionError:
            return "Calculation error: Division by zero"
        except (ValueError, TypeError, SyntaxError):
            return "Calculation error: Invalid expression"
        except Exception as e:
            return f"Calculation error: {str(e)}"

    def system_info(self, *args):
        """Get system information"""
        try:
            info = {
                "System": platform.system(),
                "Release": platform.release(), 
                "Machine": platform.machine(),
                "Processor": platform.processor() or "Unknown",
                "Python Version": platform.python_version(),
                "Architecture": platform.architecture()[0],
            }
            
            result = "💻 System Information:\n" + "="*30 + "\n"
            for key, value in info.items():
                result += f"{key}: {value}\n"
            
            return result
        except Exception as e:
            return f"System info error: {e}"

    def save_response(self, filename=None):
        """Save conversation to file"""
        if not self.conversation_history:
            return "No conversation to save"
        
        if not filename:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = [f"jarvis_conversation_{timestamp}.txt"]
        
        filepath = self.data_dir / f"{'_'.join(filename)}"
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"JarvisAI Conversation Log\n")
                f.write(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*50 + "\n\n")
                
                for entry in self.conversation_history:
                    f.write(f"[{entry['timestamp']}]\n")
                    f.write(f"You: {entry['user']}\n")
                    f.write(f"Jarvis: {entry['response']}\n\n")
            
            return f"Conversation saved to {filepath}"
        except Exception as e:
            return f"Could not save file: {e}"

    def show_history(self, *args):
        """Show conversation history"""
        if not self.conversation_history:
            return "No conversation history available"
        
        history = "📜 Conversation History:\n" + "="*40 + "\n"
        recent_entries = self.conversation_history[-5:]  # Last 5 entries
        
        for entry in recent_entries:
            history += f"[{entry['timestamp']}]\n"
            history += f"You: {entry['user']}\n"
            history += f"Jarvis: {entry['response']}\n\n"
        
        if len(self.conversation_history) > 5:
            history += f"... ({len(self.conversation_history) - 5} more entries)\n"
            history += "Use 'save' command to export full history\n"
        
        return history

    def clear_history(self, *args):
        """Clear conversation history"""
        self.conversation_history.clear()
        return "🗑️  Conversation history cleared"

    def toggle_voice(self, *args):
        """Toggle voice input/output"""
        if not TTS_AVAILABLE and not SPEECH_RECOGNITION_AVAILABLE:
            return "Voice features not available. Install with: pip install pyttsx3 SpeechRecognition"
        
        self.voice_enabled = not self.voice_enabled
        status = "enabled" if self.voice_enabled else "disabled"
        return f"🎤 Voice mode {status}"

    def show_help(self, *args):
        """Show available commands"""
        help_text = """
🤖 JarvisAI Commands:
==================
time              - Get current time
date              - Get current date  
weather [city]    - Get weather info
search [query]    - Open web search
wiki [query]      - Wikipedia search
news              - Get news sources
joke              - Tell a random joke
quote             - Get inspirational quote
open [app]        - Open application
calculate [expr]  - Perform calculation
system            - Show system info
save [filename]   - Save conversation
history           - Show chat history
clear             - Clear history
voice             - Toggle voice mode
help              - Show this help
exit/quit         - Exit Jarvis

🎯 Examples:
============
calculate 15 * 8 + 10
wiki artificial intelligence  
search python tutorials
open calculator
weather London

🎤 Voice Commands:
=================
Type 'voice' to enable voice input/output
Speak naturally after enabling voice mode
"""
        return help_text

    def process_command(self, user_input):
        """Process user commands"""
        if not user_input:
            return random.choice(self.responses["unknown"])
            
        words = user_input.lower().split()
        command = words[0] if words else ""
        args = words[1:] if len(words) > 1 else []
        
        # Check for exit commands
        if command in ['exit', 'quit', 'bye', 'goodbye']:
            return "EXIT"
        
        # Check for greetings
        if command in ['hello', 'hi', 'hey', 'greetings', 'howdy']:
            return random.choice(self.responses["greeting"])
        
        # Execute specific commands
        if command in self.commands:
            return self.commands[command](args)
        
        # Try partial matches
        for cmd, func in self.commands.items():
            if cmd.startswith(command) or command in cmd:
                return func(args)
        
        # Generate contextual response
        return self.generate_response(user_input)

    def generate_response(self, user_input):
        """Generate AI-like responses using pattern matching"""
        input_lower = user_input.lower()
        
        # Math detection
        if any(char in user_input for char in '+-*/=()') and any(char.isdigit() for char in user_input):
            return self.calculate(user_input)
        
        # Question patterns
        if any(word in input_lower for word in ['what', 'how', 'why', 'when', 'where', 'who']):
            if 'time' in input_lower:
                return self.get_time()
            elif 'date' in input_lower:
                return self.get_date()
            elif 'weather' in input_lower:
                return self.get_weather()
            elif any(word in input_lower for word in ['you', 'your', 'jarvis']):
                return "I'm Jarvis, your AI assistant. I'm here to help you with various tasks and questions! Type 'help' to see what I can do."
            else:
                return "That's a great question! Try using specific commands like 'wiki [topic]' or 'search [query]' for detailed information."
        
        # Emotional responses
        if any(word in input_lower for word in ['thank', 'thanks', 'appreciate']):
            return "You're welcome! I'm glad I could help. Is there anything else you need?"
        
        if any(word in input_lower for word in ['good', 'great', 'awesome', 'amazing']):
            return "I'm glad to hear that! How else can I assist you today?"
        
        # Default response
        return random.choice(self.responses["unknown"])

    def add_to_history(self, user_input, response):
        """Add conversation to history"""
        self.conversation_history.append({
            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'user': user_input,
            'response': response
        })

    def run(self):
        """Main conversation loop"""
        print("🤖 " + "="*60)
        print("🤖 Welcome to JarvisAI - Your Free AI Assistant!")
        print("🤖 " + "="*60)
        print("💡 Type 'help' for commands or 'exit' to quit")
        if TTS_AVAILABLE or SPEECH_RECOGNITION_AVAILABLE:
            print("🎤 Type 'voice' to enable voice interaction")
        print("💾 Data saved to:", self.data_dir.absolute())
        print()
        
        while True:
            try:
                # Get input (voice or text)
                user_input = None
                
                if self.voice_enabled:
                    print("🎤 Say something or press Enter for text input...")
                    voice_input = self.listen()
                    if voice_input:
                        user_input = voice_input
                    else:
                        user_input = input("👤 You: ").strip()
                else:
                    user_input = input("👤 You: ").strip()
                
                if not user_input:
                    continue
                
                # Process the input
                response = self.process_command(user_input)
                
                # Check for exit
                if response == "EXIT":
                    farewell = random.choice(self.responses["farewell"])
                    print(f"🤖 Jarvis: {farewell}")
                    self.speak(farewell)
                    break
                
                # Display response
                print(f"🤖 Jarvis: {response}")
                
                # Speak response if voice is enabled
                self.speak(response)
                
                # Add to history
                self.add_to_history(user_input, response)
                print()  # Add spacing
                
            except KeyboardInterrupt:
                print("\n🤖 Jarvis: Goodbye! Thanks for using JarvisAI!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                print("Type 'help' for available commands\n")

if __name__ == "__main__":
    try:
        jarvis = JarvisAI()
        jarvis.run()
    except Exception as e:
        print(f"❌ Failed to start JarvisAI: {e}")
        print("Please check your Python installation and dependencies")