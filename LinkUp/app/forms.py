# install FlaskForm flask_wtf depricated
from flask_wtf import Form
from wtforms import StringField, BooleanField, DateTimeField
from wtforms.validators import DataRequired, Length


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class EventForm(Form):
    name = StringField('Name of event', validators=[DataRequired(), Length(max=64)])
    description = StringField('Description', validators=[DataRequired(), Length(max=120)])
    venu = StringField('Venu', validators=[DataRequired(), Length(max=64)])
    date = DateTimeField('Start time', format='%d/%m/%y %H%M%S')
    end_time = DateTimeField('End time', format='%m/%d/%y %h:%m %s')
    category = StringField('Category', validators=[DataRequired()])
    admission = StringField('Admission', validators=[DataRequired()])
