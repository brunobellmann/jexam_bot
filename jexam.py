# coding: utf8

import urllib.request
import sched
import time
import requests
import re

lookfor = []

def telegram_bot_sendtext(user, msg):
    
    bot_token = ''
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + user + '&parse_mode=Markdown&text=' + msg

    response = requests.get(send_text)
    return response.json()

def checkForUpdate():
    url = 'http://jexamgroup.blogspot.com'
    testsonline = []
    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req)
    respData = resp.read()
    heading = re.findall(r'<a(.*?)/a>', str(respData))
    for h in heading:
        if "" in h: 
            paragraphs = re.findall(r'<li>(.*?)</li>',str(respData))
            for eachP in paragraphs:
                if "Es wird" in eachP:
                    break

                eachP = eachP.replace('&nbsp;', '')
                eachP = eachP.replace('\\xc3\\xbc', 'ü')
                eachP = eachP.replace('\\xc3\\xa4', 'ä')
                eachP = eachP.replace('\\xc3\\xb6', 'ö')
                testsonline.append(eachP)

    bot_chatIDs = ['']
    for user in bot_chatIDs:
        for item in lookfor:
            for itemx in testsonline:
                if item in itemx:
                    telegram_bot_sendtext(user ,itemx + ' ist online.')
                    lookfor.remove(item)
    time.sleep(600)

while True:
    checkForUpdate()