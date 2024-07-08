from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectMultipleField
from wtforms import DateField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from app.models import User, Group
from wtforms import FloatField, StringField, validators, SelectField

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Regexp('^.{6,20}$', message='Your password should be between 6 and 20 characters long.'),
        Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$', message='Password must include uppercase, lowercase, and numbers.')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
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
    amount = FloatField('Amount', [validators.DataRequired()])
    description = StringField('Description', [validators.Length(max=100)])
    submit = SubmitField('Submit')

class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired(), validators.Length(min=3, max=20)])
    email = StringField('Email', validators=[validators.DataRequired(), validators.Email()])
    submit = SubmitField('Update Profile')

# class CreateGroupForm(FlaskForm):
#     name = StringField('Group Name', validators=[DataRequired()])
#     submit = SubmitField('Create Group')

class CreateGroupForm(FlaskForm):
    name = StringField('Group Name', validators=[DataRequired()])
    members = SelectMultipleField('Add Members', coerce=int)
    submit = SubmitField('Create Group')

# class AddMemberForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired()])
#     submit = SubmitField('Add Member')

class AddMemberForm(FlaskForm):
    members = SelectMultipleField('Add Members', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add Member')


class FeedbackForm(FlaskForm):
    content = TextAreaField('Feedback', validators=[DataRequired()])
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
