from flask_wtf import Form
from flask import flash
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
                    ValidationError, SelectField 
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from ..models import User, Role, Provider

class EditUserAdminForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 128),
                                             Email()])
    username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    full_name = StringField('Full name', validators=[Required(), Length(1, 255)])
    role = SelectField('Role', coerce=int)
    confirmed = BooleanField('Confirmed')
    suspended = BooleanField('Suspended')
    
    def __init__(self, user, *args, **kwargs):
        super(EditUserAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user
        
    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
            
    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
            

class CreateUserAdminForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 128),
                                             Email()])
    username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    full_name = StringField('Full name', validators=[Required(), Length(1, 255)])
    password = PasswordField('Password', validators=[
        Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    confirmed = BooleanField('Confirmed')
        
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
            
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
            
            
class DeleteUserAdminForm(Form):
    confirm = BooleanField('Confirmed', validators=[Required(message='You must confirm to delete.')])

class CreateUserProviderAdminForm(Form):
    provider = SelectField('Provider', coerce=int)

    def __init__(self, user, *args, **kwargs):
        super(CreateUserProviderAdminForm, self).__init__(*args, **kwargs)
        self.provider.choices = [(provider.id, provider.name)
                             for provider in Provider.query.order_by(Provider.name).all()]    

class CreateProviderAdminForm(Form):
    provider = StringField('Provider', validators=[Required(), Length(1, 128)])
    name = StringField('Name', validators=[Required(), Length(1, 256)])
    project_name = StringField('Tenant Name', validators=[Required(), Length(1, 128)])
    username = StringField('User Name', validators=[Required(), Length(1, 128)])
    password = PasswordField('Password', validators=[Required(), Length(1, 256)])
    api_version = StringField('API Version', validators=[Required(), Length(1, 64)])
    url = StringField('URL', validators=[Required(), Length(1, 256)])
    enabled = BooleanField('Enabled')
    
    def validate_name(self, field):
        if Provider.query.filter_by(name=field.data).first():
            raise ValidationError('Provider name is already used. Use different name.')
            
class EditProviderAdminForm(Form):
    provider = SelectField('Provider', validators=[Required()],
                            choices=[('openstack', 'OpenStack'), ('other', 'Other')])
    name = StringField('Name', validators=[Required(), Length(1, 128)])
    project_name = StringField('Tenant Name', validators=[Required(), Length(1, 128)])
    region = StringField('Region Name', validators=[Required(), Length(1, 128)])
    username = StringField('User Name', validators=[Required(), Length(1, 128)])
    password = PasswordField('Password', validators=[Required(), Length(1, 256)])
    api_version = StringField('API Version', validators=[Required(), Length(1, 64)])
    url = StringField('URL', validators=[Required(), Length(1, 256)])
    enabled = BooleanField('Enabled')
    
class DeleteProviderAdminForm(Form):
    confirm = BooleanField('Confirmed', validators=[Required(message='You must confirm to delete.')])
    
class ValidateProviderAdminForm(Form):
    provider = SelectField('Provider', coerce=int)
    confirm = BooleanField('Confirmed', validators=[Required(message='You must confirm to delete.')])
    
    def __init__(self, provider, *args, **kwargs):
        super(ValidateProviderAdminForm, self).__init__(*args, **kwargs)
        self.provider.choices = [(provider.id, provider.name)
                             for provider in Provider.query.order_by(Provider.name).all()]