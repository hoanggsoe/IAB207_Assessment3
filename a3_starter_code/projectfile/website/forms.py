from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, SelectField, IntegerField, DateTimeField, FloatField
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange, DataRequired
from datetime import datetime

# creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

# this is the registration form
class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[InputRequired()])
    surname = StringField("Surname", validators=[InputRequired()])
    user_name=StringField("User Name", validators=[InputRequired()])
    email = StringField("Email Address", validators=[Email("Please enter a valid email")])
    contact_number = StringField("Contact Number", validators=[InputRequired()])
    street_address = TextAreaField("Street Address", validators=[InputRequired()])
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    # submit button
    submit = SubmitField("Register")

class EventForm(FlaskForm):
    name = StringField("Event Name", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    date = DateTimeField("Event Date", validators=[DataRequired()], format='%Y-%m-%dT%H:%M')
    venue = StringField("Venue", validators=[DataRequired()])
    category = SelectField("Category", choices=[
        ('Jazz', 'Jazz'),
        ('Rock', 'Rock'),
        ('Hip-Hop', 'Hip-Hop'),
        ('Electronic', 'Electronic'),
        ('Classical', 'Classical'),
        ('Pop', 'Pop'),
        ('Reggae', 'Reggae'),
        ('Acoustic', 'Acoustic')
    ], validators=[DataRequired()])
    price = FloatField("Ticket Price", validators=[DataRequired(), NumberRange(min=0)])
    tickets_available = IntegerField("Available Tickets", validators=[DataRequired(), NumberRange(min=1)])
    image = FileField("Event Image", validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField("Create Event")

class CommentForm(FlaskForm):
    content = TextAreaField("Comment", validators=[DataRequired(), Length(min=1, max=500)])
    submit = SubmitField("Post Comment")

class BookingForm(FlaskForm):
    quantity = IntegerField("Number of Tickets", validators=[DataRequired(), NumberRange(min=1, max=10)])
    submit = SubmitField("Book Tickets")