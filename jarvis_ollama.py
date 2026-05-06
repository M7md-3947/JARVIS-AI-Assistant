# ============================================================
#   J.A.R.V.I.S  —  Ollama Version (100% Offline & Free)
#   Features: Voice + Text | AI Chat | Open Apps/Web |
#             Time & Date  | Play Music on YouTube
# ============================================================
# SETUP (run once in your terminal):
#
#  1. Install Ollama from: https://ollama.com/download
#     (It's a small app — just download and run the installer)
#
#  2. Pull an AI model (choose ONE based on your RAM):
#     ollama pull llama3.2         ← Best quality (needs 8GB RAM)
#     ollama pull llama3.2:1b      ← Lighter (needs 4GB RAM)
#     ollama pull phi3             ← Very fast & light (needs 4GB RAM)
#
#  3. Install Python libraries:
#     pip install SpeechRecognition pyttsx3 pyaudio requests
#
#  4. Make sure Ollama is RUNNING (open Ollama app or run: ollama serve)
# ============================================================

import speech_recognition as sr
import pyttsx3
import requests
import json
import webbrowser
import datetime
import subprocess
import sys
import os
import time

# ─────────────────────────────────────────
#  CONFIGURATION  ← Edit this section
# ─────────────────────────────────────────
OLLAMA_MODEL = "llama3.2"          # Change to "phi3" or "llama3.2:1b" if needed
OLLAMA_URL   = "http://localhost:11434/api/chat"   # Default Ollama address
JARVIS_NAME  = "Jarvis"
WAKE_WORD    = "jarvis"
INPUT_MODE   = "both"              # "voice", "text", or "both"

# ─────────────────────────────────────────
#  SETUP: Text-to-Speech Engine
# ─────────────────────────────────────────
engine = pyttsx3.init()
engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)

voices = engine.getProperty("voices")
if voices:
    engine.setProperty("voice", voices[0].id)

def speak(text):
    """Make Jarvis speak out loud."""
    print(f"\n[{JARVIS_NAME}]: {text}")
    engine.say(text)
    engine.runAndWait()

# ─────────────────────────────────────────
#  SETUP: Ollama AI Brain (Local / Offline)
# ─────────────────────────────────────────
conversation_history = []   # Keeps memory of the conversation

SYSTEM_PROMPT = (
    f"You are {JARVIS_NAME}, a smart AI assistant like Tony Stark's Jarvis. "
    "Be helpful, concise, and slightly witty. Keep answers short unless asked for detail. "
    "You run entirely offline on the user's computer."
)

def ask_ollama(user_message):
    """Send a message to the local Ollama model and get a response."""
    global conversation_history

    # Add user message to history
    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    payload = {
        "model"   : OLLAMA_MODEL,
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history,
        "stream"  : False   # Get full response at once
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        assistant_message = data["message"]["content"]

        # Add assistant response to history (for memory)
        conversation_history.append({
            "role"   : "assistant",
            "content": assistant_message
        })

        # Keep history to last 20 messages to save memory
        if len(conversation_history) > 20:
            conversation_history = conversation_history[-20:]

        return assistant_message

    except requests.exceptions.ConnectionError:
        return (
            "I can't connect to Ollama. "
            "Please make sure Ollama is running. "
            "Open a terminal and type: ollama serve"
        )
    except requests.exceptions.Timeout:
        return "The AI is taking too long to respond. Try a lighter model like phi3."
    except Exception as e:
        return f"Something went wrong: {str(e)}"

def check_ollama_running():
    """Check if Ollama server is running before starting."""
    try:
        r = requests.get("http://localhost:11434", timeout=3)
        return True
    except:
        return False

# ─────────────────────────────────────────
#  SETUP: Speech Recognition
# ─────────────────────────────────────────
recognizer = sr.Recognizer()
recognizer.pause_threshold = 1.0
recognizer.energy_threshold = 300

def listen():
    """Listen to the microphone and return text."""
    with sr.Microphone() as source:
        print("\n[Listening...] 🎙️")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            text = recognizer.recognize_google(audio).lower()
            print(f"[You said]: {text}")
            return text
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            speak("Speech service is unavailable. Using text mode instead.")
            return ""

# ─────────────────────────────────────────
#  FEATURES
# ─────────────────────────────────────────

def get_time():
    now = datetime.datetime.now()
    return f"The current time is {now.strftime('%I:%M %p')}."

def get_date():
    now = datetime.datetime.now()
    return f"Today is {now.strftime('%A, %B %d, %Y')}."

def open_website(command):
    sites = {
        "youtube"  : "https://youtube.com",
        "google"   : "https://google.com",
        "github"   : "https://github.com",
        "reddit"   : "https://reddit.com",
        "twitter"  : "https://twitter.com",
        "instagram": "https://instagram.com",
        "wikipedia": "https://wikipedia.org",
        "gmail"    : "https://mail.google.com",
        "maps"     : "https://maps.google.com",
        "netflix"  : "https://netflix.com",
    }
    for site, url in sites.items():
        if site in command:
            webbrowser.open(url)
            return f"Opening {site} for you, sir."
    if "open" in command:
        query = command.replace("open", "").strip()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            return f"Searching for {query} in your browser."
    return None

def play_youtube(command):
    keywords = ["play", "youtube", "music", "song", "video"]
    query = command
    for word in keywords:
        query = query.replace(word, "").strip()
    if query:
        url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        webbrowser.open(url)
        return f"Playing {query} on YouTube."
    webbrowser.open("https://youtube.com")
    return "Opening YouTube for you."

def open_application(command):
    apps = {
        "notepad"     : ("notepad.exe"   , "gedit"),
        "calculator"  : ("calc.exe"      , "gnome-calculator"),
        "chrome"      : ("chrome"        , "google-chrome"),
        "vs code"     : ("code"          , "code"),
        "file explorer": ("explorer.exe" , "nautilus"),
    }
    for app, (win_cmd, linux_cmd) in apps.items():
        if app in command:
            try:
                if sys.platform == "win32":
                    subprocess.Popen(win_cmd)
                else:
                    subprocess.Popen(linux_cmd, shell=True)
                return f"Opening {app}."
            except:
                return f"I couldn't open {app}."
    return None

def jarvis_shutdown(command):
    shutdown_words = ["goodbye", "bye", "shutdown", "quit", "exit", "turn off", "stop"]
    return any(word in command for word in shutdown_words)

# ─────────────────────────────────────────
#  MAIN COMMAND PROCESSOR
# ─────────────────────────────────────────

def process_command(command):
    command = command.lower().strip()
    if not command:
        return

    if jarvis_shutdown(command):
        speak("Goodbye! It's been a pleasure serving you, offline and all.")
        sys.exit(0)

    if ("what" in command and "time" in command) or command == "time":
        speak(get_time())
        return

    if "date" in command or "day" in command or "today" in command:
        speak(get_date())
        return

    if "play" in command or ("youtube" in command and "open" not in command):
        speak(play_youtube(command))
        return

    if "open" in command or "go to" in command or "website" in command:
        result = open_website(command)
        if result:
            speak(result)
            return

    app_result = open_application(command)
    if app_result:
        speak(app_result)
        return

    # Fallback: Ask local Ollama AI
    speak("Thinking...")
    response = ask_ollama(command)
    speak(response)

# ─────────────────────────────────────────
#  MAIN LOOP
# ─────────────────────────────────────────

def main():
    print("=" * 55)
    print(f"  J.A.R.V.I.S  —  Ollama Offline Version")
    print(f"  Model: {OLLAMA_MODEL}")
    print("=" * 55)

    # Check if Ollama is running
    if not check_ollama_running():
        print("\n⚠️  WARNING: Ollama is not running!")
        print("   Start it by opening the Ollama app")
        print("   or running: ollama serve\n")
        speak(
            "Warning: I cannot connect to my local AI brain. "
            "Please start Ollama and try again. "
            "I'll still work for basic commands."
        )
    else:
        print(f"\n✅ Ollama is running with model: {OLLAMA_MODEL}")

    speak(f"Hello! I am {JARVIS_NAME}, running fully offline. How can I help you?")

    while True:
        command = ""

        if INPUT_MODE in ("voice", "both"):
            heard = listen()
            if not heard:
                # No voice input — fall to text
                pass
            elif WAKE_WORD in heard:
                speak("Yes, I'm listening.")
                time.sleep(0.3)
                heard = listen()
                command = heard
            else:
                command = heard

        if INPUT_MODE in ("text", "both") and not command:
            try:
                command = input("\n[You]: ").strip().lower()
            except KeyboardInterrupt:
                speak("Goodbye!")
                break

        if command:
            process_command(command)

if __name__ == "__main__":
    main()
