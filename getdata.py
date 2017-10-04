import operator
from itertools import islice




def wordsplit(text, words, worddict):
    for word in words:
            if word.lower() in worddict:
                worddict[word.lower()] = worddict[word.lower()] + 1
            else:
                worddict[word.lower()] = 1


def getdata(file):
    file = open('/home/jekabm/mysite/files/'+file+'.csv', 'r')
    wordfile = open('words.csv', 'w')
    worddict = {'a': 0}
    words = file.read().split()
    wordsplit(words, words, worddict)
    sortdict =  sorted(worddict.items(), key=operator.itemgetter(1), reverse=True)
    cleanword = {}
    for word in worddict:
        if '\\' not in word.lower():
            cleanword[word] = worddict[word]

    sortdict =  sorted(cleanword.items(), key=operator.itemgetter(1), reverse=True)

    sortdict=[x for x in sortdict if len(x[0])>4 and x[1] > 50]

    top =  dict(islice(sortdict, 7))

    names = list(sorted(top, key=top.get))
    nums = list(sorted(top.values()))
    data = [names,nums]
    return data

def gettextdata(text):
    worddict = {'a': 0}
    words = text.split()
    wordsplit(words, words, worddict)
    sortdict =  sorted(worddict.items(), key=operator.itemgetter(1), reverse=True)
    cleanword = {}
    for word in worddict:
        if '\\' not in word.lower():
            cleanword[word] = worddict[word]

    sortdict =  sorted(cleanword.items(), key=operator.itemgetter(1), reverse=True)

    sortdict=[x for x in sortdict if len(x[0])>4 and x[1] > 50]

    top =  dict(islice(sortdict, 7))

    names = list(sorted(top, key=top.get))
    nums = list(sorted(top.values()))
    data = [names,nums]
    return data
