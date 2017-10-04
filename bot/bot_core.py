#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import requests
import logging
logging.basicConfig(level = logging.DEBUG)
import json

from bot_img import main as getImage
from bot_response import createResponse as Answer
import urllib, urllib2


BOT_TOKEN = "294249200:AAEsVNT9AIb8c__rv07ifOP-r9eCKJfeON8"
URL = "https://api.telegram.org/bot%s/" % BOT_TOKEN
MyURL = "http://jekabm.pythonanywhere.com/telebot"

session = requests.Session()



"""def setWebHook(URL):
    try:
        wh = requests.get(URL+"setWebhook?url=%s" + MyURL)
        if set_hook.status_code != 200:
            logging.error("Can't set hook: %s. Quit." % set_hook.text)
            exit(1)"""



#MAIN

def Respond(message):
    params = Answer(message)
    sent = requests.get(URL + "sendMessage", params = params)
    return sent


def sendAnswer(message):
    try:
        utf = message['text'].encode("utf8")
        answer = "Hey, {0}, what's up? You said: {1}, right?".format(message['from']['first_name'], utf)
    except Exception as e:
        logging.error("Can't decode: %s" % e)
        answer = "Nope"

    params = {'chat_id': message['from']['id'], 'text': answer}

    sent = requests.get(URL + "sendMessage", params = params)
    logging.debug(sent.status_code)

#sendAnswer(message)

if __name__ == "__main__":

    logging.debug('File run')