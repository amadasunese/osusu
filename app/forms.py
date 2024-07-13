from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectMultipleField
from wtforms import DateField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from app.models import User, Group
from wtforms import FloatField, StringField, validators, SelectField, HiddenField
from enum import Enum


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Regexp('^.{6,20}$', message='Your password should be between 6 and 20 characters long.'),
        Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$', message='Password must include uppercase, lowercase, and numbers.')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    fullname = StringField('Full Name', validators=[DataRequired()])
    phonenumber = StringField('Contact Number')
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already in use. Please choose a different one.')



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')



class TransactionForm(FlaskForm):
    amount = FloatField('Amount', validators=[DataRequired()])
    description = StringField('Description', validators=[Length(max=100)])
    user_id = HiddenField('User ID', validators=[DataRequired()])
    group_id = SelectField('Group', choices=[], validators=[DataRequired()])  # Will populate choices dynamically
    submit = SubmitField('Submit')


# class TransactionForm(FlaskForm):
#     amount = FloatField('Amount', [validators.DataRequired()])
#     description = StringField('Description', [validators.Length(max=100)])
#     submit = SubmitField('Submit')

# class TransactionForm(FlaskForm):
#     amount = FloatField('Amount', validators=[DataRequired()])
#     description = StringField('Description', validators=[Length(max=100)])
#     user_id = HiddenField('User ID', validators=[DataRequired()])
#     group_id = HiddenField('Group ID', validators=[DataRequired()])
#     submit = SubmitField('Submit')


class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired(), validators.Length(min=3, max=20)])
    email = StringField('Email', validators=[validators.DataRequired(), validators.Email()])
    submit = SubmitField('Update Profile')


class CreateGroupForm(FlaskForm):
    name = StringField('Group Name', validators=[DataRequired()])
    members = SelectMultipleField('Add Members', coerce=int)
    submit = SubmitField('Create Group')


class AddMemberForm(FlaskForm):
    members = SelectMultipleField('Add Members', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Member')


class FeedbackForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit Feedback')

class DeleteGroupForm(FlaskForm):
    submit = SubmitField('Delete Group')

class ScheduleForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    amount = DecimalField('Amount', validators=[DataRequired()])
    group = SelectField('Group', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(ScheduleForm, self).__init__(*args, **kwargs)
        self.group.choices = [(group.id, group.name) for group in Group.query.all()]

class JoinRequestForm(FlaskForm):
    group_id = SelectField('Group', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Join Group')


# class EditUserForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired()])
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     role = SelectField('Role', choices=[('USER', 'User'), ('ADMIN', 'Admin')], validators=[DataRequired()])
#     is_admin = BooleanField('Is Admin')
#     fullname = StringField('Full Name', validators=[DataRequired()])
#     phonenumber = StringField('Phone Number')
#     submit = SubmitField('Update')

# class EditUserForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50)])
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     role = SelectField('Role', choices=[('USER', 'User'), ('ADMIN', 'Admin')], validators=[DataRequired()])
#     is_admin = BooleanField('Is Admin')
#     fullname = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=50)])
#     phonenumber = StringField('Phone Number', validators=[Length(max=20)])
#     current_password = PasswordField('Current Password', validators=[Length(min=6, max=100)])
#     new_password = PasswordField('New Password', validators=[
#         Length(min=6, max=100),
#         EqualTo('confirm_new_password', message='Passwords must match')
#     ])
#     confirm_new_password = PasswordField('Confirm New Password')
#     submit = SubmitField('Update')

class Role(Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    
class EditUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Role', choices=[(role.name, role.value) for role in Role], validators=[DataRequired()])
    is_admin = BooleanField('Is Admin')
    fullname = StringField('Full Name', validators=[DataRequired()])
    phonenumber = StringField('Phone Number')
    current_password = PasswordField('Current Password')
    new_password = PasswordField('New Password')
    confirm_new_password = PasswordField('Confirm New Password', validators=[EqualTo('new_password', message='Passwords must match')])
    submit = SubmitField('Update User')