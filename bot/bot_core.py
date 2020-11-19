#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import requests
import logging

from log_config import logger
logger.debug("test")
import json

from bot_img import main as getImage
from bot_response import createResponse as getAnswer
import urllib, urllib2


BOT_TOKEN = "634125151:AAGhQrOStKmo4nA1skOZWHYkcWWrRonbIas"
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
def respond(message):
    params = getAnswer(message)
    response = requests.get(URL + "sendMessage", params = params)
    logging.debug(response.text)
    return response

if __name__ == "__main__":

    logging.debug('Telegram bot module run.')