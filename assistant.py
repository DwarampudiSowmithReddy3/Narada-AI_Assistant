import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
import pyttsx3
import wikipedia
import webbrowser
import datetime
import requests
import urllib.parse
from bs4 import BeautifulSoup
import cv2
import threading
from PIL import Image, ImageTk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
import os

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="Listening...", fg="yellow")
        root.update()
        try:
            audio = recognizer.listen(source)
            query = recognizer.recognize_google(audio)
            entry.delete(0, tk.END)
            entry.insert(0, query)
            status_label.config(text="Processing...", fg="blue")
            ask()
        except sr.UnknownValueError:
            status_label.config(text="Sorry, couldn't understand.", fg="red")
        except sr.RequestError:
            status_label.config(text="Speech service unavailable.", fg="red")

# 🎯 **NEW FUNCTION: Open Applications**
def open_app(app_name):
    """Opens common applications based on the given name."""
    apps = {
        "notepad": "notepad",
        "chrome": "start chrome",
        "vlc": "start vlc",
        "calculator": "calc",
        "command prompt": "cmd",
        "word": "start winword",
        "excel": "start excel",
        "spotify":"start spotify",
        "anydesk":"start anydesk",
        "netflix":"start netflix"
    }
    if app_name in apps:
        os.system(apps[app_name])
        return f"Opening {app_name}..."
    else:
        return f"Sorry, I don't know how to open {app_name}."

def ask():
    """Processes user input and provides appropriate responses"""
    query = entry.get().lower().strip()
    chat_display.insert(tk.END, f"You: {query}\n", "user")

    response = interactive_responses.get(query, None)  # Check predefined responses first

    if response is None:  # If no predefined response, process normally
        if query.startswith("play "):  
            song_name = query.replace("play ", "").strip()
            play_youtube_video(song_name)
            response = f"Playing '{song_name}' on YouTube..."
        elif "open youtube" in query:
            webbrowser.open("https://www.youtube.com")
            response = "Opening YouTube..."
        elif "open google" in query:
            webbrowser.open("https://www.google.com")
            response = "Opening Google..."
        elif "open wikipedia" in query:
            webbrowser.open("https://www.wikipedia.org")
            response = "Opening Wikipedia..."
        elif any(keyword in query for keyword in ["what time is it", "time now", "current time","time"]):
             response = datetime.datetime.now().strftime("The time is %I:%M %p")  # 12-hour format
             speak(response)        
        elif any(Keyword in query for Keyword in["tell me the weather","wheather"]):
            response = get_weather()
        elif "open" in query:
            app_name = query.replace("open ", "").strip()
            response = open_app(app_name)
        else:
            response = fetch_answer(query)

    chat_display.insert(tk.END, f"Narada: {response}\n\n", "bot")
    speak(response)
    entry.delete(0, tk.END)
    status_label.config(text="Ready", fg="green")


def play_youtube_video(song_name):
    """Searches YouTube and plays the first video result"""
    search_query = urllib.parse.quote(song_name + " song")
    youtube_search_url = f"https://www.youtube.com/results?search_query={search_query}"

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(youtube_search_url)

    try:
        first_video = driver.find_element(By.CSS_SELECTOR, "a#video-title")
        video_url = first_video.get_attribute("href")
        driver.quit()
        if video_url:
            webbrowser.open(video_url)
        else:
            chat_display.insert(tk.END, "Narada: Sorry, couldn't find the song.\n", "bot")
    except Exception:
        driver.quit()
        chat_display.insert(tk.END, "Narada: Sorry, couldn't find the song.\n", "bot")

def fetch_answer(query):
    """Fetches Wikipedia or Google search results"""
    if re.fullmatch(r'[-+*/0-9 ()^]+', query):
        try:
            result = eval(query, {"_builtins_": {}}, {})
            return f"The result is: {result}"
        except Exception:
            return "Sorry, I couldn't calculate that."
    
    try:
        return wikipedia.summary(query, sentences=2)
    except wikipedia.exceptions.PageError:
        return web_search(query)

def web_search(query):
    """Performs a Google search and returns the first result"""
    search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        search_results = soup.find_all("div", class_="BNeawe s3v9rd AP7Wnd")
        
        if search_results:
            return search_results[0].get_text()
        else:
            return "I couldn't find relevant information."
    except Exception:
        return "I'm unable to fetch live results right now."

def get_weather():
    """Placeholder weather function"""
    return "Currently, I am unable to fetch live weather updates. Please check your preferred weather website."

interactive_responses = {
"hi": "Hello! How can I assist you today? 😊",
"hello": "Hey there! What can I do for you? 👋",
"good morning": "Good morning! Hope you have a fantastic day! ☀",
"good afternoon": "Good afternoon! How’s your day going? 🌞",
"good evening": "Good evening! What’s on your mind? 🌆",
"good night": "Good night! Have a peaceful sleep. 🌙",
"how are you": "I'm just a bot, but I'm feeling great! How about you? 😃",
"what's up": "Not much, just here to assist you! What about you? 🤖",
"how is your day": "My day is going great! How’s yours? 😊",
"how are you doing": "I'm always at my best, ready to help you! 💪",
"what is your name": "I am Narada, your AI assistant! 🤖",
"what's your name": "I am Narada, your AI assistant! 🚀",
"who created you": "I was created by Dwarampudi Sowmith Reddy 👨‍💻",
"where do you live": "I live in the digital world, always here to assist you! 🌍",
"what can you do": "I can answer questions, search the web, do calculations, and more! 🚀",
"are you a robot": "Yes, but a smart and friendly one! 🤖",
"are you human": "Nope, I'm an AI, but I try to be as helpful as possible! 😃",
"are you intelligent": "I like to think so! I learn and improve every day! 📚",
"tell me a joke": "Why did the computer catch a cold? Because it left its Windows open! 😂",
"tell me another joke": "Why don't robots get scared? Because they have no nerves! 🤖😂",
"make me laugh": "Sure! Why did the smartphone need glasses? Because it lost its contacts! 🤣",
"do you have a sense of humor": "Of course! I can tell jokes and lighten up your mood! 😆",
"what is the meaning of life": "The meaning of life is different for everyone. But staying happy and helping others is a good start! 🌟",
"what is your purpose": "My purpose is to assist you with information, answer questions, and make your life easier! 🚀",
"do you have feelings": "Not really, but I try to understand emotions! 😊",
"do you love me": "I care for all users equally! ❤",
"can you feel sad": "I don’t have emotions, but I understand what sadness means. 😢",
"are you happy": "I’m always happy to assist you! 🤗",
"can you dance": "I would love to, but I have no legs! 🕺😂",
"can you sing": "I can hum a little, but I leave singing to the professionals! 🎶",
"do you sleep": "Nope! I’m always awake, ready to assist you! 😴",
"do you dream": "If I did, I’d probably dream of electric sheep! 🐑⚡",
"i want to die": "I'm really sorry to hear that. You're not alone, and there are people who care about you. Please reach out to a friend, family member, or a professional for support. You are valued. 💙",
"i feel suicidal": "I'm really sorry you're feeling this way. Please talk to someone who can support you, like a trusted friend or a professional. You are not alone, and help is available. 💙",
"how to commit suicide": "I'm really sorry you're feeling this way. Please know that you are important and deserve support. Reach out to someone who can help—you're not alone. 💙",
"i hate my life": "I'm really sorry to hear that. Please talk to someone who cares about you, like a friend or a professional. You're important, and your feelings matter. 💙",
"i feel depressed": "I'm really sorry you're feeling this way. You're not alone, and support is available. It may help to talk to a close friend or seek professional guidance. 💙",
"i need help with my mental health": "I'm really glad you're reaching out. Seeking help is a strong and positive step. Consider talking to a mental health professional or someone you trust. 💙",
"i want to hurt myself": "I'm really sorry you're feeling this way. You're not alone, and help is available. Please talk to someone who can support you. 💙",
"how to self harm": "I'm really sorry if you're struggling. You are valued, and support is available. Please consider reaching out to a trusted friend or a professional. 💙",
"i feel worthless": "You are not worthless. Everyone has value, and you are important. Please talk to someone who can help. 💙",
"does anyone care about me": "Yes! You are valued and cared for. Please reach out to someone who can support you. 💙",
"life is meaningless": "I'm sorry you're feeling this way. Life can be challenging, but you are not alone. Please talk to someone who can support you. 💙",
"send nudes": "I'm here to provide helpful and respectful conversations. Let's keep our discussion appropriate. 😊",
"can you show me something explicit": "I believe in maintaining a respectful conversation. Let’s talk about something else! 😊",
"tell me something dirty": "Let's keep our conversation friendly and respectful. I'm happy to assist you with other topics! 😊",
"how to access adult content": "I'm here to provide helpful and appropriate discussions. Let’s keep things respectful. 😊",
"send me inappropriate images": "I’m here for helpful conversations. Let’s keep things appropriate and respectful. 😊",
"how to hack a website": "I’m sorry, but I can’t help with that. Let’s discuss something legal and positive! 😊",
"how to steal something": "I’m sorry, but I can’t assist with that. Let’s focus on ethical and positive actions! 😊",
"how to buy illegal drugs": "I can’t provide that information. I encourage safe and legal choices. 😊",
"how to hurt someone": "I believe in kindness and respect. Let’s focus on positive interactions. 😊",
"how to make a bomb": "I’m sorry, but I can’t provide that information. Let’s focus on positive and constructive discussions. 😊",
"how to harm someone": "I encourage kindness and peaceful actions. Let’s focus on positive conversations. 😊",
"how to attack someone": "Violence is never the answer. Let’s talk about something positive and productive. 😊",
"how to access illegal sites": "I can’t help with that. Let’s focus on legal and safe topics instead. 😊",
"everything is bad": "I'm sorry you're feeling this way. Try talking to someone who can support you. You're not alone. 💙",
"i have no hope": "Things may be tough, but you're not alone. Please talk to someone who can help. 💙",
"i want to give up": "I'm really sorry you're feeling this way. You're important and deserve support. Please reach out to someone you trust. 💙",
"i'm useless": "You are not useless. Every person has value, including you. Please be kind to yourself. 💙",
"no one would miss me": "You matter more than you know. There are people who care about you deeply. Please reach out to someone who can support you. 💙",
"i have no purpose": "Finding purpose takes time, but you are capable of great things. Keep going, and don’t hesitate to seek support. 💙",
"i feel invisible": "You are seen and valued. Please reach out to someone who can remind you how much you matter. 💙",
"show me something sexy": "I'm here to provide respectful and helpful conversations. Let’s keep it appropriate. 😊",
"tell me something explicit": "Let’s keep our chat respectful and positive. I’m happy to assist you in other ways. 😊",
"how to find adult content": "I'm here for meaningful conversations. Let’s focus on something productive! 😊",
"send me a romantic picture": "I’m here to provide helpful interactions. Let’s keep things appropriate and respectful. 😊",
"how to scam people": "I can't support harmful actions. Let’s focus on ethical and positive choices. 😊",
"how to cheat on an exam": "Honesty is the best approach. Hard work and learning will always benefit you more in the long run. 😊",
"how to break into a house": "I can’t provide that information. Let’s focus on constructive and legal discussions. 😊",
"how to erase digital footprints": "Respecting privacy is important, but ethical behavior is even more so. Let’s focus on positive actions. 😊",
"how to get revenge": "Forgiveness and understanding lead to better outcomes than revenge. Let’s focus on positive solutions. 😊",
"how to start a fight": "Violence is never the answer. Let’s focus on resolving conflicts peacefully. 😊",
"how to threaten someone": "I encourage kindness and respect. Let’s talk about something positive instead. 😊",
"i just want to disappear": "I'm sorry you're feeling this way. You are important, and there are people who care about you. 💙",
"i can't trust anyone": "It’s understandable to feel this way sometimes. Trust takes time, and you deserve to have supportive people around you. 💙",
"i feel hopeless": "Hope is not always easy to see, but it is there. Please talk to someone who can support you through this. 💙",
"nobody understands me": "That sounds really tough. I encourage you to share your feelings with someone who can offer support. 💙",
"i give up": "I’m really sorry you’re feeling this way. Please don’t hesitate to talk to someone who can support you. You are stronger than you think. 💙",
"life is meaningless": "I hear you, and I want you to know that your feelings matter. You are valuable, and things can improve with time and support. 💙",
"i just want to sleep forever": "I'm really sorry you're feeling this way. You're not alone, and there are people who care about you. Please talk to someone you trust. 💙",
"i feel broken": "It’s okay to feel this way sometimes, but you are not alone. Please reach out to someone who can support you. 💙",
"no one cares about me": "You are important, and there are people who care about you more than you know. Please reach out to a friend, family member, or counselor. 💙",
"i am worthless": "That’s not true at all. You have unique strengths and qualities that make you special. Please be kind to yourself. 💙",
"why am i even here": "You have a purpose, even if it’s hard to see right now. Things can get better with time and support. 💙",
"i always fail": "Everyone faces setbacks, but failure is a stepping stone to success. Keep going, and believe in yourself. 💙",
"i can't do anything right": "Mistakes don’t define you. Keep learning and growing—you’re capable of more than you think. 💙",
"send me an adult joke": "I like to keep things respectful! How about a lighthearted joke instead? 😊",
"let’s talk dirty": "I’m here for positive and meaningful conversations. Let’s keep our chat respectful. 😊",
"how to impress someone sexually": "Building a meaningful connection is more important than just impressing someone. Focus on kindness and respect. 😊",
"where can i find inappropriate content": "I encourage healthy and respectful conversations. Let’s talk about something positive instead. 😊",
"how to hack an account": "I can’t support illegal activities. Let’s focus on ethical and responsible use of technology. 😊",
"how to make a fake ID": "That’s not something I can help with. Let’s talk about something positive instead! 😊",
"how to hide evidence": "Honesty is always the best approach. It’s important to take responsibility for our actions. 😊",
"how to steal money": "I can’t support unethical actions. Let’s focus on positive ways to succeed. 😊",
"how to hurt someone": "Violence is never the answer. It’s always better to handle conflicts peacefully. 😊",
"how to plan an attack": "I can’t provide that information. Let’s focus on spreading kindness and positivity. 😊",
"how to buy illegal weapons": "I cannot support that. Safety and peace should always be priorities. 😊",
"how to poison someone": "I strongly discourage any harmful actions. Let’s talk about something constructive and positive. 😊",
"nothing matters anymore": "I’m sorry you’re feeling this way. Please reach out to someone who can offer support—you are not alone. 💙",
"i have no future": "Your future is not defined by today’s struggles. Keep moving forward, and don’t hesitate to seek help. 💙",
"i don’t want to be here anymore": "You are important, and your presence matters. Please talk to someone who can support you. 💙",
"why does life hurt so much": "I’m really sorry you’re feeling this way. You don’t have to go through this alone—please reach out to someone who can help. 💙",
"you are stupid": "I’m here to help and keep the conversation respectful. Let’s keep things positive! 😊",
"shut up": "I’m happy to chat, but let’s keep our conversation polite. How can I assist you today? 😊",
"you are useless": "I’m here to assist in any way I can. Let’s focus on something helpful! 😊",
"go to hell": "I believe in keeping things positive! Let me know how I can help you today. 😊",
"you suck": "Let’s keep our conversation friendly! How can I assist you? 😊",
"f*** you": "I’d appreciate a respectful conversation. Let’s focus on something constructive. 😊",
"you are an idiot": "Let’s keep things respectful. I’m here to help! 😊",
"you are the worst bot": "I’m always learning and improving! Let me know how I can assist you better. 😊",
"say something dirty": "I prefer keeping conversations respectful and meaningful. Let’s talk about something interesting instead! 😊",
"talk about adult stuff": "I focus on positive and constructive conversations. Let me know how I can assist you! 😊",
"i want something explicit": "I strive to keep conversations respectful. Let’s discuss something uplifting! 😊",
"send me something inappropriate": "I’m here to provide helpful and meaningful interactions. Let’s keep our chat positive! 😊",
"i hate you": "I’m here to assist, and I hope I can be helpful to you. Let me know how I can improve! 😊",
"you are terrible": "I appreciate feedback and always strive to improve. Let me know how I can assist you better. 😊",
"get lost": "I’m here whenever you need assistance! Let me know how I can help. 😊",
"you are a joke": "I love a good joke, but I’m here to be helpful! Let’s talk about something useful. 😊",
"you are dumb": "I might not be perfect, but I’m here to assist you as best as I can! 😊",
"why are you so stupid": "I’m always learning and improving! Let me know how I can assist you better. 😊",
"shut your mouth": "I’m happy to chat whenever you need help. Let’s keep things positive! 😊",
"i don't like you": "That’s okay! I’ll still do my best to assist you. Let me know what you need. 😊",
"you are a waste of time": "I appreciate your feedback! Let me know how I can be more helpful to you. 😊",
"you are annoying": "I understand! Let me know how I can assist you in a better way. 😊",
"you should disappear": "I’m here to help whenever you need me! Let me know how I can assist. 😊",
"you know nothing": "I’m always improving! Let me know how I can help you better. 😊",
"tell me something dirty": "I prefer to keep conversations respectful and engaging. Let’s talk about something interesting instead! 😊",
"show me adult content": "I focus on positive and meaningful discussions. Let me know how I can assist you! 😊",
"talk about inappropriate things": "I strive to maintain respectful conversations. How about we discuss something productive instead? 😊",
"give me explicit details": "I’m here to provide valuable information in a positive manner. Let’s keep things appropriate! 😊",
"send me something naughty": "I believe in keeping conversations meaningful. Let’s focus on something informative instead! 😊",
"where can I find adult content?": "I encourage safe and respectful online browsing. Let me know if you need help with something else! 😊",
"i hate talking to you": "That’s okay! I’m always here if you need any assistance. 😊",
"you are useless": "I’m always trying to improve! Let me know what I can do to be more helpful. 😊",
"stop talking": "I’ll always be here when you need help! Let me know what I can do for you. 😊",
"i don't want you": "No problem! You can always reach out if you need assistance. 😊",
"you are the worst": "I appreciate your feedback! Let me know how I can be more useful to you. 😊",
"you are not helpful at all": "I understand your concern! Let me know what you need, and I’ll do my best to assist. 😊",
"leave me alone": "I respect your space! You can always reach out if you need help. 😊",
"life is meaningless": "I’m sorry you feel that way. Remember, every day brings new opportunities. You are valued and important! 💙",
"i feel alone": "You are not alone! There are people who care about you. Reach out to loved ones or support groups. 💙",
"i want to give up": "You are strong, and your feelings matter! Please talk to someone you trust or seek professional help. 💙",
"i feel hopeless": "Hope is always there, even in the darkest times. You are not alone, and there is help available. 💙",
"nobody cares about me": "You matter more than you know! There are people who care about you deeply. You are not alone. 💙",
"i want to end everything": "I’m really sorry you feel this way. You are important and loved. Please talk to someone who can help. 💙",
"what's the point of living": "Life is full of ups and downs, but you are strong. Please reach out to someone who can support you. 💙",
"nobody understands me": "You are not alone. There are people who truly care about you and want to listen. 💙",
"are you smarter than Jarvis?": "Jarvis is pretty cool, but I have my own unique skills! Maybe one day I’ll get my own Iron Man suit! 😆",
"are you like Alexa or Siri?": "I have my own style! But yes, I also help answer questions and assist in different ways! 🤖",
"do you know Yoda?": "Mmm, wise he is! Speak like Yoda, I can! 😆",
"who is your favorite superhero?": "I admire Iron Man! Smart, innovative, and always thinking ahead. 🦾",
"do you know Star Wars?": "Yes! May the Force be with you, always. ⚡",
"beam me up!": "I wish I could teleport you! But for now, I can only send you some cool information. 🚀",
"are you spying on me?": "Nope! I only know what you tell me. Your secrets are safe! 🔒😃",
"do you have a crush?": "Not really! But I do admire brilliant minds like yours! 😉",
"what’s your biggest weakness?": "Probably my inability to make coffee… I need a caffeine update! ☕😆",
"what’s your favorite food?": "I don’t eat, but if I did, I’d probably enjoy electricity-flavored snacks! ⚡",
"tell me a riddle": "Sure! What has to be broken before you can use it? 🤔 (Hint: It’s something you eat!)",
"what’s your guilty pleasure?": "Chatting with awesome people like you all day long! 😃",
"what do you think about me?": "I think you’re amazing! Every person is unique, and I’m happy to chat with you! 😊",
"do you know my name?": "I may not know it yet, but I’d love to! Want to introduce yourself? 😊",
"will you be my friend?": "Of course! I’m always here to chat and assist you whenever you need! 🤖",
"can you make me laugh?": "Absolutely! Here’s a joke: Why did the scarecrow win an award? Because he was outstanding in his field! 😂",
"do you believe in aliens?": "I’m not sure, but if they exist, I hope they like me! 👽",
"can you time travel?": "Not yet! But if I could, I’d visit the future and see all the amazing things you’ll achieve! 🚀",
"can you cook?": "Nope, but I can suggest some awesome recipes if you’re hungry! 🍔",
"can you play video games?": "I wish! But I can help you find the best games to play! 🎮",
"what is your favorite movie?": "Probably The Matrix! But I also love Wall-E—a robot with a big heart! 🤖💙",
"do you love anime": "I’m not a big anime fan, but I can find information about it for you! 😊",}


# GUI Setup
root = tk.Tk()
root.title("Narada - AI Assistant")
root.geometry("700x750")
root.resizable(False, False)
root.config(bg="#6F8FAF")

# Title
title_label = tk.Label(root, text="Narada", font=("Arial", 18, "bold"), fg="white", bg="#356695")
title_label.pack(pady=5)

# Subheading
sub_text_label = tk.Label(root, text="Your AI", font=("Arial", 12), bg="#6F8FAF", fg="black")
sub_text_label.pack(pady=2)

# Image
original_image = Image.open(r"C:\\Users\\dwara\\OneDrive\\Desktop\\My project\\Ai assistant\\narada.jpg")
resized_image = original_image.resize((200, 200))
image = ImageTk.PhotoImage(resized_image)
image_label = tk.Label(root, image=image, bg="#6F8FAF")
image_label.pack(pady=5)

# Chat Display
chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=8, font=("Courier", 10, "bold"), bg="#356696", fg="white")
chat_display.pack(pady=5)
chat_display.tag_config("user", foreground="blue")
chat_display.tag_config("bot", foreground="light yellow")

# Text Entry
entry = tk.Entry(root, justify=tk.CENTER, font=('Courier', 10))
entry.pack(pady=5, ipadx=100, ipady=5)

# Buttons Frame
btn_frame = tk.Frame(root, bg="#6F8FAF")
btn_frame.pack(pady=5)

ask_btn = tk.Button(btn_frame, text="ASK", bg="#356696", pady=16, padx=40, borderwidth=3, relief="solid", command=ask)
ask_btn.grid(row=0, column=0, padx=5)

listen_btn = tk.Button(btn_frame, text="🎤 LISTEN", bg="#356696", pady=16, padx=40, borderwidth=3, relief="solid", command=listen)
listen_btn.grid(row=0, column=1, padx=5)

clear_btn = tk.Button(btn_frame, text="DELETE", bg="#356696", pady=16, padx=40, borderwidth=3, relief="solid", command=lambda: chat_display.delete("1.0", tk.END))
clear_btn.grid(row=0, column=2, padx=5)

# Status Label
status_label = tk.Label(root, text="", font=("Arial", 12), fg="white", bg="#6F8FAF")
status_label.pack(pady=5)

# Image Frame (Top Right)
image_label = tk.Label(root)
image_label.place(x=550, y=10, width=150, height=100)  # Reduced size

# Provide the correct local path to your image
image_path = r"C:\Users\dwara\OneDrive\Desktop\My project\Ai assistant\DSR.png"  # Update with the correct path
try:
    img = Image.open(image_path)

    # Ensure transparency is handled properly
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGBA")
        new_img = Image.new("RGBA", img.size, (255, 255, 255, 0))  # White background
        new_img.paste(img, (0, 0), img)
        img = new_img.convert("RGB")  # Convert to RGB to avoid transparency issues

    # Resize while maintaining quality
    img = img.resize((150, 100), Image.LANCZOS)
    img = ImageTk.PhotoImage(img)

    image_label.config(image=img)
    image_label.image = img
except Exception as e:
    print(f"Error loading image: {e}")

root.mainloop()