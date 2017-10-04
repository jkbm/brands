#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from flask import Flask, render_template, flash, redirect, request, jsonify, abort
from flask_sslify import SSLify
from flask_login import LoginManager, login_user

from db import adduser, connection, addtwits, checkresearch
import getdata
import twitter.twitter  as tlive
import twitter.twitrest as trest
import myforms
import multiprocessing
import requests
import analytics
from ispr.ispr import get_answer
import numpy as np
import bot.bot_core as bot_core

import json
import logging


logging.basicConfig(level=logging.DEBUG)


app = Flask(__name__)
login_manager = LoginManager()
app.secret_key = 'many random bytes'
sslify = SSLify(app)
login_manager.init_app(app)

@app.route('/')
def hello_world():
    return render_template('index.html',
                       title='Home')


@app.route('/index')
def index():
    return render_template('index.html',
                           title='Home')


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = myforms.LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(user)

        flash('Logged in successfully.')

        next = request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        if not is_safe_url(next):
            return abort(400)

        return redirect('/index')
    return render_template('login.html', form=form)

@app.route('/tflash')
def tflash():
    flash('wazzzzuuuuup')
    return render_template('tflash.html')


"""
***
Visualize data here
***
"""
@app.route('/chart')
def chart():
    research =  request.args.get('research')
    analytics.wordFreq(research)

    #GETDATA
    anlysis_file = open('/home/jekabm/mysite/analysis_data.json', 'r')
    jdata = json.load(anlysis_file)
    anlysis_file.close()
    max_data = 0
    for item in jdata:
        if jdata[item] > max_data:
            max_data = jdata[item]
    #CREATE CHART OF DATA
    return render_template("chart.html", jdata=jdata, max_data = max_data)


@app.route('/register')
def reg():
    adduser()
    flash('wazzup')
    return render_template("register.html")


"""
***
Add new Research - stream or REST
***
"""
@app.route('/newresearch', methods=['GET', 'POST'])
def Research():
    form = myforms.NewResearch()
    resid = checkresearch()
    if form.validate_on_submit():
        resid = checkresearch()
        if form.radio.data == 'two':
            done = trest.rest(form.search.data, form.number.data, form.name.data)

            n = 0
            for x in range(0,len(done)):
                addtwits(done[x][2],resid,done[x][6],done[x][0],done[x][7])
                n += 1

            res = '/dresults?research='+str(resid)+''
            return redirect(res)
        else:
            download_process = multiprocessing.Process(target = tlive.stream,
            args=(form.name.data,form.search.data,int(form.number.data), resid))
            download_process.start()

            #twitter.stream(form.name.data,form.search.data,int(form.number.data), resid)
            flash(' Name: %s; search" %s"; Number:" %s"; Method: %s' %
              (form.name.data, form.search.data, form.number.data, form.radio.data,))
            res = '/dresults?research='+str(resid)+''


            return redirect(res)

    return render_template('newresearch.html',
                           title='New Research',
                           form=form,
                           resid = str(resid)
                           )

@app.route('/newresearch_en', methods=['GET', 'POST'])
def Research_en():
    form = myforms.NewResearch()
    resid = checkresearch()
    if form.validate_on_submit():
        resid = checkresearch()
        if form.radio.data == 'two':
            done = twitrest.rest(form.search.data, form.number.data, form.name.data)

            n = 0
            for x in range(0,len(done)):
                addtwits(done[x][2],resid,done[x][6],done[x][0],done[x][7])
                n += 1

            res = '/dresults?research='+str(resid)+''
            return redirect(res)
        else:
            download_process = multiprocessing.Process(target = tlive.stream,
            args=(form.name.data,form.search.data,int(form.number.data), resid))
            download_process.start()

            #tlive.stream(form.name.data,form.search.data,int(form.number.data), resid)
            flash(' Name: %s; search" %s"; Number:" %s"; Method: %s' %
              (form.name.data, form.search.data, form.number.data, form.radio.data,))
            res = '/dresults?research='+str(resid)+''


            return redirect(res)

    return render_template('newresearch_en.html',
                           title='New Research',
                           form=form,
                           resid = str(resid)
                           )


"""
***
Raw results of tweets
***
"""
@app.route('/results')
def res():
    names = [] #Tweet authors
    data = [] #Tweet texts
    research = request.args.get('research')
    if research == None:
        c, conn = connection()
        c.execute('SELECT count(*) FROM Research;')
        req = c.fetchone ()
        for row in req:
            research = row


    c, conn = connection()
    c.execute('SELECT * FROM Response WHERE Research_id = "'+research+'";')
    dat = c.fetchall ()

    #Form data array of tweettexts
    for x in dat:
        c.execute('SELECT Screen_name FROM user WHERE id = '+str(x[2])+';')
        name = c.fetchall()
        x = list(x)
        x[4] = str(name).replace('(("',"").replace(',),)', "").replace('"', "").replace("'", "")
        data.append(x)

    c.close()
    conn.close()

    return render_template("results.html",
                            data=data,
                            names=names)


"""
***
Show results for live stream Research
***
"""
@app.route('/dresults')
def dres():
    research = request.args.get('research')
    if research == None:
        c, conn = connection()
        c.execute('SELECT count(*) FROM Research;')
        req = c.fetchone ()
        for row in req:
            research = row
        print research

    return render_template("dynamicresults.html", res = research)


@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)


@app.route('/_add_twit')
def add_twit():

    return jsonify(twit)


"""
***
TeleBot home: setup WebHook and process requests
***
"""
@app.route('/telebot',methods=['GET','POST','OPTIONS'])
def telebot():
    BOT_TOKEN = "294249200:AAEsVNT9AIb8c__rv07ifOP-r9eCKJfeON8"
    myurl = "https://jekabm.pythonanywhere.com/telebot"
    URL = "https://api.telegram.org/bot%s/" % BOT_TOKEN
    f = open('posts.txt', 'a')
    r = ""
    """ set up WebHook
    try:
        r = requests.get(URL + "setWebhook?url=%s" % myurl)
        #r = requests.get(URL + "deleteWebhook")
        #r = requests.get(URL +"getWebhookInfo")
        if r.status_code != 200:
            logging.error("Can't set hook: %s. Quit." % r.text)
        else:
            logging.debug(r.text)
        print "WEBHOOK RESPONSE:" + str(r.json())

    except Exception as e:
        logging.error("There was an error setting up WebHook: %s" % e)
    r = r.json()
    """
    jdata = '{"update_id":273032929, "message":{"message_id":48,"from":{"id":289232696,"first_name":"Evgeniy","last_name":"Beardear"},"chat":{"id":289232696,"first_name":"Evgeniy","last_name":"Beardear","type":"private"},"date":1479225848,"text":"Chicken soup."}}'

    data = request.data
    if data:
        jdata = str.join(" ", data.splitlines())
        f.write(jdata)
        try:
            jdata = json.dumps(json.JSONDecoder().decode(jdata))
        except Exception as e:
            jdata = '{"update_id":273032929, "message":{"message_id":48,"from":{"id":289232696,"first_name":"Evgeniy","last_name":"Beardear"},"chat":{"id":289232696,"first_name":"Evgeniy","last_name":"Beardear","type":"private"},"date":1479225848,"text":"'+str(e)+'"}}'
            jdata = json.dumps(json.JSONDecoder().decode(jdata))

        try:
            jdata = json.loads(jdata)
            jdata = jdata['message']
        except Exception as e:
            jdata = "NO WAY: %s" % e

        bot_core.Respond(jdata)

    return render_template("telebot.html", message=jdata)


@app.route('/bot')
def bot():

    return render_template('bot.html')

@app.route('/ispr', methods=['GET', 'POST'])
def ispr():

    file = "/home/jekabm/mysite/ispr/SVM.pkl"
    form = myforms.ISPR()

    if form.validate_on_submit():
        if form.method == 1:
            file = "/home/jekabm/mysite/ispr/GNB.pkl"
        elif form.method == 2:
            file = "/home/jekabm/mysite/ispr/NEU.pkl"
        else:
            file = "/home/jekabm/mysite/ispr/SVM.pkl"

        form_data = [form.age.data, form.workclass.data, form.education.data, 2, 4, form.occupation.data, 5, form.sex.data, 10000.0, 1, form.hoursPerWeek.data, 5]
        ispr_data = np.array(form_data)
        #ispr_data = ispr_data.astype(float)
        #ispr_data = np.loadtxt('/home/jekabm/mysite/ispr/test1.txt')
        answer = get_answer(ispr_data, file)
        if answer[0] == 0:
            flash_text = '<=50'
        else:
            flash_text = 'Answer: >50'
        flash_text = flash_text.decode("utf-8")
        flash(flash_text)
        return redirect('/ispr')


    return render_template('ispr.html', form = form)

@app.route('/ispr2', methods=['GET', 'POST'])
def ispr2():
    file = "/home/jekabm/mysite/ispr/SVM.pkl"
    form = myforms.ISPR2()

    if form.validate_on_submit():
        form_data = [form.age.data, form.workclass.data, form.education.data, form.occupation.data, form.sex.data, 10000.0, 1, form.hoursPerWeek.data]
        ispr_data = np.array(form_data)
        ispr_data = ispr_data.astype(float)
        answer = get_answer(ispr_data, file)
        if answer[0] == 0:
            flash_text = '<=50'
        else:
            flash_text = 'Answer: >50'
        flash_text = flash_text.decode("utf-8")
        flash(flash_text)
        return redirect('/ispr2')

    return render_template('ispr2.html', form = form)


@app.route('/ispr3', methods=['GET', 'POST'])
def ispr3():
    file = "/home/jekabm/mysite/ispr/SVM.pkl"
    form = myforms.ISPR3()

    if form.validate_on_submit():
        form_data = [form.age.data, form.workclass.data, form.education.data, form.occupation.data, form.sex.data, 10000.0, 1, form.hoursPerWeek.data]
        ispr_data = np.array(form_data)
        ispr_data = ispr_data.astype(float)
        answer = get_answer(ispr_data, file)
        if answer[0] == 0:
            flash_text = '<=50'
        else:
            flash_text = 'Answer: >50'
        flash_text = flash_text.decode("utf-8")
        flash(flash_text)


        return redirect('/ispr2')


    return render_template('ispr_Stasy.html', form = form)


@app.route('/temp')
def temp():
    data = '\u041c\u043e\u0443\u0440\u0438\u043d\u044c\u043e \u043f\u0440\u0438\u0437\u043d\u0430\u043b\u0441\u044f, \u0447\u0435\u043c \u0435\u0433\u043e \u0443\u0434\u0438\u0432\u0438\u043b "\u0427\u0435\u043b\u0441\u0438'
    return render_template('temp.html', data = str(data).decode('utf-8'))
