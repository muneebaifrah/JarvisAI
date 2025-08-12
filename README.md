# 🤖 JarvisAI

JarvisAI is a **Python-based AI assistant** that can run both **locally** (with voice features) and on **Vercel** (as an API).  
It uses **OpenAI's GPT model** to generate intelligent responses.

---

## 🚀 Features

### **Local Mode**
- 🎤 **Voice recognition** (Speech-to-Text)  
- 🎧 **Text-to-Speech replies**  
- 💬 **GPT-powered chat with memory**

### **Vercel API Mode**
- 🌐 **Serverless API** deployment  
- 🔑 **Secure API key handling**  
- 🧩 Can integrate with **web apps or chat UIs**

---

## 📂 Folder Structure

```
JarvisAI/
├── api/
│   └── index.py          # Vercel API endpoint
├── requirements.txt      # Python dependencies
├── vercel.json           # Vercel deployment configuration
└── README.md             # Project documentation
```

---

## 🛠 Local Setup (Voice Assistant)

> **Note:** Local mode includes voice commands and text-to-speech.  
> Requires a microphone and speakers.

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/muneebaifrah/JarvisAI.git
cd JarvisAI
```

### **2️⃣ Create a Virtual Environment**
```bash
python -m venv venv
```
**Activate it:**
```bash
# macOS/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate
```

### **3️⃣ Install Requirements**
```bash
pip install -r requirements.txt
```

### **4️⃣ Add Your API Key**
Create a `.env` file in the project root:
```ini
OPENAI_API_KEY=your_openai_api_key_here
```

### **5️⃣ Run Locally**
```bash
python main.py
```

---

## 🌐 Deploy to Vercel (API Mode)

> **Tip:** API mode does not use microphone or TTS. It's made for web integrations.

### **1️⃣ Login to Vercel**
```bash
vercel login
```

### **2️⃣ Deploy**
```bash
vercel
```

### **3️⃣ Add Environment Variable on Vercel**
```bash
vercel env add OPENAI_API_KEY
```

### **4️⃣ Access Your API**
```
https://your-vercel-project.vercel.app/api
```

---

## ⚠️ Notes
- `api/index.py` → for Vercel API only  
- `main.py` → for running locally with voice features (not deployed)  
- **Never commit** `.env` or `config.py` to GitHub

---

## 🙌 Credits
Inspired by **CodeWithHarry** and enhanced for educational purposes.
