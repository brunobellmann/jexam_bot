#!/usr/bin/env python
# coding: utf8

import requests
import re
import json
import traceback

modules = open("modules.txt", "r")
lookfor = modules.read().splitlines()
modules.close()
if not lookfor:
    exit

with open("config.json") as json_data_file:
    data = json.load(json_data_file)

bot_token = data.get("bot_token")


def telegram_bot_sendtext(user, msg):
    send_text = (
        "https://api.telegram.org/bot"
        + bot_token
        + "/sendMessage?chat_id="
        + user
        + "&parse_mode=Markdown&text="
        + msg
    )
    response = requests.get(send_text)
    return response.json()


# potential debug notification
telegram_bot_sendtext("", "started")

def checkForUpdate(lookfor):
    response = requests.get("https://jexamgroup.blogspot.com")
    heading = re.findall(r"<a(.*?)/a>", str(response.text))
    semester = data.get("semester")
    bot_chatIDs = data.get("chatIds")
    for h in heading:
        if semester in h:
            paragraphs = re.findall(r"<li>(.*?)</li>", str(response.text))
            for eachP in paragraphs:
                if "Es wird" in eachP:
                    break

                for subject in lookfor:
                    if subject.lower() in eachP.lower():
                        for user in bot_chatIDs:
                            telegram_bot_sendtext(user, eachP + " ist online.")
                            lookfor.remove(subject)
                        break
            break

    editFile = open("modules.txt", "w")
    editFile.write("\n".join(lookfor))
    editFile.close()


try:
    checkForUpdate(lookfor)
# potential error notifaction if bot crashes
except Exception as e:
    me = ""
    error = str(e)
    error = traceback.format_exc()
    telegram_bot_sendtext(me, error)