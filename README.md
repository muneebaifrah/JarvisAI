
# 🤖 JarvisAI

JarvisAI is a **Python-based AI assistant** that can run both **locally** (as an interactive script) and on **Vercel** (as an API).  
It uses **OpenAI's GPT model** to generate intelligent responses.

---

## 🚀 Features

### **Local Mode (Standalone Script)**
- 💬 **Interactive command-line AI assistant**  
- 📝 **Chat with memory and command processing**  
- 💾 **Save AI responses to files**  
- ⏰ **Get current time and other commands**  
- 🔄 **Reset chat or exit anytime**

### **Vercel API Mode**
- 🌐 **Serverless API deployment**  
- 🔑 **Secure API key handling via environment variables**  
- 🧩 Can integrate with **web apps or chat UIs**

---

## 📂 Folder Structure

```
JarvisAI/
├── api/
│   └── index.py          # Vercel API endpoint
├── main.py               # Standalone local interactive script
├── requirements.txt      # Python dependencies
├── vercel.json           # Vercel deployment configuration
└── README.md             # Project documentation
```

---

## 🛠 Local Setup (Interactive Script)

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

> **Note:** API mode does not include voice or interactive CLI. It exposes a serverless HTTP API.

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
https://your-vercel-project.vercel.app/api/jarvis
```

---

## ⚠️ Notes
- `api/index.py` → Vercel API backend code  
- `main.py` → local interactive script (not deployed)  
- **Never commit** `.env` or secrets to GitHub  
- Use environment variables to keep API keys safe

---

## 🙌 Credits
Inspired by **CodeWithHarry** and enhanced for educational purposes.
