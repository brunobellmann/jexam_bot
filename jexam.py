#!/usr/bin/env python
# coding: utf8

import requests
import re
import json
import traceback
from dotenv import load_dotenv
import os
from datetime import date

# get bot_token
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

# get current date for scope
today = date.today()
semester = 'Sommersemester 2020'

# set wintersemester range
winterStart = (2, 1)
winterEnd = (6, 1)

# set sommersemester range
sommerStart = (7, 1)
sommerEnd = (11, 1)

# check for semester
if winterStart < (today.month, today.day) < winterEnd:
    shortyear = today.strftime("%y")
    nextyear = int(shortyear) + 1
    semester = "Wintersemester " + str(shortyear) + "/" + str(nextyear)
elif sommerStart < (today.month, today.day) < sommerEnd:
    semester = "Sommersemester " + year
else:
    exit

lookfor = []
removable = {}

with open("sessions.json") as json_data_file:
    sessions = json.load(json_data_file)

    for user in sessions.get("sessions"):
        for c in user['data']['courses']:
            lookfor.append(c)

# sort and remove duplications
lookfor = sorted(set(lookfor))

# if not lookfor:
exit

def checkForUpdate(lookfor):
    response = requests.get("https://jexamgroup.blogspot.com")
    heading = re.findall(r"<a(.*?)/a>", str(response.text))
    for h in heading:
        if semester in h:
            paragraphs = re.findall(r"<li>(.*?)</li>", str(response.text))
            for eachP in paragraphs:
                if "Es wird" in eachP:
                    break

                # check for possible online subject
                for subject in lookfor:
                    if subject.lower() in eachP.lower():
                            removable[subject] = eachP
                
                # remove subjects from session.json if subject online found
                for user in sessions.get("sessions"):
                    courses = user['data']['courses']
                    for key, value in removable.items():
                        if key in courses:
                            telegram_bot_sendtext(user['id'], value + " ist online.")
                            courses.remove(key)
                            if not courses:
                                sessions.get("sessions").remove(user)
            with open('sessions.json', 'w') as out:
                json.dump(sessions, out, indent=4)
                
            break

# function to actually send a message to the incoming user
def telegram_bot_sendtext(user, msg):
    send_text = (
        "https://api.telegram.org/bot"
        + BOT_TOKEN
        + "/sendMessage?chat_id="
        + user
        + "&parse_mode=Markdown&text="
        + msg
    )
    
    response = requests.get(send_text)
    return response.json()

try:
    checkForUpdate(lookfor)
# potential error notifaction if bot crashes
except Exception as e:
    me = ""
    error = str(e)
    error = traceback.format_exc()
    telegram_bot_sendtext(me, error)