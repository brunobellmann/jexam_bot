#!/usr/bin/env python
# coding: utf8

import urllib.request
import sched
import time
import requests
import re
import json

import os
import sys
from os.path import getmtime

with open('config.json') as json_data_file:
    data = json.load(json_data_file)

bot_token = data.get("bot_token")

def telegram_bot_sendtext(user, msg):
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + user + '&parse_mode=Markdown&text=' + msg
    response = requests.get(send_text)
    return response.json()

# potential debug notification
telegram_bot_sendtext('', 'started')

def checkForUpdate(lookfor):
    url = 'http://jexamgroup.blogspot.com'
    testsonline = []
    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req)
    respData = resp.read()
    heading = re.findall(r'<a(.*?)/a>', str(respData))
    for h in heading:
        if data.get("semester") in h: 
            paragraphs = re.findall(r'<li>(.*?)</li>',str(respData))
            for eachP in paragraphs:
                if "Es wird" in eachP:
                    break

                eachP = eachP.replace('&nbsp;', '')
                eachP = eachP.replace('\\xc3\\xbc', 'ü')
                eachP = eachP.replace('\\xc3\\xa4', 'ä')
                eachP = eachP.replace('\\xc3\\xb6', 'ö')
                testsonline.append(eachP)

    bot_chatIDs = data.get("chatIds")
    lookfortests = lookfor
    for user in bot_chatIDs:
        for item in lookfortests:
            for itemx in testsonline:
                if item in itemx:
                    telegram_bot_sendtext(user ,itemx + ' ist online.')
                    lookfortests.remove(item) 

    lookfor = lookfortests
    
    editFile = open("modules.txt", "w")
    editFile.write( "\n".join( lookfor ) )
    editFile.close()

    time.sleep(600)

while True:
    modules = open("modules.txt", "r")
    lookfor = modules.read().splitlines()
    modules.close()

    try:
        checkForUpdate(lookfor)
    # potential error notifaction if bot crashes
    except:
        me = ''
        error = 'ERROR!'
        telegram_bot_sendtext(me , error)