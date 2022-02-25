# Requred modules
import sys
import webbrowser
import pyautogui
import speech_recognition as sr
import os
import webbrowser as wb
import datetime
import wikipedia
import pyttsx3
import time
import random
from datetime import date
import Weather
from app_dict import apps

owm = Weather.owm
mgr = owm.weather_manager()

observation = mgr.weather_at_place('Kathmandu')

w = observation.weather

temperature = w.temperature('celsius')
clouds = w.clouds


def weather_info():
    weather_status = w.detailed_status
    return weather_status


def humidity():
    h = w.humidity
    return h


def wind_speed():
    wind = w.wind()['speed']
    return wind


def current_temperature():
    temp = temperature['temp']
    return temp


def min_temperature():
    temp = temperature['temp_min']
    return temp


def max_temperature():
    temp = temperature['temp_max']
    return temp


def feels_like():
    temp = temperature['feels_like']
    return temp


# Required engines
engine = pyttsx3.init('sapi5')
rate = engine.getProperty('rate')
voices = engine.getProperty('voices')
volume = engine.getProperty('volume')
engine.setProperty('rate', 180)
engine.setProperty('voice', voices[1].id)
engine.setProperty('volume', 0.8)


# Speak function
def speak(text):
    engine.say(text)
    engine.runAndWait()
    print(text)


# Wishing in the beginning
def wish(text):
    engine.say(text)
    engine.runAndWait()


def openfile(file_name):
    files_path1 = 'C:/ProgramData/Microsoft/Windows/Start Menu/Programs'
    files_path2 = 'C:/Users/nbhel/AppData/Roaming/Microsoft/Windows/Start Menu/Programs'
    path1 = os.listdir(files_path1)
    path2 = os.listdir(files_path2)
    path = path1 + path2
    req_fil = file_name
    websites = ['youtube', 'facebook', 'instagram', 'twitter', 'wikipedia', 'gmail']
    junk_words = ['can you open ', 'can you please open ', 'open ']
    start = 0

    for words in junk_words:
        if words in req_fil:
            req_fil = req_fil.replace(words, '')
    if req_fil in websites:
        speak('ok opening '+req_fil)
        wb.get().open_new_tab('www.' + req_fil + '.com')
        start = 1
    else:
        for filename in path:
            fil_mod = filename.lower()
            if '.' in filename:
                if req_fil in fil_mod:
                    if filename in path1:
                        os.startfile(files_path1 + '/' + filename)
                        speak('Opening' + req_fil)
                        start = 1
                    elif filename in path2:
                        os.startfile(files_path2 + '/' + filename)
                        speak('Opening' + req_fil)
                        start = 1

    if start < 1:
        speak("No file found with that name")


# Wishing user
def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        wish('good morning sir. how are you')
    elif hour >= 12 and hour < 16:
        wish('good afternoon sir. how are you')
    else:
        wish('good evening sir. how are you')


# Taking voice input
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        audio = r.listen(source)
        r.energy_threshold = 800
        r.dynamic_energy_threshold = True
        try:
            print('Recognizing...')
            text1 = r.recognize_google(audio)
            text = text1.lower()
            print('You: ' + text)
        except:
            return ""
        return text


def sleep():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        r.energy_threshold = 500
        try:
            text1 = r.recognize_google(audio)
            text = text1.lower()
        except:
            return "none"
        return text


def close_apps(close_req):
    close_app = close_req
    websites = ['youtube', 'facebook', 'wikipedia', 'youtube.com', 'facebook.com', 'wikipedia.org']
    junk_words = ['can you close ', 'can you please close ', 'close ']
    for words in junk_words:
        if words in close_app:
            close_app = close_app.replace(words, '')
    try:
        if close_app in apps:
            os.system('TASKKILL /F /IM ' + apps[close_app] + '.exe')
        elif close_app in websites:
            pyautogui.hotkey('ctrl', 'w')
        else:
            os.system('TASKKILL /F /IM ' + close_app + '.exe')
        speak('Closed ' + close_app)
    except Exception as e:
        speak(close_app + ' is not open.')


# Logic of the program
text = ''
question = ''
type_sentence = ''
running = True
time.sleep(5)
wishme()
confirmation = False
digits = []
calculation = ''
sign = ''
sentence = ''
c = 0

# Operating according to input voice
while running:
    text = takecommand()
    question = text
    query4 = ''
    query3 = ''
    query1 = ''
    query5 = ''
    query2 = ''
    page1 = ''
    page2 = ''
    wakeup_txt = ''
    if 'good evening' in text or 'good morning' in text or 'good afternoon' in text:
        speak('how may i help you sir?')
    if 'search' in text and 'in wikipedia' in text or 'search about' in text and 'in wikipedia' in text or 'wikipedia' in text:
        query1 = text.replace('wikipedia', '')
        query3 = query1.replace('about', '')
        query4 = query3.replace('in', '')
        query5 = query4.replace('for', '')
        query2 = query5.replace('search', '')
        query6 = query2
        speak('do you want me to narrate or open webpage sir?')
        answer = takecommand()
        if 'narrate' in answer or 'direct' in answer:
            speak('searching about ' + query6)
            results = wikipedia.summary(query6, sentences=1, auto_suggest=False)
            speak('according to wikipedia: ' + results)
        elif 'web page' in answer or 'website' in answer or 'webpage' in answer:
            page1 = wikipedia.page(query2, auto_suggest=False)
            print(page1)
            page2 = page1.url
            print(page2)
            speak('redirecting to webpage')
            webbrowser.get().open_new_tab(page2)
            print(page2)
    elif 'add reminder' in text or 'check reminder' in text:
        if 'add' in text:
            speak('For which date do you want to add reminder?')
            rem_date = takecommand()
            if rem_date == 'today':
                rem_date = datetime.datetime.now().strptime(rem_date, '%B %d %Y')
            elif rem_date == 'tomorrow':
                rem_date = datetime.datetime.now() + datetime.timedelta(days=1)
            else:
                rem_date = datetime.datetime.strptime(rem_date, '%B %d %Y')
            rem_date = rem_date.strftime('%B %d %Y')
            speak('Can you say the reminder?')
            reminder = takecommand()
            file = open('Reminder.dat', 'a')
            file.write(rem_date + ': ' + reminder.capitalize() + '\n')
            speak('Reminder added')

        elif 'check' in text:
            file = open('Reminder.dat', 'r')
            lines = file.readlines()
            for i in lines:
                if datetime.datetime.now().strftime('%B %d %Y') in i:
                    speak('The reminder for today is ' + i.replace(datetime.datetime.now().strftime('%B %d %Y') + ': ',
                                                                   ''))
                    c = 1
            if c < 1:
                speak('There are no reminder for today')
            file.close()
    elif text == '':
        speak('sorry sir. can you say that again?')
    elif 'search' in text and 'in google' in text:
        query1 = text.replace('in google', '')
        query2 = query1.replace('search', '')
        speak('searching ' + query2 + ' in google')
        wb.get().open_new_tab('www.google.com/search?gx&q=' + query2)
    elif 'search' in text and 'in youtube' in text:
        query1 = text.replace('in youtube', '')
        query2 = query1.replace('search for', '')
        speak('searching ' + query2 + ' in youtube')
        wb.get().open_new_tab('https://www.youtube.com/results?search_query=' + query2)
    elif 'search' in text:
        abc1 = text.replace('search', '')
        abc2 = abc1.replace('about', '')
        abc3 = abc2.replace('for', '')
        speak('do you want me to search in google, wikipedia or youtube sir?')
        answer3 = takecommand()
        if 'google' in answer3:
            speak('searching for ' + abc3 + ' in google')
            wb.get().open_new_tab('www.google.com/search?gx&q=' + abc3)

        elif 'wikipedia' in answer3:
            speak('do you want me to narrate or open webpage sir?')
            answer2 = takecommand()
            if 'narrate' in answer2 or 'direct' in answer2:
                results = wikipedia.summary(abc3, sentences=1, auto_suggest=False)
                speak('according to wikipedia: ' + results)
            elif 'web page' in answer2 or 'website' in answer2 or 'webpage' in answer2:
                page1 = wikipedia.page(abc3, auto_suggest=False)
                print(page1)
                page2 = page1.url
                print(page2)
                speak('redirecting to webpage')
                webbrowser.get().open_new_tab(page2)
                print(page2)
        elif 'youtube' in answer3:
            speak('searching for ' + abc3 + 'in youtube')
            wb.get().open_new_tab('https://www.youtube.com/results?search_query=' + abc3)
    elif 'who is' in text:
        people1 = text.replace('who is', '')
        speak('searching about ' + people1)
        results = wikipedia.summary(people1, sentences=1, auto_suggest=False)
        speak(results)
    elif 'your name' in text or text == 'what is the name':
        speak('My name is Sylvie')
    elif text == 'hi' or text == 'hello' or text == 'hai' or text == 'hello hai' or text == 'hello hi':
        speak('Hello sir. how can I help you?')
    elif text == 'i am fine what about you' or text == "i'm fine what about you" or 'how are you' in text or 'what about you' in text:
        speak('I am great. do you need any help sir?')
    elif text == 'i am fine' or text == "i'm fine":
        speak('Great! do you need any help sir?')
    elif 'who created you' in text:
        speak('I was created by Nishchit Bhandari')
    elif text == 'introduce yourself' or text == 'who are you' or text == 'tell me something about yourself' or 'introduce yourself' in text:
        speak(
            'I am Sylvie. You can know me as personal computer and virtual assistant of Nishchit Bhandari. I was created by using python. I am 1 day old. currently, I am in development stage.')
    elif text == 'tell me something about mr bhandari' or text == 'tell me something about nishchit bhandari' or text == 'who is nishchit bhandari' or text == 'who is mr bhandari' or text == 'who is nishchit':
        speak(
            'Nishchit Bhandari is a student from nepal who wants to be a software engineer. As a practice and a small project, he created me and I am talking to you.')
    elif 'thank you' in text or 'thanks' in text:
        speak('You are welcome! enything else sir?')
    elif 'roll' in text and 'dice' in text:
        r = random.randint(1, 6)
        dice = str(r)
        speak('you got ' + dice)
    elif 'open ' in text:
        openfile(text)
    elif 'shut down the computer' in text or 'shutdown the computer' in text or 'shot down the computer' in text:
        speak('ok shutting down the computer')
        os.system('shutdown /s /f')
        running = False
        sys.exit()
    elif 'close ' in text:
        close_apps(text)
    elif 'stop typing' in text:
        speak('sir I already stopped typing')
    elif 'what' in text and 'time' in text:
        h = datetime.datetime.now().strftime("%H,%M,%S")
        speak(f"sir, the time is{h}")
    elif 'what' in text and 'date' in text:
        today = date.today()
        date_is = today.strftime("%B %d, %Y")
        speak(f'today is {date_is}')
    elif 'repeat' in text:
        speak('ok sir. say stop repeating if i have to stop')
        repeating = ''
        while repeating != 'stop repeating':
            repeating = takecommand()
            if repeating != 'stop repeating':
                speak(repeating)
            elif repeating == 'stop repeating':
                speak('ok sir. repeating stopped.')
    elif 'sleep' in text:
        speak('ok sir goodnight')
        sl_cr = ''
        while not 'wake up' in sl_cr:
            sl_cr = sleep()
            if sl_cr == 'quit':
                speak('bye bye sir. have a great day')
        speak('hello again sir')
    elif 'close' in text and 'camera' in text:
        speak('ok. closing camera')
        pyautogui.hotkey('alt', 'f4')
    elif 'search' in text and 'in youtube' in text:
        search_text1 = text.replace('search', '')
        search_text2 = search_text1.replace('in youtube', '')
        speak('searching for ' + search_text2 + ' in youtube')
        webbrowser.get().open_new_tab('https://www.youtube.com/results?search_query=' + search_text2)
    elif 'play' in text and 'music' in text or 'playlist' in text:
        speak('ok sir enjoy your music')
        os.system('spotify.exe')
        time.sleep(1)
        pyautogui.click(button='left')
        pyautogui.press('space')
        pyautogui.hotkey('alt', 'f4')
        while not 'wake up' in wakeup_txt:
            wakeup_txt = sleep()
            if wakeup_txt == 'quit':
                speak('bye bye sir. have a great day')
                running = False
                sys.exit()
            elif 'pause' in wakeup_txt or 'play' in wakeup_txt:
                os.system('spotify')
                time.sleep(1)
                pyautogui.press('space')
                pyautogui.hotkey('alt', 'f4')
            elif 'close spotify' in wakeup_txt:
                os.system('TASKKILL /F /IM Spotify.exe')
        speak('hello again sir')
    elif text == 'quit' or text == 'sylvie bye' or text == 'sylvie quit' or text == 'bye' or 'bye' in text or 'quit' in text or 'quick' in text:
        speak('bye bye sir. thanks for your time and have a beautiful day')
        running = False
        sys.exit()
    elif '1' in text or '2' in text or '3' in text or '4' in text or '5' in text or '6' in text or '7' in text or '8' in text or '9' in text or '0' in text:
        sign = ''
        sentence = ''
        calculation = ''
        for syl in text:
            if syl.isdigit() or syl == '+' or syl == '-' or syl == '/' or syl == 'plus' or syl == 'minus' or syl == 'multiplied by' or syl == 'divided by':
                if syl == '+' or syl == 'plus':
                    syl = '+'
                    sign = ' plus '
                elif syl == '-' or syl == 'minus':
                    syl = '-'
                    sign = ' minus '
                elif syl == '/' or syl == 'divided by':
                    syl = '/'
                    sign = ' divided by '
                else:
                    sign = syl
                calculation += syl
                sentence += sign
            elif syl == 'x':
                calculation += '*'
                sign = ' multiplied by '
                sentence += sign
        speak(sentence + ' is ' + str(eval(calculation)))
    elif 'weather' in text:
        speak('Today we can see some ' + weather_info() + '. The humidity is ' + str(
            humidity()) + '. Wind is blowing at the speed of ' + str(
            wind_speed()) + ' meters per second. The current temperature is ' + str(
            current_temperature()) + ' degree celsius')
    elif 'start' in text and 'typing' in text:
        speak("You can recite sir, I'll start typing")
        sentence_type = ''
        while not 'stop typing' in sentence_type:
            sentence_type = takecommand()
            if not 'stop typing' in sentence_type:
                pyautogui.write(sentence_type.capitalize() + '. ', interval=0.001)
        speak('OK sir, stopped typing.')
    elif 'temperature' in text:
        if 'current' in text:
            speak('The temperature is ' + str(current_temperature() + ' degree celsius'))
        elif 'maximum' in text:
            speak("Today's maximum temperature is " + str(max_temperature()) + ' degree celsius')
        elif 'minimum' in text:
            speak("Today's minimum temperature is " + str(min_temperature()) + ' degree celsius')
        else:
            speak("The current temperature is " + str(
                current_temperature()) + ' degree celsius, maximum temperature is ' + str(
                max_temperature()) + ' degree celsius, minimum temperature is ' + str(
                min_temperature()) + ' degree celsius and it feels like ' + str(
                feels_like()) + ' degree celsius.')
    else:
        speak('sorry sir that is not assigned. do you want to search for ' + text + '?')
        confirmation = takecommand()
        if 'yes' in confirmation:
            speak('do you want me to search in google, wikipedia or youtube sir?')
            answer4 = takecommand()
            if 'google' in answer4:
                speak('searching for ' + text + ' in google')
                wb.get().open_new_tab('www.google.com/search?gx&q=' + text)

            elif 'wikipedia' in answer4:
                speak('do you want me to narrate or open webpage sir?')
                answer2 = takecommand()
                if 'narrate' in answer2 or 'direct' in answer2:
                    speak('searching about ' + text)
                    results = wikipedia.summary(text, sentences=1, auto_suggest=False)
                    speak('according to wikipedia: ' + results)
                elif 'web page' in answer2 or 'website' in answer2 or 'webpage' in answer2:
                    page1 = wikipedia.page(text, auto_suggest=False)
                    print(page1)
                    page2 = page1.url
                    print(page2)
                    speak('redirecting to webpage')
                    webbrowser.get().open_new_tab(page2)
                    print(page2)
            elif 'youtube' in answer4:
                speak('searching for ' + text + 'in youtube')
                wb.get().open_new_tab('https://www.youtube.com/results?search_query=' + text)

        elif 'no' in confirmation:
            speak('ok. anything else sir?')
