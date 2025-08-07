import pyttsx3

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Adjust speech speed
    engine.say(text)
    engine.runAndWait()
