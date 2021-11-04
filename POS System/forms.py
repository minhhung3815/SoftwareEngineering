from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError


class RegisterForm(FlaskForm):
    def my_length_check(form, field):
        if len(field.data) < 2 or len(field.data) > 15:
            raise ValidationError('Username must be from 2 to 15')

    def my_length_check_password(form, field):
        if len(field.data) < 3:
            raise ValidationError('Password must be more than 3 characters')

    username = StringField(label='Username', validators=[my_length_check, DataRequired()])
    email_address = StringField(label='Email', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=3), DataRequired()])
    password2 = PasswordField(label='Confirm password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Register')


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Login')