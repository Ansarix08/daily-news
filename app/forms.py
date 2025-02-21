from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email
from flask_wtf.file import FileField, FileAllowed
from wtforms import URLField
from wtforms.validators import Optional, URL

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class ContentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Content', validators=[DataRequired()])
    image = FileField('Image')
    external_link = URLField('External Link', validators=[Optional(), URL()])
    submit = SubmitField('Save')

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired(), Length(min=2, max=100)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=1000)])
    submit = SubmitField('Send Message') 