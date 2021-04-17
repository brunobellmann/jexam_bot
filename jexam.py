#!/usr/bin/env python
# coding: utf8

import requests
import re
import json
import traceback
from dotenv import load_dotenv
import os
from datetime import date
from bs4 import BeautifulSoup
import time

# get environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
UPDATE_INTERVAL = os.getenv("UPDATE_INTERVAL")

# function to actually send a message to an user
def telegram_bot_sendtext(user: str, msg: str):
    send_text = (
        "https://api.telegram.org/bot"
        + BOT_TOKEN
        + "/sendMessage?chat_id="
        + user
        + "&parse_mode=Markdown&text="
        + msg
    )
    requests.get(send_text)


def getSemester():
    # get current date for scope
    today = date.today()

    # set wintersemester range
    winterStart = (2, 1)
    winterEnd = (6, 1)

    # set sommersemester range
    sommerStart = (7, 1)
    sommerEnd = (11, 1)

    # check for semester
    if winterStart < (today.month, today.day) < winterEnd:
        currentyear = today.strftime("%Y")
        lastyear = int(currentyear) - 1
        return "Wintersemester " + str(lastyear) + "/" + str(currentyear)
    elif sommerStart < (today.month, today.day) < sommerEnd:
        return "Sommersemester " + year
    else:
        raise Exception("Error while calculating semester")


def getLookForModules(sessions) -> [str]:
    lookfor = []
    for user in sessions["sessions"]:
        for c in user["courses"]:
            lookfor.append(c)
    return lookfor

def checkForUpdate(lookfor):
    removable = {}
    semester_elem = {}
    response = requests.get("https://jexamgroup.blogspot.com")
    soup = BeautifulSoup(response.text, "html.parser")
    entries = soup.find_all("div", "date-outer")
    for item in entries:
        semester_text = item.find(string=re.compile(semester))
        if semester_text is not None:
            semester_elem = item
    if semester_elem == {}:
        raise Exception("HTML Element with current semester couldn't be found.")
    paragraphs = re.findall(r"<li>(.*?)</li>", str(semester_elem))
    # check for possible online subject
    for eachP in paragraphs:
        for subject in lookfor:
            if subject.lower() in eachP.lower():
                removable[subject] = eachP

        # remove subjects from session.json if subject online found
        for user in sessions.get("sessions"):
            courses = user["courses"]
            for key, value in removable.items():
                if key in courses:
                    replacedString = value.replace("<br/>", "")
                    telegram_bot_sendtext(user["id"], replacedString + " ist online.")
                    courses.remove(key)
                    if not courses:
                        sessions.get("sessions").remove(user)
    with open("usersessions.json", "w") as out:
        json.dump(sessions, out, indent=4)
    return


# Start loop
while True:
    try:
        semester = getSemester()

        sessions = {}

        with open("usersessions.json") as json_data_file:
            sessions = json.load(json_data_file)

        lookfor = getLookForModules(sessions)
        # sort and remove duplications
        lookfor = sorted(set(lookfor))
        if lookfor != []:
            checkForUpdate(lookfor)
    except Exception:
        traceback.print_exc()
        me = ADMIN_ID
        error = traceback.format_exc()
        telegram_bot_sendtext(me, error)
    time.sleep(int(UPDATE_INTERVAL))
