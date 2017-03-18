# install FlaskForm flask_wtf depricated
from flask_wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired, Length
from wtforms.fields.html5 import DateTimeField, DateField, DateTimeLocalField


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class EventForm(Form):
    name = StringField('Name of event', validators=[DataRequired(), Length(max=64)])
    description = StringField('Description', validators=[DataRequired(), Length(max=120)])
    venu = StringField('Venu', validators=[DataRequired(), Length(max=64)])
    date = DateField('Start Date Time')
    end_time = DateTimeLocalField('End Date Time')
    category = StringField('Category', validators=[DataRequired()])
    admission = StringField('Admission', validators=[DataRequired()])


class EditUserForm(Form):
    nickname = StringField('Displap Name', validators=[DataRequired(), Length(max=64)])
    username = StringField('User Name', validators=[DataRequired(), Length(max=64)])
    email = StringField('Email', validators=[Length(max=64)])
    website = StringField('Website', validators=[Length(max=64)])
    bio = StringField('Bio', validators=[Length(max=120)])
