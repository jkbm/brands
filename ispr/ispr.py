#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
from sklearn.externals import joblib
import numpy as np


def get_answer(data, file):
    print data

    clf = joblib.load(file)
    answer = clf.predict(data.reshape(1, -1))
    with open("results.txt", "a") as myfile:
        myfile.write(answer)

    return answer

if __name__ == "__main__":
    data = np.loadtxt('/home/jekabm/mysite/ispr/test1.txt')
    file = "/home/jekabm/mysite/ispr/SVM.pkl"
    data = np.array(['31', '4', '13', '2','4', '10', '0','14084','0','1', '50', '3'])
    print len(data)
    one = get_answer(data, file)
    if one[0] == 0:
        one = ">=50k"
    print one

