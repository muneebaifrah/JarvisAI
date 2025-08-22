#!/usr/bin/env python3
"""
JarvisAI Flask Server - Free Alternative to Vercel
Run locally with: python app.py
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import datetime
import random
import json
import os
import platform
import webbrowser
import re
import ast
import operator
import math

# Try to import optional dependencies
try:
    import wikipedia
    WIKIPEDIA_AVAILABLE = True
except ImportError:
    WIKIPEDIA_AVAILABLE = False
    print("⚠️  Wikipedia not available. Install with: pip install wikipedia")

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

class JarvisAPI:
    def __init__(self):
        self.conversation_history = []
        
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
        
        # Jokes and quotes
        self.jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? He was outstanding in his field!",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "What do you call a fake noodle? An impasta!",
            "Why did the coffee file a police report? It got mugged!",
            "Why don't programmers like nature? It has too many bugs!",
            "How many programmers does it take to change a light bulb? None, that's a hardware problem!",
        ]
        
        self.quotes = [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Innovation distinguishes between a leader and a follower. - Steve Jobs",
            "Life is what happens to you while you're busy making other plans. - John Lennon",
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
            "It is during our darkest moments that we must focus to see the light. - Aristotle",
            "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
        ]

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

    def get_time(self):
        """Get current time"""
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}"

    def get_date(self):
        """Get current date"""
        current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        return f"Today's date is {current_date}"

    def get_joke(self):
        """Get a random joke"""
        return random.choice(self.jokes)

    def get_quote(self):
        """Get a random quote"""
        return random.choice(self.quotes)

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
        try:
            # Clean the expression
            expression = expression.strip()
            
            # Replace common math functions
            expression = expression.replace('^', '**')  # Power operator
            
            # Check for dangerous patterns
            dangerous_patterns = ['import', 'exec', 'eval', '__', 'open', 'file']
            if any(pattern in expression.lower() for pattern in dangerous_patterns):
                return "Invalid expression: potentially dangerous operation"
            
            # Parse and evaluate safely
            tree = ast.parse(expression, mode='eval')
            result = self.safe_eval(tree.body)
            
            # Handle division by zero and other edge cases
            if isinstance(result, float):
                if math.isnan(result):
                    return "Calculation error: Result is not a number"
                elif math.isinf(result):
                    return "Calculation error: Result is infinity"
                else:
                    result = round(result, 10)  # Limit decimal places
            
            return f"{expression} = {result}"
        except ZeroDivisionError:
            return "Calculation error: Division by zero"
        except (ValueError, TypeError, SyntaxError) as e:
            return f"Calculation error: Invalid expression"
        except Exception as e:
            return f"Calculation error: {str(e)}"

    def get_system_info(self):
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
            
            result = "System Information:\n"
            for key, value in info.items():
                result += f"{key}: {value}\n"
            
            return result
        except Exception as e:
            return f"System info error: {e}"

    def wikipedia_search(self, query):
        """Search Wikipedia"""
        if not WIKIPEDIA_AVAILABLE:
            return "Wikipedia search unavailable. Please install: pip install wikipedia"
        
        if not query:
            return "Please provide a search query for Wikipedia"
        
        try:
            wikipedia.set_lang("en")
            summary = wikipedia.summary(query, sentences=2)
            return f"Wikipedia says: {summary}"
        except wikipedia.exceptions.DisambiguationError as e:
            options = ', '.join(e.options[:5])
            return f"Multiple results found. Try being more specific. Options: {options}"
        except wikipedia.exceptions.PageError:
            return f"No Wikipedia page found for '{query}'"
        except Exception as e:
            return f"Wikipedia search error: {str(e)}"

    def show_help(self):
        """Show available commands"""
        help_text = """🤖 JarvisAI API Commands:
==================
time - Get current time
date - Get current date
joke - Tell a joke
quote - Get inspirational quote
calculate [expression] - Perform calculation (e.g., 2+2, 10*5)
system - Show system info
wiki [query] - Wikipedia search
weather - Weather info
search [query] - Web search suggestion
help - Show this help

📡 API Usage:
============
POST /api/chat
Body: {"message": "your command here"}
Response: {"response": "Jarvis response"}

GET /api/commands - List available commands
GET /api/history - Get conversation history
POST /api/clear - Clear history
"""
        return help_text

    def process_message(self, user_input):
        """Process user messages"""
        if not user_input:
            return random.choice(self.responses["unknown"])
        
        words = user_input.lower().split()
        command = words[0] if words else ""
        args = ' '.join(words[1:]) if len(words) > 1 else ''
        
        # Check for greetings
        if command in ['hello', 'hi', 'hey', 'greetings', 'howdy']:
            return random.choice(self.responses["greeting"])
        
        # Check for farewells
        if command in ['bye', 'goodbye', 'exit', 'quit', 'farewell']:
            return random.choice(self.responses["farewell"])
        
        # Execute specific commands
        if command == 'time':
            return self.get_time()
        elif command == 'date':
            return self.get_date()
        elif command == 'joke':
            return self.get_joke()
        elif command == 'quote':
            return self.get_quote()
        elif command in ['calculate', 'calc', 'math']:
            if args:
                return self.calculate(args)
            else:
                return "Please provide a mathematical expression (e.g., 2+2, 10*5, 100/4)"
        elif command == 'system':
            return self.get_system_info()
        elif command == 'wiki':
            return self.wikipedia_search(args)
        elif command == 'weather':
            city = args if args else "your location"
            return f"Weather feature: Please check weather.com or your local weather service for {city}!"
        elif command == 'help':
            return self.show_help()
        elif command == 'search':
            if args:
                return f"To search for '{args}', visit: https://www.google.com/search?q={'+'.join(args.split())}"
            else:
                return "Please provide a search query"
        elif command in ['clear', 'reset']:
            self.conversation_history.clear()
            return "Conversation history cleared!"
        else:
            return self.generate_response(user_input)

    def generate_response(self, user_input):
        """Generate AI-like responses using pattern matching"""
        input_lower = user_input.lower()
        
        # Math detection - check if input contains mathematical expressions
        if re.search(r'[\d+\-*/()=]', user_input) and any(char.isdigit() for char in user_input):
            return self.calculate(user_input)
        
        # Question patterns
        if any(word in input_lower for word in ['what', 'how', 'why', 'when', 'where', 'who']):
            if 'time' in input_lower:
                return self.get_time()
            elif 'date' in input_lower:
                return self.get_date()
            elif any(word in input_lower for word in ['you', 'your', 'jarvis']):
                return "I'm Jarvis, your AI assistant. I'm here to help you with various tasks and questions! Type 'help' to see what I can do."
            else:
                return "That's a great question! Try using specific commands like 'wiki [topic]' for detailed information or 'help' to see all commands."
        
        # Emotional responses
        if any(word in input_lower for word in ['thank', 'thanks', 'appreciate']):
            return "You're welcome! I'm glad I could help. Is there anything else you need?"
        
        if any(word in input_lower for word in ['good', 'great', 'awesome', 'amazing', 'excellent']):
            return "I'm glad to hear that! How else can I assist you today?"
        
        if any(word in input_lower for word in ['bad', 'terrible', 'awful', 'horrible']):
            return "I'm sorry to hear that. Is there anything I can help you with to make things better?"
        
        # Default response
        return random.choice(self.responses["unknown"])

    def add_to_history(self, user_input, response):
        """Add conversation to history"""
        self.conversation_history.append({
            'timestamp': datetime.datetime.now().isoformat(),
            'user': user_input,
            'response': response
        })

# Initialize Jarvis API
jarvis_api = JarvisAPI()

# Web interface HTML template (updated)
WEB_INTERFACE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JarvisAI - Your Free AI Assistant</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0; 
            padding: 20px; 
            min-height: 100vh;
        }
        
        .container { 
            max-width: 900px; 
            margin: 0 auto; 
            background: rgba(255, 255, 255, 0.95); 
            border-radius: 20px; 
            overflow: hidden;
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
            backdrop-filter: blur(10px);
        }
        
        .header { 
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white; 
            padding: 30px; 
            text-align: center; 
        }
        
        .header h1 { 
            margin: 0; 
            font-size: 2.8em; 
            font-weight: 300;
            text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }
        
        .header p { 
            margin: 15px 0 0 0; 
            opacity: 0.9; 
            font-size: 1.2em;
        }
        
        .status { 
            padding: 10px 30px; 
            background: rgba(40, 167, 69, 0.1); 
            color: #28a745; 
            text-align: center;
            font-weight: 500;
        }
        
        .chat-area { 
            padding: 20px; 
            min-height: 450px; 
            max-height: 550px; 
            overflow-y: auto;
            background: #f8f9fa;
        }
        
        .message { 
            margin: 15px 0; 
            padding: 18px 24px; 
            border-radius: 18px; 
            max-width: 75%;
            animation: fadeIn 0.3s ease-out;
            word-wrap: break-word;
        }
        
        .user-msg { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; 
            margin-left: auto; 
            text-align: right;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }
        
        .jarvis-msg { 
            background: white; 
            border: 2px solid #e9ecef;
            margin-right: auto;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .input-area { 
            padding: 25px; 
            background: white;
            border-top: 1px solid #e9ecef;
        }
        
        .input-group { 
            display: flex; 
            gap: 15px; 
            align-items: center;
        }
        
        input[type="text"] { 
            flex: 1; 
            padding: 18px 24px; 
            border: 2px solid #e9ecef; 
            border-radius: 30px; 
            font-size: 16px;
            outline: none;
            transition: all 0.3s ease;
        }
        
        input[type="text"]:focus { 
            border-color: #4facfe; 
            box-shadow: 0 0 0 3px rgba(79, 172, 254, 0.1);
        }
        
        button { 
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white; 
            border: none; 
            padding: 18px 30px; 
            border-radius: 30px; 
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(79, 172, 254, 0.3);
        }
        
        button:hover { 
            transform: translateY(-2px); 
            box-shadow: 0 6px 20px rgba(79, 172, 254, 0.4);
        }
        
        .commands { 
            padding: 20px; 
            background: rgba(255,255,255,0.9); 
            font-size: 0.95em;
            border-bottom: 1px solid #e9ecef;
        }
        
        .cmd-btn { 
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            margin: 4px; 
            padding: 8px 16px; 
            font-size: 0.85em;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.2s ease;
            display: inline-block;
        }
        
        .cmd-btn:hover {
            transform: translateY(-1px);
            box-shadow: 0 3px 10px rgba(40, 167, 69, 0.3);
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(15px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .typing-indicator {
            display: none;
            padding: 15px 25px;
            color: #6c757d;
            font-style: italic;
            text-align: center;
        }
        
        .typing-dots::after {
            content: '';
            animation: dots 1.4s infinite;
        }
        
        @keyframes dots {
            0%, 20% { content: '●'; }
            40% { content: '●●'; }
            60% { content: '●●●'; }
            80%, 100% { content: ''; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 JarvisAI</h1>
            <p>Your Free Local AI Assistant - No External APIs Required!</p>
        </div>
        
        <div class="status">
            ✅ Server Running Locally | 🚀 Ready to Assist
        </div>
        
        <div class="commands">
            <strong>🎯 Quick Commands:</strong><br>
            <button class="cmd-btn" onclick="sendCommand('time')">⏰ time</button>
            <button class="cmd-btn" onclick="sendCommand('date')">📅 date</button>
            <button class="cmd-btn" onclick="sendCommand('joke')">😄 joke</button>
            <button class="cmd-btn" onclick="sendCommand('quote')">💭 quote</button>
            <button class="cmd-btn" onclick="sendCommand('calculate 15*8')">🔢 calculate</button>
            <button class="cmd-btn" onclick="sendCommand('system')">💻 system</button>
            <button class="cmd-btn" onclick="sendCommand('help')">❓ help</button>
        </div>

        <div class="chat-area" id="chatArea">
            <div class="message jarvis-msg">
                🤖 Hello! I'm Jarvis, your free local AI assistant. I can help you with calculations, time, jokes, quotes, Wikipedia searches, and more! Try the commands above or type your own message.
            </div>
        </div>

        <div class="typing-indicator" id="typingIndicator">
            <span class="typing-dots">🤖 Jarvis is thinking</span>
        </div>

        <div class="input-area">
            <div class="input-group">
                <input type="text" id="messageInput" placeholder="Ask me anything... (try: calculate 2+2, joke, time)" onkeypress="handleEnter(event)">
                <button onclick="sendMessage()">Send</button>
            </div>
        </div>
    </div>

    <script>
        async function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            if (!message) return;

            // Add user message to chat
            addMessage(message, true);
            input.value = '';

            // Show typing indicator
            showTyping();

            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify({ message: message })
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                hideTyping();
                addMessage(data.response, false);
            } catch (error) {
                console.error('Error:', error);
                hideTyping();
                addMessage('Sorry, there was an error processing your request. Please try again.', false);
            }
        }

        function sendCommand(command) {
            document.getElementById('messageInput').value = command;
            sendMessage();
        }

        function addMessage(text, isUser) {
            const chatArea = document.getElementById('chatArea');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user-msg' : 'jarvis-msg'}`;
            messageDiv.textContent = isUser ? text : `🤖 ${text}`;
            chatArea.appendChild(messageDiv);
            chatArea.scrollTop = chatArea.scrollHeight;
        }

        function showTyping() {
            document.getElementById('typingIndicator').style.display = 'block';
        }

        function hideTyping() {
            document.getElementById('typingIndicator').style.display = 'none';
        }

        function handleEnter(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        // Focus input on load
        window.onload = () => {
            document.getElementById('messageInput').focus();
            hideTyping();
        };
    </script>
</body>
</html>
'''

# Routes
@app.route('/')
def index():
    """Serve the web interface"""
    return render_template_string(WEB_INTERFACE)

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat API endpoint"""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        user_message = data['message']
        if not user_message.strip():
            return jsonify({'error': 'Message cannot be empty'}), 400
            
        response = jarvis_api.process_message(user_message)
        jarvis_api.add_to_history(user_message, response)
        
        return jsonify({
            'response': response,
            'timestamp': datetime.datetime.now().isoformat(),
            'status': 'success'
        })
    
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get conversation history"""
    try:
        return jsonify({
            'history': jarvis_api.conversation_history,
            'count': len(jarvis_api.conversation_history),
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clear', methods=['POST'])
def clear_history():
    """Clear conversation history"""
    try:
        jarvis_api.conversation_history.clear()
        return jsonify({'message': 'History cleared', 'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/commands', methods=['GET'])
def get_commands():
    """Get available commands"""
    try:
        commands = {
            'time': 'Get current time',
            'date': 'Get current date',
            'joke': 'Tell a random joke',
            'quote': 'Get an inspirational quote',
            'calculate': 'Perform mathematical calculations',
            'system': 'Show system information',
            'wiki': 'Search Wikipedia',
            'weather': 'Get weather information',
            'search': 'Web search suggestions',
            'help': 'Show available commands'
        }
        return jsonify({
            'commands': commands,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat(),
        'service': 'JarvisAI Flask Server'
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("🤖 " + "="*60)
    print("🤖 Starting JarvisAI Flask Server...")
    print("🤖 " + "="*60)
    print("🌐 Web Interface: http://localhost:5000")
    print("📡 API Endpoint: http://localhost:5000/api/chat")
    print("📚 Commands List: http://localhost:5000/api/commands")
    print("❤️  Health Check: http://localhost:5000/api/health")
    print("🛑 Press Ctrl+C to stop the server")
    print("🤖 " + "="*60)
    
    # Run the Flask app
    app.run(
        host='0.0.0.0',  # Listen on all interfaces
        port=5000,       # Port 5000
        debug=True,      # Enable debug mode
        threaded=True    # Handle multiple requests
    )