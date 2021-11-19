from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import Length, Regexp, DataRequired, EqualTo, Email
from wtforms import ValidationError
from models import User
from database import db


class RegisterForm(FlaskForm):
    class Meta:
        csrf = False

    full_name = StringField('Full Name', validators=[Length(1, 30)])

    email = StringField('Email', [
        Email(message='Not a valid email address.'),
        DataRequired()])

    username = StringField('Username', validators=[Length(5, 20)])

    password = PasswordField('Password', [
        DataRequired(message="Please enter a password."),
        EqualTo('confirmPassword', message='Passwords must match')
    ])

    confirmPassword = PasswordField('Confirm Password', validators=[
        Length(min=6, max=10)
    ])
    submit = SubmitField('Submit')

    def validate_username(self, field):
        if db.session.query(User).filter_by(username=field.data).count() != 0:
            raise ValidationError('Username already in use.')


class LoginForm(FlaskForm):
    class Meta:
        csrf = False

    username = StringField('Username', [
        DataRequired(message="Please enter a Username.")])

    password = PasswordField('Password', [
        DataRequired(message="Please enter a password.")])

    submit = SubmitField('Submit')

    def validate_username(self, field):
        if db.session.query(User).filter_by(username=field.data).count() == 0:
            raise ValidationError('Incorrect username or password.')

