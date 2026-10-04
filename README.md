# 🤖 JARVIS — AI Voice Assistant

> *"Just A Rather Very Intelligent System"*  
> A Python-based voice assistant for macOS, inspired by Iron Man's JARVIS.

---

## ✨ Features

| Command | What JARVIS Does |
|---|---|
| `"what is your name"` | Introduces itself |
| `"what is the time"` | Tells the current time |
| `"open google"` | Opens Google in your browser |
| `"[topic] according to wikipedia"` | Searches Wikipedia and reads a summary |
| `"exit"` | Says goodbye and quits |

- 🎙️ **Voice Recognition** — Listens via your microphone using Google Speech Recognition
- 🔊 **Text-to-Speech** — Uses macOS native `say` command (Daniel / Rishi voice)
- 🌐 **Wikipedia Search** — Fetches summaries using the Wikipedia REST API (no extra library needed)
- 📝 **Logging** — All errors are logged to `logs/application.log`
- 🕐 **Time-aware Greeting** — Good Morning / Afternoon / Evening based on current hour

---

## 📁 Project Structure

```
Jarvis/
├── main.py              # Main assistant logic
├── requirements.txt     # Python dependencies
├── run.sh               # Quick launch script
├── logs/
│   └── application.log  # Runtime error logs
└── README.md
```

---

## 🛠️ Setup & Installation

### Prerequisites

- macOS (required for `say` command TTS)
- [Anaconda](https://www.anaconda.com/) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- Working microphone
- Internet connection (for speech recognition & Wikipedia)

### 1. Create & activate the conda environment

```bash
conda create -n jarvis python=3.8 -y
conda activate jarvis
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

> **Note:** `pyaudio` requires PortAudio. If installation fails, run:
> ```bash
> brew install portaudio
> pip install pyaudio
> ```

### 3. Run JARVIS

```bash
# Option A — directly
conda activate jarvis
python main.py

# Option B — using the run script
./run.sh
```

---

## 🎤 Usage Examples

Once running, JARVIS will greet you based on the time of day. Speak naturally:

```
You  → "what is your name"
JARVIS → "My name is JARVIS"

You  → "what is the time"
JARVIS → "Sir the current time is 15:30:00"

You  → "open google"
JARVIS → "ok sir. opening google"   [opens browser]

You  → "Elon Musk according to wikipedia"
JARVIS → "Searching wikipedia"
JARVIS → "Elon Musk is a business magnate..."

You  → "exit"
JARVIS → "Good bye sir"
```

---

## ⚙️ How It Works

```
┌─────────────────────────────────────────────────────┐
│                      JARVIS                         │
│                                                     │
│  Microphone ──► SpeechRecognition ──► Google STT   │
│                        │                            │
│              ┌─────────▼──────────┐                 │
│              │   Command Parser   │                 │
│              └──┬──────┬──────┬───┘                 │
│                 │      │      │                     │
│             Time  Wiki  Open  Name ...              │
│                 │      │                            │
│                 └──►  macOS 'say' ──► 🔊 Speaker   │
└─────────────────────────────────────────────────────┘
```

### Voice Engine

JARVIS uses macOS's built-in `say` command for TTS. It automatically picks the best available voice:
1. **Daniel** — British English (classic JARVIS feel)
2. **Rishi** — Indian English (fallback)
3. System default (if neither is available)

### Wikipedia (No Library Needed)

Uses two Wikipedia APIs directly via `requests`:
- **Search API** to find the best matching page title
- **REST Summary API** to fetch a clean 2-sentence summary

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `SpeechRecognition` | Converts microphone audio to text |
| `pyaudio` | Microphone access |
| `requests` | Wikipedia API calls |
| `google-generativeai` | (Future) Gemini AI integration |
| `gTTS` | (Future) Google Text-to-Speech |
| `streamlit` | (Future) Web UI |

---

## 🐛 Troubleshooting

**`ModuleNotFoundError: No module named 'speech_recognition'`**  
→ Make sure you're in the correct conda environment:
```bash
conda activate jarvis
python main.py
```

**Microphone not detected**  
→ Grant Terminal microphone access in:  
`System Settings → Privacy & Security → Microphone`

**Speech recognition not working**  
→ Check your internet connection — Google STT requires it.

**`say` command not found**  
→ This project requires macOS. On other platforms, replace `subprocess.run(["say", ...])` with `pyttsx3`.

---

## 🚀 Roadmap

- [ ] Integrate **Gemini AI** for general Q&A beyond fixed commands
- [ ] Add **Spotify / Music** control
- [ ] Add **Weather** lookup
- [ ] Add **Reminder / Alarm** feature
- [ ] **Streamlit web UI** for visual display
- [ ] Wake word detection (*"Hey JARVIS"*)

---

## 👨‍💻 Author

**Manish Thakur**  
GitHub: [@Manishthakur99](https://github.com/Manishthakur99)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).