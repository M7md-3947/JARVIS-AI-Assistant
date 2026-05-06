# J.A.R.V.I.S 🤖
### Just A Rather Very Intelligent System

A fully functional AI voice + text assistant inspired by Tony Stark's J.A.R.V.I.S — built with Python. Comes in two versions: one powered by **Google Gemini** (online) and one powered by **Ollama** (completely offline and free).

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat&logo=python)
![Gemini](https://img.shields.io/badge/AI-Google%20Gemini-orange?style=flat&logo=google)
![Ollama](https://img.shields.io/badge/AI-Ollama%20%28Offline%29-green?style=flat)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat)

---

## 📸 Demo

> Talk to Jarvis by voice or type your commands — it responds, opens apps, plays music, and answers any question using AI.

---

## ✨ Features

- 🎙️ **Voice Recognition** — Speak to Jarvis using your microphone
- ⌨️ **Text Mode** — Type commands if you prefer or have no mic
- 🧠 **AI-Powered Answers** — Ask anything, powered by Gemini or Ollama
- 🌐 **Open Websites** — YouTube, Google, GitHub, Reddit, Instagram & more
- 🎵 **Play Music** — Searches and plays any song/artist on YouTube
- 🕐 **Time & Date** — Ask for the current time or date
- 💻 **Open Applications** — Launch Notepad, Calculator, VS Code & more
- 💬 **Conversation Memory** — Remembers what you said earlier in the chat
- 🔒 **Offline Version** — Ollama version works with zero internet connection

---

## 🗂️ Project Structure

```
jarvis/
├── gemini_version/
│   └── jarvis_gemini.py     # Online version using Google Gemini AI
├── ollama_version/
│   └── jarvis_ollama.py     # Offline version using Ollama (local AI)
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11 — Download from [python.org](https://python.org/downloads/release/python-3119/)
- A microphone (optional — text mode works without one)

### Installation

**1. Clone this repository**
```bash
git clone https://github.com/YOUR_USERNAME/jarvis.git
cd jarvis
```

**2. Install dependencies**
```bash
pip install SpeechRecognition pyttsx3 google-generativeai pyaudio requests
```

> ⚠️ **PyAudio on Windows:** If `pip install pyaudio` fails, run:
> ```
> pip install pipwin
> pipwin install pyaudio
> ```

---

## 🔑 Version A — Gemini (Online)

**1. Get a free API key**
- Go to [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
- Sign in with Google → Click **"Create API Key"** → Copy it

**2. Add your key to the code**

Open `gemini_version/jarvis_gemini.py` and replace:
```python
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
```
with your actual key.

**3. Run**
```bash
cd gemini_version
python jarvis_gemini.py
```

---

## 🔒 Version B — Ollama (Offline)

**1. Install Ollama**
- Download from [https://ollama.com/download](https://ollama.com/download)

**2. Pull an AI model** (choose based on your RAM)
```bash
ollama pull llama3.2        # Best quality — needs 8GB RAM
ollama pull llama3.2:1b     # Lighter — needs 4GB RAM
ollama pull phi3            # Fastest — needs 4GB RAM
```

**3. Run Ollama**, then run Jarvis
```bash
cd ollama_version
python jarvis_ollama.py
```

---

## 🗣️ Example Commands

| What you say | What Jarvis does |
|---|---|
| `"Jarvis, what time is it?"` | Tells you the current time |
| `"What's today's date?"` | Tells you the date |
| `"Open YouTube"` | Opens YouTube in your browser |
| `"Play lo-fi music"` | Searches on YouTube and plays it |
| `"Open GitHub"` | Opens GitHub in your browser |
| `"What is machine learning?"` | Asks the AI and reads the answer |
| `"Open Notepad"` | Launches Notepad on your PC |
| `"Goodbye"` | Shuts Jarvis down |

---

## ⚙️ Configuration

At the top of each file you can customize:

```python
JARVIS_NAME = "Jarvis"       # Change the name (e.g. "Friday")
WAKE_WORD   = "jarvis"       # Word to activate voice mode
INPUT_MODE  = "both"         # "voice", "text", or "both"
```

**Adding new websites** (in `open_website` function):
```python
"twitch": "https://twitch.tv",
"linkedin": "https://linkedin.com",
```

---

## 🛠️ Troubleshooting

| Problem | Fix |
|---|---|
| `No module named 'pyaudio'` | `pip install pipwin` then `pipwin install pyaudio` |
| Jarvis can't hear me | Check microphone is set as default in Windows settings |
| Gemini API error | Check your API key is correct and you have internet |
| Ollama connection error | Make sure Ollama app is open / run `ollama serve` |
| Works slow on Ollama | Switch to a lighter model: `OLLAMA_MODEL = "phi3"` |

---

## 🧰 Built With

- [Python 3.11](https://python.org)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) — Voice input
- [pyttsx3](https://pypi.org/project/pyttsx3/) — Text to speech
- [Google Gemini API](https://aistudio.google.com) — Online AI brain
- [Ollama](https://ollama.com) — Offline local AI brain
- [webbrowser](https://docs.python.org/3/library/webbrowser.html) — Open websites & YouTube

---

## 📄 License

This project is licensed under the MIT License — feel free to use, modify, and share it.

---

## 👤 Author

**Your Name**
- GitHub: [@M7md-3947](https://github.com/M7md-3947)

---

## ⭐ Show Your Support

If you found this project useful, please give it a **star** ⭐ — it helps a lot!

---

*"Sometimes you gotta run before you can walk." — Tony Stark*
