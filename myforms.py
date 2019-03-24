#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, RadioField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Required


class LoginForm(Form):
    SECRET_KEY='LUL'
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class NewResearch(Form):
    SECRET_KEY='LUL'
    name = StringField('search', validators=[DataRequired()])
    search = StringField('search', validators=[DataRequired()])
    number = IntegerField('number', validators=[DataRequired()])
    radio =  RadioField('radio', choices=[('one','Stream'),('two','History')], coerce=unicode)
    location = StringField('location', validators=[DataRequired()], default='USA')
    params = StringField('params', validators=[DataRequired()], default='None')

class ISPR(Form):
    SECRET_KEY = 'LUL'
    method = SelectField(u'Method', choices = [('1', u'Наївний баєсів класифікатор'), ('2',  u'Нейронна мережа'), ('3',  u'Метод опорних векторів')])
    age = IntegerField('age', validators=[DataRequired()])
    workclass = SelectField(u'Робочий клас', choices = [('0', u'Приватний підприємець'), ('1', u'Самозайнятість'), ('2', u'ФОП'), ('3', u'Федеральні органи влади'), ('4', u'Місцеві органи влади'), ('5', u'Державні органи влади'), ('6', u'Волонтерство'), ('7', u'Без досвіду роботи')])
    education = SelectField(u'Освіта', choices = [('0', u'Бакалаврат'), ('1', u'Коледж'), ('2', u'Середня освіта'), ('3', u'Закінчена середня освіта - 11 класів'), ('4', u'Професійні курси'), ('5', u'Академічна освіта'), ('6', u'Професійно-технічна освіта'), ('7',u'Середня освіта - 9 класів'), ('8',u'Середня освіта - 7-8 класів'), ('9', u'Закінчена середня освіта - 12 класів'), ('10', u'Магістратура'), ('11', u'Закінчена початкова школа'), ('12', u'Середня освіта - 10 класів'), ('13', u'Докторантура'), ('14', u'Середня освіта - 5-6 класів'), ('15', u'Без освіти')])
    occupation = SelectField(u'Вид діяльності', choices = [('0', u'Технічна підтримка'), ('1', u'Ремонтні послуги'), ('2', u'Сфера послуг'), ('3', u'Продаж'), ('4', u'Менеджмент'), ('5', u'Prof-specialty'), ('6', u'Прибиральні послуги'), ('7', u'Автомобільні послуги'), ('8', u'Клерк'), ('9', u'Фермерство'), ('10', u'Логістика'), ('11', u'Послуги допомоги по господарству'), ('12', u'Охоронні послуги')])
    sex = SelectField(u'Стать', choices = [('0', u"Жіноча"), ('1', u"Чоловіча")])
    hoursPerWeek = IntegerField('hoursPerWeek', validators=[DataRequired()])
    submit = SubmitField("Submit")

class ISPR2(Form):
    SECRET_KEY = 'LUL'
    method = SelectField(u'Method', choices = [('1', u'Наївний баєсів класифікатор'), ('2',  u'Нейронна мережа'), ('3',  u'Метод опорних векторів')])
    msgs = IntegerField('age', validators=[DataRequired()])
    followers = IntegerField('age', validators=[DataRequired()])
    likes = IntegerField('age', validators=[DataRequired()])
    goodmsgs = IntegerField('age', validators=[DataRequired()])
    sex = SelectField(u'Стать', choices = [('0', u"Жіноча"), ('1', u"Чоловіча")])
    submit = SubmitField("Submit")

class ISPR3(Form):
    SECRET_KEY = 'LUL'
    method = SelectField(u'Method', choices = [('1', u'Наївний баєсів класифікатор'), ('2',  u'Нейронна мережа'), ('3',  u'Метод опорних векторів')])
    model1 = SelectField(u'Результат моделі №1', choices = [('0', u"Нерентабельна продукція"), ('1', u"Рентабельна продукція")])
    model2 = SelectField(u'Результат моделі №2', choices = [('0', u"Нерентабельна продукція"), ('1', u"Рентабельна продукція")])
    model3 = SelectField(u'Результат моделі №3', choices = [('0', u"Нерентабельна продукція"), ('1', u"Рентабельна продукція")])
    model4 = SelectField(u'Результат моделі №4', choices = [('0', u"Нерентабельна продукція"), ('1', u"Рентабельна продукція")])
    costprice = IntegerField('costprice', validators=[DataRequired()])
    price = IntegerField('price', validators=[DataRequired()])
    demand = IntegerField('demand', validators=[DataRequired()])
    submit = SubmitField("Submit")