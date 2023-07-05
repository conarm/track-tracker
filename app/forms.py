from app import models
from flask_wtf import FlaskForm
from wtforms import DateField, StringField, TextAreaField, BooleanField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo

# class AddForm(FlaskForm):
#     # Create a new FlaskForm with the correct fields
#     deadline = DateField('Deadline', validators=[DataRequired()], format='%Y-%m-%d')
#     module_code = StringField('Module code', validators=[DataRequired()])
#     assessment_title = StringField('Assessment title', validators=[DataRequired()])
#     assessment_desc = TextAreaField('Assessment Description', validators=[DataRequired()])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = models.User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = models.User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class RatingForm(FlaskForm):
    rating = SelectField('Rating', choices=[0,1,2,3,4,5,6,7,8,9,10], validators=[DataRequired()])
    review = TextAreaField('Review', validators=[DataRequired()])
    submit = SubmitField('Add rating')