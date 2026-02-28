# Narada AI Assistant

A comprehensive Python-based AI desktop assistant supporting both voice and text inputs, capable of intelligent task execution, real-time information retrieval, and system automation.

## Quick Start

### 1. Install Dependencies

Install the required Python packages:

```bash
pip install SpeechRecognition pyttsx3 wikipedia beautifulsoup4 opencv-python Pillow selenium webdriver-manager gpt4all requests
```

### 2. Configure Environment

Ensure you have a working microphone and speaker to fully utilize the speech-to-text and text-to-speech features. Note that PyAudio may be required for microphone input on some systems.

### 3. Start the Assistant

Run the main application script:

```bash
python assistant.py
```

## Features

- **Multi-Modal Input:** Interact via a clean graphical user interface (GUI) or voice commands.
- **Intelligent Queries:** Real-time web search and Wikipedia integration.
- **Media Playback:** Play songs effortlessly through automated YouTube searches.
- **System Automation:** Execute commands to launch desktop applications (VLC, Chrome, Notepad, etc.).
- **Conversational Engine:** Rich, pre-defined interactive responses designed to maintain a supportive and conversational tone.

## Project Structure

```text
Ai assistant/
├── assistant.py          # Main Tkinter application and conversational logic
├── action.py             # Advanced AI engine integration (GPT4All local LLM)
├── speech_to_text.py     # Microphone listening and Google Speech API logic
├── text_to_speech.py     # Pyttsx3 TTS synthesis logic
├── weather.py            # Future module for live weather capabilities
├── README.md             # Project documentation
├── DSR.png               # Developer branding asset
└── narada.jpg            # Application avatar asset
```

## Tech Stack

- **Frontend Interface:** Python Tkinter + Pillow (Image processing)
- **Voice & Audio Processing:** `SpeechRecognition` + `pyttsx3`
- **Search & Automation:** `wikipedia` API + `selenium` (headless browsing) + `requests` & `BeautifulSoup` (web scraping)
- **Experimental AI Engine:** `gpt4all` (Local Mistral LLM integration)
