import sys
from googlesearch import search
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import pyaudio
import time
import requests, json
import math

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()
    
#talk("Hello I am alexa how may i help you")


def take_command():
    
    with sr.Microphone() as source:
        print("listening...")
        engine.say("Hello, how may I help you?")
        engine.runAndWait()
        listener.adjust_for_ambient_noise(source, duration=5)
        voice = listener.listen(source)
        try:
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(command)
        except LookupError:
            print("Could not understand audio")
    return command


def run_alexa():
    command = take_command()
    print(command)
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing '+song)
        pywhatkit.playonyt(song)
        
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I :%M %p')
        talk('Current time is'+time)
        
    elif 'who is' in command:
        person = command.replace('who is', '')
        info = wikipedia.summary(person, 1)
        print(info)
        talk(info)
        
    elif 'date' in command:
        dt = str(datetime.date.today())
        print(dt)
        talk("Today's date is"+dt)
        
    elif 'joke' in command:
        joke = pyjokes.get_joke()
        print(joke)
        talk(joke)
        
    elif 'stop' in command:
        sys.exit()
        
        
    elif 'search' in command:
        print('Hello from google')
        query = command.replace('search' ,'')
        for j in search(query, tld='co.uk' ,num=10, stop=10, pause=2):
            print(j)
            
    elif 'weather' in command:
        api_key = "4199205ee19b3a9177f26f930a600d67"
        
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        city_name = "london"
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name

        # get method of requests module
        # return response object
        response = requests.get(complete_url)
        # python format data
        x = response.json()
        
        if x["cod"] != "404":
            y = x["main"]
            print(x["main"])
            
            current_temperature = y["temp"]-273.15
            vals = math.trunc(current_temperature)
            
            print("Temperature (in celsius) is "+ str(vals))
            talk(vals)
        else:
            print("City not found")
        
            
        
if __name__ == "__main__":
    run_alexa()