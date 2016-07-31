from flask_wtf import Form
from flask import flash
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from ..models import User

class ChangePasswordForm(Form):
    old_password = PasswordField('Password', validators=[Required()])
    password = PasswordField('Password', validators=[
        Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    change_password = SubmitField('Change Password')
    
class UpdateProfileForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 128),
                                             Email()])
    username = StringField('Username', validators=[
                    Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    full_name = StringField('Full name', validators=[Required(), Length(1, 255)])
    update_profile = SubmitField('Update Profile')
    
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
            
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')