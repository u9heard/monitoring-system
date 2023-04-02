from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields import DateTimeLocalField, SelectField, FileField
from wtforms.validators import DataRequired
from wtforms import validators


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()], render_kw={"placeholder": "Логин"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"placeholder": "Пароль"})
    remember_me = BooleanField('Запомнить')
    submit = SubmitField('Войти')

class DataForm(FlaskForm):
    date_start = DateTimeLocalField("Начало записи", format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    date_end = DateTimeLocalField("Конец записи", format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    box_field = SelectField("Шкаф:", coerce=str)
    submit = SubmitField('Сохранить') #TODO html5 datetime is better(placeholder)

class FileForm(FlaskForm):
    file = FileField()
    submit = SubmitField('Сохранить')
    
class ConfigForm(FlaskForm):
    address_field = SelectField("Шкаф:", coerce=str)
    submit = SubmitField('Сохранить', render_kw={"class": "custom-button"})

    