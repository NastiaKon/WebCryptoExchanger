# -*- coding: utf-8 -*-
from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Kind_operations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    operation_full = db.Column(db.String(32), index=True, unique=True, nullable=False)
    operation_short = db.Column(db.String(16), unique=True, nullable=False)
    ko_transact = db.relationship('Transactions', backref=db.backref('trans'), lazy='dynamic')
    
    def __repr__(self):
        return '<Op:{}>'.format(self.operation_full)

class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    sum_curr = db.Column(db.Float, nullable=True)
    sum_rubl = db.Column(db.Float, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    operation_id = db.Column(db.Integer, db.ForeignKey('kind_operations.id'))
    currency_id = db.Column(db.Integer, db.ForeignKey('kind_currency.id'))
    
    def __repr__(self):
        return ('<trId:%s,TrTm:%s,TrSc:%s,TrSr:%s>'%(self.id,self.timestamp,self.sum_curr,self.sum_rubl))

class Kind_currency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    currency_full = db.Column(db.String(32), index=True, unique=True, nullable=False)
    currency_short = db.Column(db.String(16), unique=True, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    c_course_prodaza = db.Column(db.Float, nullable=False)
    c_course_pokupka = db.Column(db.Float, nullable=False)
    c_course_market = db.Column(db.Float, nullable=False)
    kc_transact = db.relationship('Transactions', backref=db.backref('transact'), lazy='dynamic')

    def __repr__(self):
        return ('<Id:%s,Nm:%s,Prod:%s,Mark:%s,Pokup:%s>'%(self.id,self.currency_full,self.c_course_prodaza,self.c_course_market,self.c_course_pokupka))

class Roles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(12), index=True, unique=True, nullable=False)
    users = db.relationship('User', backref=db.backref('owner'), lazy='dynamic')

    def __repr__(self):
        return ('<Rid:%s,Rt:%s>'%(self.id,self.title))    

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    bank_acc_curr = db.Column(db.String(20), unique=True, nullable=False)
    balance_curr = db.Column(db.String(128), nullable=True, default='0')
    bank_acc_rubl = db.Column(db.String(20), unique=True, nullable=False)
    balance_rubl = db.Column(db.String(128), nullable=True, default='0')    
    descr = db.Column(db.String(64), nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    us_transact = db.relationship('Transactions', backref=db.backref('transs'), lazy='dynamic')
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
#    role_id = db.Column(db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

#    def __repr__(self):
#        return '<User {}>'.format(self.username)
    def __repr__(self):
        return ('<Uid:%s,UN:%s,Em:%s>'%(self.id,self.username,self.email))

@login.user_loader
def load_user(id):
    return User.query.get(int(id))