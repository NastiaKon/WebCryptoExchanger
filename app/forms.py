# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SubmitField, FloatField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User, Roles, Kind_operations, Transactions, Kind_currency

def check_float(f): # Функция проверки, что пользователь ввёл число
    try:
        num = float(f)
        if num <= 0:
            return(0)
        else:
            return num
    except ValueError:
        return(0)
        
def curr_query():
    return Kind_currency.query.order_by(Kind_currency.id.asc()).all()        

class Index(FlaskForm):
    currency_full = StringField('Валюта')
    currency_short = StringField('Обозн.')
    c_course_market = FloatField('Курс ЦБ РФ')
    c_course_prodaza = FloatField('Курс продажи банком')
    c_course_pokupka = FloatField('Курс покупки банком')
    
class PokupkaForm(FlaskForm):
    Вид_валюты = QuerySelectField(query_factory=curr_query, allow_blank=True, \
get_label='currency_full',  blank_text="Выберите из списка...", validators=[DataRequired()])
    sum_curr = FloatField('Сумма в валюте', validators=[DataRequired()])
#    sum_rubl = FloatField('Сумма (руб.)')
#    curr_name = currency_name
    submit = SubmitField('Подтвердить покупку')
    
class ProdazaForm(FlaskForm):
    Вид_валюты = QuerySelectField(query_factory=curr_query, allow_blank=True, \
get_label='currency_full',  blank_text="Выберите из списка...", validators=[DataRequired()])
    sum_curr = FloatField('Сумма в валюте', validators=[DataRequired()])
#    sum_rubl = FloatField('Сумма (руб.)')
#    curr_name = currency_name
    submit = SubmitField('Подтвердить продажу')
    
class LoginForm(FlaskForm):
    username = StringField('Имя пользователя:', validators=[DataRequired()])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Вход')
    
class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя:', validators=[DataRequired()])
    email = StringField('E-mail:', validators=[DataRequired(), Email()])
#---
    bank_acc_curr = StringField('Банковский валючный счет пользователя:', validators=[DataRequired()])
    bank_acc_rubl = StringField('Банковский рублевый счет пользователя:', validators=[DataRequired()])
#---
    password = PasswordField('Введите пароль:', validators=[DataRequired()])
    password2 = PasswordField(
        'Повторите пароль:', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрировать')
            
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        cl_role = Roles.query.filter_by(title='Client').first()
        if user is not None:
            raise ValidationError('Этот пользователь уже зарегистрирован!')
        elif cl_role is None:
            raise ValidationError('В системе не установлена роль Client!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Этот e-mail уже зарегистрирован!')

    def validate_bank_acc_curr(self, bank_acc_curr):
        acc_found = User.query.filter_by(bank_acc_curr=bank_acc_curr.data).first()
        acc_len = len(self.bank_acc_curr.data)
        acc_null = check_float(self.bank_acc_curr.data)
        if acc_found is not None:
            raise ValidationError('Этот валютный счет уже зарегистрирован!')
        elif acc_len != 2:
            raise ValidationError('Cчет должен состоять из 2 числовых символов!')
        elif acc_null == 0:
            raise ValidationError('Cчет должен быть числовым!')
        
        
    def validate_bank_acc_rubl(self, bank_acc_rubl):
        acc_found = User.query.filter_by(bank_acc_rubl=bank_acc_rubl.data).first()
        acc_len = len(self.bank_acc_rubl.data)
        acc_null = check_float(self.bank_acc_rubl.data)
        if acc_found is not None:
            raise ValidationError('Этот рублевый счет уже зарегистрирован!')
        elif acc_len != 2:
            raise ValidationError('Cчет должен состоять из 2 числовых символов!')
        elif acc_null == 0:
            raise ValidationError('Cчет должен быть числовым!')
            
class EditProfileForm(FlaskForm):
    username = StringField('Имя пользователя:', validators=[DataRequired()])
    email = StringField('E-mail:', validators=[DataRequired(), Email()])
    bank_acc_curr = StringField('Банковский валючный счет пользователя:', validators=[DataRequired()])
    bank_acc_rubl = StringField('Банковский рублевый счет пользователя:', validators=[DataRequired()])
    descr = TextAreaField('Немного о себе:', validators=[Length(min=0, max=64)])
    submit = SubmitField('Submit')
    
    def __init__(self, orig_username, orig_email, orig_bank_acc_curr, orig_bank_acc_rubl, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.orig_username = orig_username
        self.orig_email = orig_email
        self.orig_bank_acc_curr = orig_bank_acc_curr
        self.orig_bank_acc_rubl = orig_bank_acc_rubl
        
    def validate_username(self, username):
        if username.data != self.orig_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Этот пользователь уже зарегистрирован!')

    def validate_email(self, email):
        if email.data != self.orig_email:
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError('Этот e-mail уже зарегистрирован!')

    def validate_bank_acc_curr(self, bank_acc_curr):
        if bank_acc_curr.data != self.orig_bank_acc_curr:
            acc_found = User.query.filter_by(bank_acc_curr=bank_acc_curr.data).first()
            acc_len = len(self.bank_acc_curr.data)
            acc_null = check_float(self.bank_acc_curr.data)
            if acc_found is not None:
                raise ValidationError('Этот валютный счет уже зарегистрирован!')
            elif acc_len != 2:
                raise ValidationError('Cчет должен состоять из 2 числовых символов!')
            elif acc_null == 0:
                raise ValidationError('Cчет должен быть числовым!')
        
    def validate_bank_acc_rubl(self, bank_acc_rubl):
        if bank_acc_rubl.data != self.orig_bank_acc_rubl:
            acc_found = User.query.filter_by(bank_acc_rubl=bank_acc_rubl.data).first()
            acc_len = len(self.bank_acc_rubl.data)
            acc_null = check_float(self.bank_acc_rubl.data)
            if acc_found is not None:
                raise ValidationError('Этот рублевый счет уже зарегистрирован!')
            elif acc_len != 2:
                raise ValidationError('Cчет должен состоять из 2 числовых символов!')
            elif acc_null == 0:
                raise ValidationError('Cчет должен быть числовым!')
            