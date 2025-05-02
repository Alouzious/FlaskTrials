from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask_wtf.file import FileField, FileRequired, FileAllowed





class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message='Passwords must match')
    ])
    dob = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    country = SelectField('Country', choices=[
        ('Uganda', 'Uganda'),
        ('Kenya', 'Kenya'),
        ('Tanzania', 'Tanzania'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    submit = SubmitField('Sign Up')


class ProfileUpdateForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')


class ImageUploadForm(FlaskForm):
    # Form to upload an image with a description
    image = FileField('Image', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Upload Image')