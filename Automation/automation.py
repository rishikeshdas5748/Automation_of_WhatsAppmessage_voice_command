import time
import pywhatkit
import pyttsx3
import datetime
import speech_recognition as sr
from time import ctime
import webbrowser as wb

from pywhatkit.exceptions import CountryCodeException

engine = pyttsx3.init()
r = sr.Recognizer()


def speak(audio):
    engine.setProperty('rate', 180)
    print(audio)
    engine.say(audio)
    engine.runAndWait()


def get_voices(voice):
    voices = engine.getProperty('voice')
    if voices == 1:
        engine.setProperty('voice', voices[0].id)
    if voices == 2:
        engine.setProperty('voice', voices[1].id)
    # speak('This is Jarvis')


def whatsapp_response():
    contact = {'Amma': "+919447141334", 'dad': "+971529038191"}
    speak('To whom do you want to sent')
    name = voice_assistant()
    ph_no = contact[name]
    speak('say the message please')
    msg = voice_assistant()
    speak('say the time in hour')
    hrs = voice_assistant()
    speak('time in minutes')
    minutes = voice_assistant()
    speak('Please verify the details')
    speak('your phone number is ' + str(ph_no) + '\n the time is ' + hrs + ':' + minutes)
    # speak('\nPress 1 if all details are correct')
    # choice = input()
    try:
        pywhatkit.sendwhatmsg(ph_no, msg, int(hrs), int(minutes))
        speak('your message have been delivered')
    except CountryCodeException:
        speak('country code is missing')


def voice_assistant(ask=False):
    with sr.Microphone() as source:
        if ask:
            speak(ask)
        audio = r.listen(source, phrase_time_limit=5)
        voice_data1 = ' '
        try:
            voice_data1 = r.recognize_google(audio)
        except sr.UnknownValueError:
            speak('Sorry I did not get that')
        except sr.RequestError:
            speak('Sorry, my speech server is down.')
        return voice_data1


def response(voice_data):
    if 'what is your name' in voice_data:
        speak('I\'am JARVIS your virtual assistant.')
    if 'what time is it' in voice_data:
        speak(ctime())
    if 'search' in voice_data:
        speak('What do you want to search for ?')
        search = voice_assistant()
        url = 'https://google.com/search?q=' + search
        wb.get().open_new(url)
        speak('Here is what i found about ' + search)
    if 'send a WhatsApp message' in voice_data:
        whatsapp_response()
    if 'locate' in voice_data:
        speak('where do you want to locate ?')
        location = voice_assistant()
        url = 'https://google.nl/maps/place/' + location + '/&amp;'
        wb.get().open_new(url)
        speak('Here is the map of ' + location)
    if 'exit' in voice_data:
        speak('JARVIS shutting down!')
        exit(0)


def wish_me():
    greeting()
    speak("Welcome back")
    speak("what can i do now?")


def greeting():
    hour = datetime.datetime.now().hour
    if 6 <= hour < 12:
        speak("Good morning sir")
    elif 12 <= hour < 18:
        speak("Good afternoon sir")
    elif 18 <= hour < 24:
        speak("Good evening sir")
    else:
        speak("Good night sir")


get_voices(1)
time.sleep(1)
wish_me()
while 1:
    voice_data = voice_assistant()
    response(voice_data)
