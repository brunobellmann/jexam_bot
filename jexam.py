# coding: utf8

import requests
import re
import json

with open("config.json") as json_data_file:
    data = json.load(json_data_file)

lookfor = data.get("modules")

if not lookfor:
    exit


def telegram_bot_sendtext(user, msg):

    bot_token = data.get("bot_token")
    send_text = (
        "https://api.telegram.org/bot"
        + bot_token
        + "/sendMessage?chat_id="
        + user
        + "&parse_mode=Markdown&text="
        + msg
    )
    requests.get(send_text)
    return


response = requests.get("https://jexamgroup.blogspot.com")
heading = re.findall(r"<a(.*?)/a>", str(response.text))
for h in heading:
    if data.get("semester") in h:
        paragraphs = re.findall(r"<li>(.*?)</li>", str(response.text))
        for eachP in paragraphs:
            if "Es wird" in eachP:
                break

            for subject in lookfor:
                if subject in eachP:
                    bot_chatIDs = data.get("chatIds")
                    for user in bot_chatIDs:
                        telegram_bot_sendtext(user, eachP + " ist online.")
                    lookfor.remove(subject)
                    data["modules"] = lookfor
                    json.dump(data, open("config.json", "w"), indent=4)
                    break

