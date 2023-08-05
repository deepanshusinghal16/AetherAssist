import datetime
import win32com.client
speaker = win32com.client.Dispatch("SAPI.SpVoice")
import speech_recognition as sr
import webbrowser
import AppOpener as appOpener
import pywhatkit
import openai
from config import apikey
openai.api_key = apikey
from whatsappMessage import send_whatsapp_message

def say(text):
    speaker.Speak(text)


chatStr = ""
def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Deepanshu: {query}\n Jarvis: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.6
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio,language="en-in")
            print(f"User said {query}")
            return query.lower()
        except Exception as e:
            return ""

say("hello")

applications = {
            "calculator": "Calculator",
            "notepad": "Notepad",
            "whatsapp": "Whatsapp",
            "instagram": "Instagram",
            "chrome": "Google Chrome",
            "spotify": "Spotify",
            "telegram": "Telegram Desktop",
            "virtualbox": "Oracle VM VirtualBox"
            }
sites = [
            ["youtube", "https://youtube.com"],
            ["google", "https://google.com"],
            ["instagram", "https://instagram.com"],
            ["lc", "https://leetcode.com"],
            ["gfg", "https://practice.geeksforgeeks.org"],
            ["potd", "https://practice.geeksforgeeks.org/problem-of-the-day"]
        ]

while 1:
    print("Listening....")
    query = takeCommand()
    # say(query)
    if "send message" in query:
        name = ""
        while 1:
            say("To whom ? ")
            name = takeCommand()
            if name != "":
                break

        msg = ""
        while 1:
            say("what to send ? ")
            msg = takeCommand()
            if msg != "":
                break
        say(f"Sending {msg} to {name}")
        send_whatsapp_message(name, msg)

    # Opening the application
    elif "open" in query:
        opened = False
        for app_name, app_command in applications.items():
            if app_name in query:
                appOpener.open(app_command)
                say(f"Opening {app_name} boss")
                opened = True
                break
        if not opened:
            for site in sites:
                if site[0].lower() in query:
                    webbrowser.open(site[1])
                    say(f"Opening {site[0]} boss")
                    opened = True
                    break
        if not opened:
            say("Sorry, I couldn't find a matching application or site.")

    #         closing
    elif "close" in query:
        closed = False
        for app_name, app_command in applications.items():
            if app_name in query:
                try:
                    appOpener.close(app_name)  # Replace with the actual method to close applications
                    say(f"Closing {app_name} boss")
                    closed = True
                    break
                except Exception as e:
                    say(f"Couldn't close {app_name}. Error: {e}")

        if not closed:
            say(f"I don't find any opened application named {app_name}")

    # play songs or any video on YT
    elif "play" in query.lower():
        pywhatkit.playonyt(query.split("play ")[1])
    #     Time
    elif "time" in query.lower():
        say(f"The time is: " + datetime.datetime.now().strftime("%H:%M:%S"))

    #     ai chat
    # elif "using ai" in query:
    #     chat(query)

    #     Sleep
    elif "sleep" in query:
        say(f"Ok going to Sleep, bye sir")
        break
    else:
        print("Chatting...")


