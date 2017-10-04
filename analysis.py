
import operator
from itertools import islice

file = open('ml2.csv', 'r')
wordfile = open('words.csv', 'w')
worddict = {'a': 0}
words = file.read().split()
file.close()
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
    if '\\' not in word.lower():
        cleanword[word] = worddict[word]

sortdict =  sorted(cleanword.items(), key=operator.itemgetter(1), reverse=True)
print [x for x in sortdict if len(x[0])>4 and x[1] > 50]
print('')
sortdict=[x for x in sortdict if len(x[0])>4 and x[1] > 50]
top =  dict(islice(sortdict, 7))

names = list(sorted(top, key=top.get))
nums = list(sorted(top.values()))
print names
print nums

import matplotlib.pyplot as plt

# The slices will be ordered and plotted counter-clockwise.
labels = names
sizes = nums
colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral', 'blue', 'red']
explode = (0, 0, 0, 0, 0.1, 0.1, 0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')

plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=90)
# Set aspect ratio to be equal so that pie is drawn as a circle.

plt.show()
