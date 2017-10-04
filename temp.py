#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
from db import connection as con
import json


def get_data(res_num):
    c, conn = con()
    c.execute('SELECT Text FROM Response WHERE Research_id = '+str(res_num)+';')

    data = c.fetchall()

    return data

def popularWords(tweets):
    string = ""
    for x in tweets:
        string += str(x)

    words = string.split()
    worddict = {'a': 0}

    import operator
    from itertools import islice

    def wordsplit(text):
        for word in words:
            if word.lower() in worddict:
                worddict[word.lower()] = worddict[word.lower()] + 1
            else:
                worddict[word.lower()] = 1


    wordsplit(words)


    sortdict =  sorted(worddict.items(), key=operator.itemgetter(1), reverse=True)



    cleanword = {}
    for word in worddict:
        if '\\' not in word.lower() and '@' not in word.lower() and '&' not in word.lower():
            if '#' not in word.lower():
                cleanword[word] = worddict[word]

    sortdict =  sorted(cleanword.items(), key=operator.itemgetter(1), reverse=True)
    print [x for x in sortdict if len(x[0])>4 and x[1] > 20]
    print('')
    sortdict=[x for x in sortdict if len(x[0])>4 and x[1] > 20]
    top =  dict(islice(sortdict, 10))

    names = list(sorted(top, key=top.get))
    nums = list(sorted(top.values()))
    print names
    print nums

    top_dict = {}
    for n in range(0, len(names)):
        top_dict[names[n]] =  nums[n]
    print top_dict
    for item in top_dict:
        print top_dict[item]
    with open("/home/jekabm/mysite/analysis_data.json", "w") as jsonFile:
            jsonFile.write(json.dumps(top_dict))

tweets = get_data(59)
popularWords(tweets)


