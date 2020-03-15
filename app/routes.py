# -*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request 
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, Index, EditProfileForm, PokupkaForm, ProdazaForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Roles, Kind_operations, Transactions, Kind_currency

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/')
@app.route('/index')
def index():
#    form = Index()
    vals = Kind_currency.query.all()
    return render_template("index.html", title='Home Page', vals=vals)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Не верный пароль или имя пользователя!")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        r = Roles.query.filter_by(title='Client').first()
        user = User(username=form.username.data, email=form.email.data, \
bank_acc_curr=form.bank_acc_curr.data, bank_acc_rubl=form.bank_acc_rubl.data, owner=r)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/pokupka', methods=['GET', 'POST'])
@login_required
def pokupka():
    form = PokupkaForm()
    if form.validate_on_submit():
#        currency = form.currency_name.data
        currency = form.Вид_валюты.data
        pok = Kind_operations.query.filter_by(operation_short='Покупка').first()
#Обновим баланс пользователя
        kurs_val = (currency.c_course_prodaza / currency.quantity)
        sum_val = round(form.sum_curr.data,2)
#       sum_ru=form.sum_rubl.data
        sum_ru = round(sum_val * kurs_val,2)
        bal_curr = ('+'+str(sum_val)+currency.currency_short+';'+current_user.balance_curr)
        bal_rubl = ('-'+str(sum_ru)+'РУБ;'+current_user.balance_rubl)
        current_user.balance_curr = bal_curr[0:150]
        current_user.balance_rubl = bal_rubl[0:150]
        db.session.commit()
#        print(current_user.id, current_user.balance_curr, current_user.balance_rubl)
        trans = Transactions(sum_curr=form.sum_curr.data, sum_rubl=sum_ru, \
user_id=current_user.id, operation_id=pok.id, currency_id=currency.id)
        db.session.add(trans)
        db.session.commit()
        flash('Вы приобрели: '+str(sum_val)+currency.currency_short+' на сумму: '+str(sum_ru)+'РУБ'\
+' по курсу: '+str(kurs_val)+'. Транзакция прошла успешно.')
        return redirect(url_for('pokupka'))
    return render_template('pokupka.html', title='Buy', form=form)

@app.route('/prodaza', methods=['GET', 'POST'])
@login_required
def prodaza():
    form = ProdazaForm()
    if form.validate_on_submit():
#        currency = form.currency_name.data
        currency = form.Вид_валюты.data
        pok = Kind_operations.query.filter_by(operation_short='Продажа').first()
#Обновим баланс пользователя
        kurs_val = (currency.c_course_pokupka / currency.quantity)
        sum_val = round(form.sum_curr.data,2)
#       sum_ru=form.sum_rubl.data
        sum_ru = round(sum_val * kurs_val,2)
        bal_curr = ('-'+str(sum_val)+currency.currency_short+';'+current_user.balance_curr)
        bal_rubl = ('+'+str(sum_ru)+'РУБ;'+current_user.balance_rubl)
        current_user.balance_curr = bal_curr[0:150]
        current_user.balance_rubl = bal_rubl[0:150]
        db.session.commit()
#        print(current_user.id, current_user.balance_curr, current_user.balance_rubl)
        trans = Transactions(sum_curr=form.sum_curr.data, sum_rubl=sum_ru, \
user_id=current_user.id, operation_id=pok.id, currency_id=currency.id)
        db.session.add(trans)
        db.session.commit()
        flash('Вы обменяли: '+str(sum_val)+currency.currency_short+' на: '+str(sum_ru)+'РУБ'\
+' по курсу: '+str(kurs_val)+'. Транзакция прошла успешно.')
        return redirect(url_for('prodaza'))
    return render_template('prodaza.html', title='Sale', form=form)

@app.route('/history/<username>')
@login_required
def history(username):
    user = User.query.filter_by(username=username).first_or_404()
#    trs = Transactions.query.filter_by(user_id=user.id).all()
    trs = Transactions.query.filter_by(user_id=user.id).order_by(Transactions.timestamp.desc()).all()
    return render_template('history.html', user=user, trs=trs)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username, current_user.email, current_user.bank_acc_curr, current_user.bank_acc_rubl)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bank_acc_curr = form.bank_acc_curr.data
        current_user.bank_acc_rubl = form.bank_acc_rubl.data
        current_user.descr = form.descr.data
        db.session.commit()
        flash('Все изменения зафиксированы.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bank_acc_curr.data = current_user.bank_acc_curr
        form.bank_acc_rubl.data = current_user.bank_acc_rubl
        form.descr.data = current_user.descr
    return render_template('edit_profile.html', title='Edit Profile', form=form)