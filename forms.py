from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, validators

class SignupForm(FlaskForm):
    Firstname = StringField('Firstname', [
        validators.Length(min=4, max=25),
        validators.DataRequired()
    ])
    Lastname = StringField('Lastname', [
        validators.Length(min=4, max=25),
    ])
    email = StringField('Email Address', [
        validators.Email(),
        validators.DataRequired()
    ])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.Length(min=4, max=25)
    ])


class SigninForm(FlaskForm):
    email = StringField('Email Address', [
        validators.Email(),
        validators.DataRequired()
    ])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.Length(min=4, max=25)
    ])
