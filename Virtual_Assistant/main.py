import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
import gtts
import pygame
import os

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "api-key"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def speak_new(text):
    tts = gtts(text)
    tts.save('temp.mp3')

    pygame.mixer.init()
    
    # Load the mp3 file
    pygame.mixer.music.load("temp.mp3")
    
    # Play the mp3 file
    pygame.mixer.music.play()
    
    # Keep the program running while the music plays
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def aiProcess(command):
    client = OpenAI(
    api_key="open-ai-api-key"
    )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named blacky."},
            {
                "role": "user",
                "content": command
            }
        ]
    )

    return completion.choices[0].message.content

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()

            articles = data.get('articles', [])

            for article in articles:
                speak(article['title'])

    else:
        #let openai handle the request
        output = aiProcess(c)
        speak(output)

if __name__ == "__main__":
    speak("Initializing Sphinx...")
    while(True):
        # obtain audio from the microphone
        r = sr.Recognizer()
        
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Say something!")
                audio = r.listen(source)
            word = r.recognize_google(audio)
            if(word.lower()=="blacky"):
                speak("Ya")
                with sr.Microphone() as source:
                    print("Sphinx Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)

        except Exception as e:
            print("Error; {0}".format(e))
