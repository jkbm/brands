#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
from bot_db import DBHelper
from bot_img import main as getImage
from bot_movie import getMovie
from nltk.stem.snowball import SnowballStemmer
from random import randint
import logging
import json
import time
import unicodedata as ud


latin_letters= {}

symbols = (u"абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
           u"abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA")

path = "/home/jekabm/mysite/bot/"


#tr = {ord(a):ord(b) for a, b in zip(*symbols)}
# for Python 2.*:
tr = dict( [ (ord(a), ord(b)) for (a, b) in zip(*symbols) ] )
key_words = ['cupcake', 'cake', 'muffin', u"капкейк", u"торт", u"кекс"]
flavours = ['chocolate', 'vanila', 'blueberry']
heys = ["hey", "hello", "hi", "greetings", u"привет"]
images = ['cat', 'cats', 'meme']
name = 'username'
general_answers = ["Здравствуй, {0}, чудная сегодня погода, не правда ли?".format(name), "Он принёс три кармана:Первый карман – с пирогами,Второй карман – с орехами…", "А где щи, там и ищи.", "А дело бывало — и коза волка съедала.", "Без складу по складам, без толку по толкам.",
"Февраль богат снегом, апрель -водою.", "Проснитесь и пойте, морпехи! День в морской пехоте - кусочек счастья. Каждая еда - банкет. Каждая выплата - состояние. Каждое построение - парад. Не служба - праздник!", "Ты выглядишь так, как я себя чувствую.",
"Они лезут из стен! Из этих чёртовых стен!", "Хемингуэй когда-то сказал: «Мир — это прекрасное место. И за него стоит бороться». Со второй фразой я согласен.", "Ты хочешь быть лучше всех. Но людям не нужен герой, они хотят есть чизбургеры, играть в лотерею и смотреть телевизор.",
"Люди всё время меня спрашивают: знаю ли я Тайлера Дёрдена?", "Я обрёл свободу. Свобода есть утрата всяческих надежд",
"Просыпаешься… в самолёте. Где — в Лос-Анжелесе, в Сан-Франциско? Просыпаешься… в Далласе, в Фортворде. Где бы ты ни был, где-то в Центральных штатах, — это твоя жизнь, и с каждой минутой она подходит к концу. Если можно проснуться в другом времени, и в другом месте, нельзя ли проснуться другим человеком?",
"Простите, у вас тут можно приземлиться?"]
order = {}

def createResponse(message):
    db = DBHelper()
    settings = open(path + 'bot_settings.json', 'r')
    jsettings = json.load(settings)
    settings.close()

    stemmer2 = SnowballStemmer("russian", ignore_stopwords=True)
    stemmed = []

    chat = message['chat']
    name = chat['first_name'].encode('utf-8')
    user = message['from']

    try:
        last_name = chat['last_name']
        full_name = "{0} {1}".format(name, chat['last_name'].encode('utf-8'))
    except:
        full_name = "{0}".format(name)
        chat['last_name']=""

    try:
        text = message['text']
        if only_roman_chars(text) == False:
            text = text.translate(tr)
            print text
    except Exception as e:
        text = message['text'] = "NO TEXT: %s" % e

    answer = general_answers[randint(0,len(general_answers))] #GENERAL GREETING

    for word in text:
        stemmed.append(stemmer2.stem(word))

    words = text.lower().split()

    for key in key_words:
        if key in words:
            order['type'] = key
            break
        else:
            logging.debug('Nope')
    ctime = time.strftime('%Y-%m-%d %H:%M:%S') #current time

    try:
        last_name = user['last_name']
    except:
        user['last_name'] = "last name undefiend"

    db.add_item(text, user['id'], ctime)
    db.add_user(user)

    words = text.lower().split() #break text into words
    for key in key_words:
        if key in words:
            order['type'] = key
            break
        else:
            logging.debug('Nope')
    for taste in flavours:
        if taste in words:
            order['taste'] = taste
            break

    for key in key_words:
        if key in words:
            logging.debug(key)
            answer = "Вы хотите заказать {0}?".format(key.encode('utf-8'))
            logging.debug(key)
        else:
            logging.debug('Nope')

    if message['text'].lower() in heys:
        answer = "Hey, %s!" % full_name

    params = {'chat_id' : chat['id'], 'text' : answer} #answer parameters dictionary


    #command response
    if text.startswith("/"):
        params['text'] = commandResponse(text, chat, db)
    #question response
    if '?' in text:
        params['text'] = 'I got your question, {0}.'.format(chat['first_name'].encode('utf-8'))

    #MEME
    if 'meme' in text.lower() and jsettings['memegen'] == True:
        img = getImage(text)
        params['text'] = img['link']
        #requests.get(URL + 'sendPhoto', data=data, files=files)
    elif 'meme' in text:
        params['text'] = "Your memes are off. Type '/meme 1' to turn them on."

    #CATS
    if 'cat' in words and jsettings['catsgen'] == True:
        img = getImage(text)
        params['text'] = img['link']
        #requests.get(URL + 'sendPhoto', data=data, files=files)
    elif 'cat' in words:
        params['text'] = "Your cats are asleep. Type '/cats 1' to wake them up."


    #MOVIE
    if 'movie' in text.lower():
        query = text.replace('movie','')
        movie = getMovie(query)
        params['text'] = '<b>{0}</b>  \nRelease date: {1} \n    {2} \n https://image.tmdb.org/t/p/w500{3}'.format(movie['title'], movie['release_date'], movie['overview'].encode('utf-8').strip(), movie['poster_path'])
        params['parse_mode'] = 'HTML'

    #WebPage visit
    if text == "Chicken soup.":
        params['text'] = "Someone visited the web page. Kick them out!"

    return params


#Select response for a command message
def commandResponse(text,chat,db):
    jcmnds = open(path + 'bot_commands.json', 'r')
    cmnds = json.load(jcmnds)
    jcmnds.close()
    settings = open(path + 'bot_settings.json', 'r')
    jsettings = json.load(settings)
    settings.close()

    if text == "/start":
        name = "{0} {1}".format(chat['first_name'].encode('utf-8'), chat['last_name'].encode('utf-8'))
        db.add_conversation(chat['id'], name)
        answer = u"Greeting fellow traveller of the virtual galaxy of the Internet. I'm JKBMbot of JKBM inn, here to assist you. {0}. Use /help to get to know me.".format(u"\U0001F603")
    elif text == "/help": answer = "This is a movie bot. Type a name of a movie + 'movie' to use it."
    elif text == "/meme 1":
        jsettings['memegen'] = True
        with open(path + "bot_settings.json", "w") as jsonFile:
            jsonFile.write(json.dumps(jsettings))
        answer = cmnds[text]
    elif text == "/meme 0":
        jsettings['memegen'] = False
        with open(path + "'bot_settings.json", "w") as jsonFile:
            jsonFile.write(json.dumps(jsettings))
        answer = cmnds[text]
    elif text == "/cats 1":
        jsettings['catsgen'] = True
        with open(path + "bot_settings.json", "w") as jsonFile:
            jsonFile.write(json.dumps(jsettings))
        answer = cmnds[text]
    elif text == "/cats 0":
        jsettings['catsgen'] = False
        with open(path + "bot_settings.json", "w") as jsonFile:
            jsonFile.write(json.dumps(jsettings))
        answer = cmnds[text]
    else:
        answer = cmnds['else']

    return answer


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
