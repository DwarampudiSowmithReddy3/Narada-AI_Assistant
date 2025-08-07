import speech_recognition as sr

def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")  
        try:
            audio = r.listen(source, timeout=5)
            voice_data = r.recognize_google(audio)
            print("You said:", voice_data)
            return voice_data
        except sr.UnknownValueError:
            return "I couldn't understand that."
        except sr.RequestError:
            return "Sorry, I couldn't reach the recognition service."
