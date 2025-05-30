from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, validators ,SubmitField, SelectField, HiddenField 

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

class Borrow(FlaskForm):
    borrow = SubmitField('Borrow')


class SigninForm(FlaskForm):
    email = StringField('Email Address', [
        validators.Email(),
        validators.DataRequired()
    ])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.Length(min=4, max=25)
    ])

class Searchbar(FlaskForm):
    search_query = StringField(
        'Search',
        render_kw={"placeholder": "Search by book name"},
        )
    submit = SubmitField('Search')

class Singup(FlaskForm):
    sgnup = SubmitField('Sign UP')

class Singin(FlaskForm):
    sgnin = SubmitField('Sign UP')

class Return(FlaskForm):
    rturn = SubmitField('Return')