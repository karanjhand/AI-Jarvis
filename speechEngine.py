from gtts import gTTS
import pyttsx3
import speech_recognition as sr
import os
import re
import webbrowser
from time import gmtime, strftime
import smtplib
import requests
from weather import Weather

jarvisEngine = pyttsx3.init('sapi5')
voices = jarvisEngine.getProperty('voices')
print(voices)
jarvisEngine.setProperty('voice',voices[0].id)

def talkToMe(audio):
    "speaks audio passed as argument"
    jarvisEngine.say(audio)
    jarvisEngine.runAndWait()



def myCommand():
    "listens for commands"

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('say something...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')

    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('Your last command couldn\'t be heard')
        command = myCommand();

    return command


def assistant(command):
    "if statements for executing commands"

    if 'open reddit' in command:
        reg_ex = re.search('open reddit (.*)', command)
        url = 'https://www.reddit.com/'
        if reg_ex:
            subreddit = reg_ex.group(1)
            url = url + 'r/' + subreddit
        webbrowser.open(url)
        print('Done!')

    elif 'open google' in command:
        webbrowser.open('google.com')

    elif 'open music' in command:
        webbrowser.open('spotify.com')

    elif 'open youtube' in command:
        webbrowser.open('youtube.com')
        
    elif 'open facebook' in command:
        webbrowser.open('facebook.com')    

    elif 'what\'s up' in command:
        talkToMe('I''m great just enjoying your company')

    elif 'joke' in command:
        res = requests.get(
                'https://icanhazdadjoke.com/',
                headers={"Accept":"application/json"}
                )
        if res.status_code == requests.codes.ok:
            talkToMe(str(res.json()['joke']))
        else:
            talkToMe('oops!I ran out of jokes')

    elif 'open linkedIn' in command:
        webbrowser.open('linkedin.com')

    elif 'what is the date and time' in command:
        currentTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        talkToMe('current time is' + currentTime)


    elif 'send email' in command:
        talkToMe('Who is the recipient?')
        recipient = myCommand()

        if 'john' in recipient:
            talkToMe('What should I say?')
            content = myCommand()

            #init gmail SMTP
            mail = smtplib.SMTP('smtp.gmail.com', 587)

            #identify to server
            mail.ehlo()

            #encrypt session
            mail.starttls()

            #login
            mail.login('karan42283@gmail.com', 'sender Password')

            #send message
            mail.sendmail('karan42283@gmail.com', 'amritpalsinghs369@gmail.com', content)

            #end mail connection
            mail.close()

            talkToMe('Email sent.')
    

        else:
            talkToMe('I don\'t know what you mean!')

  
        

talkToMe('I am jarvis your personal assistant how can I help you')

#loop to continue executing multiple commands
endCondition  = True
while endCondition:
    assistant(myCommand())
    if myCommand() == 'go to sleep jarvis' :
        talkToMe('thank you for spending your time with me')
        break
   