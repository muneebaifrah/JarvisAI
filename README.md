# JarvisAI 🤖

JarvisAI is a Python-based AI assistant that can run both **locally** (with voice features) and on **Vercel** (as an API).  
It uses OpenAI's GPT model to generate intelligent responses.

---

## 🚀 Features

- **Local Mode**:  
  - 🎤 Voice recognition (speech-to-text)  
  - 🎧 Text-to-speech replies  
  - 💬 GPT-powered chat with memory  

- **Vercel API Mode**:  
  - 🌐 Deployable as a serverless API  
  - 🔑 Secure API key handling  
  - 🧩 Can integrate with web apps or chat UIs  

---

## 📁 Folder Structure

JarvisAI/
├── api/
│ └── index.py # Vercel API endpoint
├── requirements.txt # Python dependencies
├── vercel.json # Vercel deployment configuration
└── README.md # Project documentation

yaml
Copy
Edit

---

## 🛠 Local Setup (Voice Assistant)

1. **Clone the Repository**
```bash
git clone https://github.com/muneebaifrah/JarvisAI.git
cd JarvisAI
Create a Virtual Environment

bash
Copy
Edit
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
Install Requirements

bash
Copy
Edit
pip install -r requirements.txt
Add Your API Key
Create a .env file:

ini
Copy
Edit
OPENAI_API_KEY=your_openai_api_key_here
Run Locally

bash
Copy
Edit
python main.py
🌐 Deploy to Vercel (API Mode)
Login to Vercel

bash
Copy
Edit
vercel login
Deploy

bash
Copy
Edit
vercel
Set Environment Variables on Vercel

bash
Copy
Edit
vercel env add OPENAI_API_KEY
Access Your API
Once deployed, your endpoint will be:

arduino
Copy
Edit
https://your-vercel-project.vercel.app/api
⚠ Notes
api/index.py is designed for Vercel deployment — it does not include microphone or TTS features.

For local mode, you need a main.py file (not included in Vercel deployment).

Keep your .env and config.py files out of GitHub.

🙌 Credits
Inspired by CodeWithHarry and enhanced for educational purposes.
