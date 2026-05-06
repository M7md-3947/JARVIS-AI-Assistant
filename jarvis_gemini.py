# ============================================================
#   J.A.R.V.I.S  —  Gemini Version
#   Features: Voice + Text | AI Chat | Open Apps/Web |
#             Time & Date  | Play Music on YouTube
# ============================================================
# SETUP (run once in your terminal):
#   pip install SpeechRecognition pyttsx3 google-generativeai pyaudio webbrowser
#
# API KEY:
#   Get a FREE Gemini API key at: https://aistudio.google.com/app/apikey
#   Paste it below where it says: YOUR_GEMINI_API_KEY_HERE
# ============================================================

import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
import webbrowser
import datetime
import subprocess
import sys
import os
import time

# ─────────────────────────────────────────
#  CONFIGURATION  ← Edit this section
# ─────────────────────────────────────────
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"   # ← Paste your key here
JARVIS_NAME    = "Jarvis"
WAKE_WORD      = "jarvis"                      # Say this word to wake Jarvis
INPUT_MODE     = "both"                        # "voice", "text", or "both"

# ─────────────────────────────────────────
#  SETUP: Text-to-Speech Engine
# ─────────────────────────────────────────
engine = pyttsx3.init()
engine.setProperty("rate", 175)       # Speed of speech (words per minute)
engine.setProperty("volume", 1.0)     # Volume: 0.0 to 1.0

# Try to set a male voice (index 0 is usually male)
voices = engine.getProperty("voices")
if voices:
    engine.setProperty("voice", voices[0].id)

def speak(text):
    """Make Jarvis speak out loud."""
    print(f"\n[{JARVIS_NAME}]: {text}")
    engine.say(text)
    engine.runAndWait()

# ─────────────────────────────────────────
#  SETUP: Gemini AI Brain
# ─────────────────────────────────────────
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=(
        f"You are {JARVIS_NAME}, a smart AI assistant like Tony Stark's Jarvis. "
        "Be helpful, concise, and slightly witty. Keep answers short unless asked for detail."
    )
)
chat = model.start_chat(history=[])  # Keeps conversation memory

def ask_gemini(prompt):
    """Send a message to Gemini and get a response."""
    try:
        response = chat.send_message(prompt)
        return response.text
    except Exception as e:
        return f"I'm having trouble connecting to my brain. Error: {str(e)}"

# ─────────────────────────────────────────
#  SETUP: Speech Recognition (Microphone)
# ─────────────────────────────────────────
recognizer = sr.Recognizer()
recognizer.pause_threshold = 1.0     # Seconds of silence before stopping
recognizer.energy_threshold = 300    # Microphone sensitivity

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
            speak("Speech service is unavailable. Please check your internet.")
            return ""

# ─────────────────────────────────────────
#  FEATURES
# ─────────────────────────────────────────

def get_time():
    """Tell the current time."""
    now = datetime.datetime.now()
    hour = now.strftime("%I")          # 12-hour format
    minute = now.strftime("%M")
    period = now.strftime("%p")        # AM or PM
    return f"The current time is {hour}:{minute} {period}."

def get_date():
    """Tell the current date."""
    now = datetime.datetime.now()
    day  = now.strftime("%A")          # Monday, Tuesday ...
    date = now.strftime("%B %d, %Y")   # January 01, 2025
    return f"Today is {day}, {date}."

def open_website(command):
    """Open a website based on the command."""
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
    # Try to extract a custom URL or search
    if "open" in command:
        query = command.replace("open", "").strip()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            return f"Searching for {query} in your browser."
    return None

def play_youtube(command):
    """Search and play something on YouTube."""
    keywords = ["play", "youtube", "music", "song", "video"]
    query = command
    for word in keywords:
        query = query.replace(word, "").strip()

    if query:
        url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        webbrowser.open(url)
        return f"Playing {query} on YouTube."
    else:
        webbrowser.open("https://youtube.com")
        return "Opening YouTube for you."

def open_application(command):
    """Open a desktop application."""
    apps = {
        "notepad"    : ("notepad.exe"                  , "notepad"),
        "calculator" : ("calc.exe"                     , "gnome-calculator"),
        "chrome"     : ("chrome.exe"                   , "google-chrome"),
        "vs code"    : ("code"                         , "code"),
        "file explorer":("explorer.exe"                , "nautilus"),
        "task manager": ("taskmgr.exe"                 , "gnome-system-monitor"),
    }
    for app, (win_cmd, linux_cmd) in apps.items():
        if app in command:
            try:
                if sys.platform == "win32":
                    subprocess.Popen(win_cmd)
                else:
                    subprocess.Popen(linux_cmd, shell=True)
                return f"Opening {app}."
            except Exception as e:
                return f"I couldn't open {app}. Make sure it's installed."
    return None

def jarvis_shutdown(command):
    """Check if user wants to shut Jarvis down."""
    shutdown_words = ["goodbye", "bye", "shutdown", "quit", "exit", "turn off", "stop"]
    return any(word in command for word in shutdown_words)

# ─────────────────────────────────────────
#  MAIN COMMAND PROCESSOR
# ─────────────────────────────────────────

def process_command(command):
    """Understand the command and respond."""
    command = command.lower().strip()

    if not command:
        return

    # ── Shutdown ──
    if jarvis_shutdown(command):
        speak("Goodbye! It's been a pleasure serving you.")
        sys.exit(0)

    # ── Time ──
    if "time" in command and "what" in command or command == "time":
        speak(get_time())
        return

    # ── Date ──
    if "date" in command or "day" in command or "today" in command:
        speak(get_date())
        return

    # ── Play Music / YouTube ──
    if "play" in command or ("youtube" in command and "open" not in command):
        result = play_youtube(command)
        speak(result)
        return

    # ── Open Website ──
    if "open" in command or "go to" in command or "website" in command:
        result = open_website(command)
        if result:
            speak(result)
            return

    # ── Open Application ──
    app_result = open_application(command)
    if app_result:
        speak(app_result)
        return

    # ── Fallback: Ask Gemini AI ──
    speak("Let me think about that...")
    response = ask_gemini(command)
    speak(response)

# ─────────────────────────────────────────
#  MAIN LOOP
# ─────────────────────────────────────────

def main():
    speak(f"Hello! I am {JARVIS_NAME}, your personal AI assistant. How can I help you?")

    while True:
        command = ""

        if INPUT_MODE in ("voice", "both"):
            # ── Voice input ──
            heard = listen()

            if not heard:
                continue

            # Wake word check (optional — remove if you want always-on)
            if WAKE_WORD in heard:
                speak("Yes, I'm here.")
                time.sleep(0.3)
                heard = listen()   # Listen for actual command after wake word

            command = heard

        if INPUT_MODE in ("text", "both") and not command:
            # ── Text input (fallback or primary) ──
            try:
                command = input("\n[You]: ").strip().lower()
            except KeyboardInterrupt:
                speak("Goodbye!")
                break

        if command:
            process_command(command)

if __name__ == "__main__":
    main()
