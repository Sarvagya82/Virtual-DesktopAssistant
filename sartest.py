import pyttsx3 #pip install pyttsx3
import datetime
import re
import speech_recognition as sr #pip install speechRecognition
import wikipedia
import os
from pyowm import OWM
import webbrowser
import sys
import subprocess
from random import randint
import urllib.request
import urllib.parse
from urllib.request import urlopen
import bs4
from bs4 import BeautifulSoup as soup
import json
import smtplib
#new commands for whether
from pyowm.utils import config
from pyowm.utils import timestamps


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices[0].id)
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening! I am sofia Sir and I am your personal voice assistant, Please give a command or say 'help me' and I will tell you what all I can do for you")  
#yaha pas commnd dalna hai sofiua kaI am sofia Sir and I am your personal voice assistant, Please give a command or say 'help me' and I will tell you what all I can do for you
    speak("commnd pls.")

def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said : {query}\n")

    except Exception as e:
        #print(e)    
        print("Say that again please...")  
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('sarvagyamishra82@gmail.com', 'hshfAnasfasgganya89@&')
    server.sendmail('sarvagyamishra82@gmail.com', to, content)
    server.close()

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

        #Logic for executing tasks

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results.encode("utf-8"))
            speak(results)
        
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")   


        elif 'play music' in query:
            music_dir = 'F:\Music'
            songs = os.listdir(music_dir)
            length = len(songs)
            #print(f"Total Number of songs are : {length}")
            rand_song = randint(0,length-1)
            #print(songs)    
            speak('Playing song for you sir')
            print(f"Playing song for you sir {songs[rand_song]}\n")
            os.startfile(os.path.join(music_dir, songs[rand_song]))

        
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")

        
        elif 'current weather' in query:
             reg_ex = re.search('current weather in (.*)', query)
             if reg_ex:
                 city = reg_ex.group(1)
                 owm = OWM(API_key='*****************')
                 obs = owm.weather_at_place(city)
                 w = obs.get_weather()
                 k = w.get_status()
                 x = w.get_temperature(unit='celsius')
                 print(f"Current weather in {city} is {k} and the current temperature is {x['temp_max']}")
                 speak('Current weather in %s is %s and the Current temperature is %0.2f degree celcius' % (city, k, x['temp_max']))

        
        elif 'open' in query:
            reg_ex = re.search('open (.+)', query)
            if reg_ex:
                    domain = reg_ex.group(1)
                    print(domain)
                    url = 'https://www.' + domain
                    webbrowser.open(url)
                    speak('The website you have requested has been opened for you Sir.')
            else:
                    pass

        
        elif 'launch google chrome' in query:
            print('Launching Google Chrome...\n')
            chromePath = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
            os.startfile(chromePath)


        elif 'launch virtualbox' in query:
            print('Launching Oracle VM Virtualbox...\n')
            vboxPath = "D:\\Oracle\\Virtualbox\\VirtualBox.exe"
            os.startfile(vboxPath)


        
        elif 'search on youtube' in query:
             speak('Searching on youtube sir')
             reg_ex = re.search('search on youtube (.+)', query)
             if reg_ex:
                domain = query.split("youtube",1)[1]
                query_string = urllib.parse.urlencode({"search_query" : domain})
                html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
                search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
                #print("http://www.youtube.com/watch?v=" + search_results[0])
                webbrowser.open("http://www.youtube.com/watch?v={}".format(search_results[0]))
                pass

        
        elif 'news' in query:
           try:
              news_url="https://news.google.com/news/rss"
              Client=urlopen(news_url)
              xml_page=Client.read()
              Client.close()
              soup_page=soup(xml_page,"xml")
              news_list=soup_page.findAll("item")
              for news in news_list[:5]:
                  print(news.title.text)
                  print(news.pubDate.text)
                  print("-"*60)
                  speak(news.title.text.encode('utf-8'))
           except Exception as e:
                print(e)

        
        elif 'send email' in query:
            try:
                speak("What should I say?")
                print("What should I say?")
                content = takeCommand()
                to = "sarvagyamioshra828@gmail.com"    
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry sir. I am not able to send this email")
                 
        elif 'help me' in query:
            speak("""
            You can use these commands and I'll help you out :
            1. Open reddit subreddit : Opens the subreddit in default browser.
            2. Open xyz.com : replace xyz with any website name
            3. Send email/email : Follow up questions such as recipient name, content will be asked in order.
            4. Current weather in {cityname} : Tells you the current condition and temperture
            5. Hello
            6. play music : Plays song in your VLC media player
            7. change wallpaper : Change desktop wallpaper
            8. news for today : reads top news of today
            9. time : Current system time
            10. top stories from google news (RSS feeds)
            11. tell me about xyz : tells you about xyz
            """)

        
        elif 'how are you' in query:
            print("I am fine sir. Tell me how may I help you ?")
            speak("I am fine sir. Tell me how may I help you ?")

        
        elif 'who are you' in query:
            print("I am Jarvis Sir and I am your personal voice assistant.")
            speak("I am Jarvis Sir and I am your personal voice assistant")

        


        elif 'shutdown' in query:
            print('Bye Sir. Have a nice day')
            speak('Bye Sir. Have a nice day')
            sys.exit()
