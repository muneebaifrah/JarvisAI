# 🤖 JarvisAI - Free Local AI Assistant

JarvisAI is a **Python-based AI assistant** that runs completely **locally** without requiring expensive API keys. It features both a **web interface** (Flask server) and a **command-line interface** for interactive use.

## ✨ Features

### 🌐 **Web Interface (Flask Server)**
- **Modern responsive web UI** with gradient design
- **Real-time chat interface** with typing indicators
- **Quick command buttons** for common tasks
- **REST API endpoints** for integration
- **No external APIs required** - completely free!

### 💻 **Command Line Interface** 
- **Interactive terminal chat** with colored output
- **Voice input/output support** (optional)
- **Conversation history** with export functionality
- **Cross-platform compatibility** (Windows, macOS, Linux)

### 🛠️ **Core Capabilities**
- ⏰ **Time & Date** - Get current time and date
- 🔢 **Safe Calculator** - Perform mathematical calculations
- 😄 **Entertainment** - Random jokes and inspirational quotes
- 📚 **Wikipedia Search** - Access Wikipedia articles
- 🌐 **Web Search** - Open browser searches
- 💻 **System Info** - Display system information  
- 🗂️ **App Launcher** - Open system applications
- 💾 **History Management** - Save and export conversations
- 🎤 **Voice Features** - Speech-to-text and text-to-speech (optional)

---

## 🚀 Quick Start

### **1️⃣ Clone Repository**
```bash
git clone https://github.com/yourusername/JarvisAI.git
cd JarvisAI
```

### **2️⃣ Create Virtual Environment**
```bash
# Create virtual environment
python -m venv jarvis_env

# Activate it
# Windows:
jarvis_env\Scripts\activate
# macOS/Linux:
source jarvis_env/bin/activate
```

### **3️⃣ Install Dependencies**
```bash
# Install basic requirements
pip install -r requirements.txt

# Optional: For voice features (if desired)
pip install pyttsx3 SpeechRecognition
```

### **4️⃣ Run JarvisAI**

**Web Interface (Recommended):**
```bash
python app.py
```
Then open: http://localhost:5000

**Command Line Interface:**
```bash
python main.py
```

---

## 📂 File Structure

```
JarvisAI/
├── app.py              # Flask web server with modern UI
├── main.py             # Standalone command-line version
├── requirements.txt    # Python dependencies
├── jarvis_data/        # Generated conversation logs
└── README.md          # This file
```

---

## 🎯 Usage Examples

### **Basic Commands**
```
time                    → Get current time
date                    → Get today's date  
joke                    → Tell a random joke
quote                   → Get inspirational quote
help                    → Show all commands
```

### **Calculations**
```
calculate 15 * 8 + 10   → Perform math operations
calc 2^8                → Calculate powers
math sqrt(64)           → Advanced calculations
```

### **Information & Search**  
```
wiki artificial intelligence    → Wikipedia search
search python tutorials         → Open web search
system                         → Show system info
weather London                 → Weather information
```

### **System Operations**
```
open calculator        → Launch calculator app
open browser          → Open web browser  
save conversation     → Export chat history
clear                 → Clear conversation
```

---

## 🎤 Voice Features (Optional)

Enable voice interaction for hands-free operation:

```bash
# Install voice dependencies
pip install pyttsx3 SpeechRecognition

# In the application, type:
voice                 # Toggle voice mode on/off
```

**System Requirements for Voice:**
- **Windows**: Usually works out of the box
- **macOS**: `brew install portaudio`
- **Ubuntu/Debian**: `sudo apt-get install portaudio19-dev python3-pyaudio espeak-espeak-data`

---

## 🌐 API Endpoints (Flask Server)

When running `app.py`, these endpoints are available:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web interface |
| `/api/chat` | POST | Send message to Jarvis |
| `/api/commands` | GET | List available commands |
| `/api/history` | GET | Get conversation history |
| `/api/clear` | POST | Clear history |
| `/api/health` | GET | Health check |

**Example API Usage:**
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "tell me a joke"}'
```

---

## 🔧 Configuration

### **Environment Variables (Optional)**
Create a `.env` file for configuration:
```ini
# Optional settings
JARVIS_NAME=Jarvis
JARVIS_VOICE_ENABLED=false
JARVIS_DATA_DIR=jarvis_data
```

### **Customization**
- **Add new commands** by editing the `commands` dictionary
- **Customize responses** in the `responses` dictionary  
- **Add more jokes/quotes** to the respective lists
- **Modify UI styling** in the HTML template

---

## 🐛 Troubleshooting

### **Common Issues**

**Port already in use:**
```bash
# Change port in app.py
app.run(port=5001)  # Use different port
```

**Import errors:**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

**Voice features not working:**
```bash
# Install system dependencies first, then:
pip install pyttsx3 SpeechRecognition pyaudio
```

**Calculator errors:**
- Only basic math operations are supported
- Avoid using dangerous functions (for security)
- Use standard operators: +, -, *, /, **, ()

---

## 🎨 Screenshots

### Web Interface
- Modern gradient design with chat bubbles
- Quick command buttons for easy access  
- Real-time typing indicators
- Responsive design for mobile/desktop

### Command Line
- Colorful terminal output with emojis
- Interactive prompts and responses
- Voice input/output indicators
- Conversation history display

---

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to branch (`git push origin feature/amazing-feature`)  
5. **Open** a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** - see the LICENSE file for details.

---

## ⭐ Acknowledgments

- **Flask** for the web framework
- **Wikipedia API** for knowledge search
- **pyttsx3** for text-to-speech
- **SpeechRecognition** for speech-to-text
- Inspired by AI assistants and educational projects

---

## 🚫 No External APIs Required!

Unlike other AI assistants that require expensive API keys:
- ❌ No OpenAI API needed
- ❌ No Google API keys required  
- ❌ No monthly subscription fees
- ✅ **100% Free and Local**
- ✅ **Privacy-focused** - your data stays on your machine
- ✅ **Educational** - perfect for learning Python and AI concepts

---

**Happy Coding! 🎉**