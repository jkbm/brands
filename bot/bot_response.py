#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import logging
import json
import time
import unicodedata as ud

from nltk.stem.snowball import SnowballStemmer

from bot_db import DBHelper
from constants import HEYS, SYMBOLS
from bot_scenarios import ChatScenarios

latin_letters= {}

#tr = {ord(a):ord(b) for a, b in zip(*symbols)}
# for Python 2.*:
tr = dict( [ (ord(a), ord(b)) for (a, b) in zip(*SYMBOLS) ] )


def createResponse(message):
    if not isinstance(message, dict):
        logging.debug(message)
        return {}
    chat = message['chat']
    name = chat['first_name'].encode('utf-8')
    user = message['from']

    try:
        full_name = "{0} {1}".format(name, chat['last_name'].encode('utf-8'))
    except:
        full_name = "{0}".format(name)
        chat['last_name'] = ""

    try:
        text = message['text']
        if only_roman_chars(text) == False:
            text = text.translate(tr)
    except Exception as e:
        text = message['text'] = "NO TEXT: %s" % e

    """
    stemmer2 = SnowballStemmer("russian", ignore_stopwords=True)
    stemmed = []
    for word in text:
        stemmed.append(stemmer2.stem(word))
    """
    # add db entry
    db = DBHelper()
    ctime = time.strftime('%Y-%m-%d %H:%M:%S') #current time
    db.add_item(text, user['id'], ctime)
    db.add_user(user)
    params = {'chat_id' : chat['id'], 'text' : None, 'input_text': text} #answer parameters dictionary

    # 'hey' response
    if message['text'].lower() in HEYS:
        params['text'] = "Hey, %s!" % full_name

    #command response
    if text.startswith("/"):
        params['text'] = ChatScenarios.command_response(text, chat, db)
        return params
    #question response
    if text.endswith('?'):
        params['text'] = 'I got your question, {0}.'.format(chat['first_name'].encode('utf-8'))
    # special mode
    params = ChatScenarios.fun_response(params)

    return params

def is_latin(uchr):
    try: return latin_letters[uchr]
    except KeyError:
         return latin_letters.setdefault(uchr, 'LATIN' in ud.name(uchr))


def only_roman_chars(unistr):
    return all(is_latin(uchr)
           for uchr in unistr
           if uchr.isalpha())


"""
if message['text'].lower() in heys:
    _id = message['from']['id']
    answer = "Hey!"
    payload = {'chat_id': _id, 'text': answer}
    sticker = {'chat_id': _id, 'sticker': "BQADAgADeAcAAlOx9wOjY2jpAAHq9DUC"}
    smile = {'chat_id': _id, 'text': answer + u" \U00002663"}
    #sent = requests.get(URL + "sendMessage", params = payload)
    #sent = requests.get(URL + "sendSticker", params = sticker)
    #sent = requests.get(URL + "sendMessage", params = smile)
    #print sent
"""
