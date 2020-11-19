import json
from random import randint

from bot_img import main as getImage
from bot_movie import getMovie
from constants import GENERAL_ANSWERS

# TODO move to config
path = "/home/jekabm/mysite/bot/"
with open(path + 'bot_settings.json', 'r') as settings:
    jsettings = json.load(settings)
def get_meme_response(params):
    #MEME
    if jsettings['memegen'] == True:
        img = getImage(params['input_text'])
        params['text'] = img['link']
        #requests.get(URL + 'sendPhoto', data=data, files=files)
    else:
        params['text'] = "Your memes are off. Type '/meme 1' to turn them on."
    return params

def get_cat_response(params):
    #CATS
    if jsettings['catsgen'] == True:
        img = getImage(params['input_text'])
        params['text'] = img['link']
        #requests.get(URL + 'sendPhoto', data=data, files=files)
    else:
        params['text'] = "Your cats are asleep. Type '/cats 1' to wake them up."
    return params

def get_movie_response(params):
    #MOVIE
    query = params['input_text'].replace('movie','')
    movie = getMovie(query)
    html_list = [
        '<b>{0}</b>'.format(movie['title']),
        'Release date: {0}'.format(movie['release_date']),
        '{0}'.format(movie['overview'].encode('utf-8').strip()),
        'https://image.tmdb.org/t/p/w500{0}'.format(movie['poster_path'])
    ]
    params['text'] = "\n".join(html_list)
    params['parse_mode'] = 'HTML'
    return params

def get_default_response(params):
    #WebPage visit
    if params['input_text'] == "Chicken soup.":
        params['text'] = "Someone visited the web page. Kick them out!"
    else:
        params['text'] = GENERAL_ANSWERS[randint(0,len(GENERAL_ANSWERS))] #GENERAL GREETING
    return params

response_functions = {
    "meme": get_meme_response,
    "cat": get_cat_response,
    "movie": get_movie_response,
    "default": get_default_response,
}
class ChatScenarios:
    #Select response for a command message
    @classmethod
    def command_response(cls, text, chat, db):
        with open(path + 'bot_commands.json', 'r') as jcmnds:
            cmnds = json.load(jcmnds)
        with open(path + 'bot_settings.json', 'r') as settings:
            jsettings = json.load(settings)

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
    
    @classmethod
    def fun_response(cls, params):
        """Get function for correct scenario or send generic answer if not found.
        """
        words = params.get("input_text", "").split()
        func = response_functions.get(words[-1], get_default_response)
        return func(params)
