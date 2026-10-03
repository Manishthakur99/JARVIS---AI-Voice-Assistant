import speech_recognition as sr
import pyttsx3
import logging
import os

LOG_DIR = "logs"
LOG_FILE_NAME = "application.log"

os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE_NAME)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

#Taking male voice from my system

engine = pyttsx3.init()

# Speech clarity settings: rate (speed) and volume
engine.setProperty('rate', 175)     # Default is often too fast; 170-180 is natural & clear
engine.setProperty('volume', 1.0)   # 100% volume

# Get system voices
voices = engine.getProperty("voices")

# macOS default voices[0] is 'Albert' (a distorted robotic voice).
# We pick a clear male voice: 'Daniel' (British English - classic JARVIS voice) or 'Rishi' (Indian English).
selected_voice = None
for voice in voices:
    if "daniel" in voice.name.lower():  # British male voice (Classic Jarvis)
        selected_voice = voice.id
        break

if not selected_voice:
    for voice in voices:
        if "rishi" in voice.name.lower():  # Indian English male voice
            selected_voice = voice.id
            break

if selected_voice:
    engine.setProperty('voice', selected_voice)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.adjust_for_ambient_noise(source, duration=0.5)
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except Exception as e:
            logging.info(e)
            print("Say that again please")
            return "None"
    return query

while True:
    query = takeCommand()
    speak(query)
            