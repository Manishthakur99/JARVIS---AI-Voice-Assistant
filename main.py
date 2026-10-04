import speech_recognition as sr
import subprocess
import logging
import os
import datetime
import webbrowser
import requests

LOG_DIR = "logs"
LOG_FILE_NAME = "application.log"

os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE_NAME)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


# ---------- Voice (macOS 'say' command) ----------
def get_voice():
    out = subprocess.run(["say", "-v", "?"], capture_output=True, text=True).stdout.lower()
    for name in ["daniel", "rishi"]:   # Daniel = British (classic Jarvis), Rishi = Indian English
        if name in out:
            return name.capitalize()
    return None


VOICE = get_voice()


def speak(text):
    print("JARVIS:", text)
    cmd = ["say", "-r", "175"]
    if VOICE:
        cmd += ["-v", VOICE]
    cmd.append(text)
    subprocess.run(cmd)   # jab tak bol nahi leta, code aage nahi badhega
# -------------------------------------------------


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


def wish_me():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good Morning sir! How are you doing today?")
    elif hour < 18:
        speak("Good Afternoon sir! How are you doing today?")
    else:
        speak("Good Evening sir! How are you doing today?")

    speak("I am JARVIS. Tell me sir how can i help you?")


# ---------- Wikipedia (requests se, 'wikipedia' library ke bina) ----------
HEADERS = {"User-Agent": "JarvisAssistant/1.0 (manish@example.com)"}


def clean_query(text):
    text = text.lower()
    for phrase in ["according to wikipedia", "on wikipedia", "wikipedia",
                   "who is", "who was", "what is", "tell me about", "search"]:
        text = text.replace(phrase, "")
    return text.strip()


def wiki_summary(topic, sentences=2):
    # Step 1: best matching page title dhundho
    search = requests.get(
        "https://en.wikipedia.org/w/api.php",
        params={"action": "query", "list": "search", "srsearch": topic,
                "srlimit": 1, "format": "json"},
        headers=HEADERS, timeout=10,
    )
    hits = search.json()["query"]["search"]
    if not hits:
        return None
    title = hits[0]["title"]

    # Step 2: us title ka summary lo
    r = requests.get(
        "https://en.wikipedia.org/api/rest_v1/page/summary/" + title.replace(" ", "_"),
        headers=HEADERS, timeout=10,
    )
    if r.status_code != 200:
        return None
    extract = r.json().get("extract", "")
    return ". ".join(extract.split(". ")[:sentences]).strip()
# --------------------------------------------------------------------------


wish_me()
while True:
    query = takeCommand().lower()

    if query == "none":
        continue

    # Wikipedia sabse upar, taaki "name" jaise words se na takraye
    if "wikipedia" in query:
        speak("Searching wikipedia")
        query = clean_query(query)
        try:
            results = wiki_summary(query)
            if results:
                speak("According to wikipedia")
                speak(results)
            else:
                speak("I couldn't find that on wikipedia")
        except Exception as e:
            logging.info(e)
            print("Wikipedia error:", e)
            speak("Sorry sir, I couldn't reach wikipedia right now")

    elif "time" in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Sir the current time is {strTime}")

    elif "your name" in query or "name" in query:
        speak("My name is JARVIS")

    elif "open google" in query:
        speak("ok sir. opening google")
        webbrowser.open("google.com")

    elif "exit" in query:
        speak("Good bye sir")
        exit()