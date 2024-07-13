from flask_mail import Mail, Message
from flask import current_app
from flask import url_for
from itsdangerous import URLSafeTimedSerializer
import os


from flask import render_template, request, flash, redirect, url_for, current_app
from flask_mail import Message

from . import mail

# def send_email(to, subject, template):
#     msg = Message(
#         subject,
#         recipients=[to],
#         html=template,
#         sender=current_app.config["MAIL_DEFAULT_SENDER"],
#     )
#     mail.send(msg)

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender= os.environ.get('MAIL_DEFAULT_SENDER')
        
    )
    mail.send(msg)



# # Flask app configuration
# MAIL_SERVER = "smtp.gmail.com"
# MAIL_PORT = 465
# MAIL_USE_SSL = True
# MAIL_USERNAME = 'amadasunese@gmail.com'
# MAIL_PASSWORD = 'qxxo axga dzia jjsw'
# MAIL_DEFAULT_SENDER = 'amadasunese@gmail.com'

# app.config.update(
#     MAIL_SERVER='smtp.gmail.com',
#     MAIL_PORT=587,
#     MAIL_USE_TLS=True,
#     MAIL_USE_SSL=False,
#     MAIL_USERNAME='your-email@gmail.com',
#     MAIL_PASSWORD='your-email-password',
#     MAIL_DEFAULT_SENDER='your-email@gmail.com'
# )

# mail = Mail()

# def send_email(to, subject, template):
#     msg = Message(
#         subject,
#         recipients=[to],
#         html=template,
#         sender=current_app.config["MAIL_DEFAULT_SENDER"],
#     )
#     mail.send(msg)

# def send_email(to, subject, template):
#     msg = Message(
#         subject,
#         recipients=[to],
#         html=template,
#         sender=current_app.config["MAIL_DEFAULT_SENDER"],
#     )
#     mail.send(msg)

    
def send_feedback(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=current_app.config["MAIL_DEFAULT_SENDER"],
    )
    mail.send(msg)

def send_password_reset_email(user):

    """Initialize the serializer with the app's secret key"""
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

    """Generate a token"""
    token = serializer.dumps(user.email, salt='password-reset-salt')

    """Create the password reset email"""
    msg = Message('Reset Your Password',
                  sender=current_app.config["MAIL_DEFAULT_SENDER"],
                  recipients=[user.email])

    """Email body with the link to reset password"""
    msg.body = (
        "To reset your password, visit the following link: "
        f"{url_for('main.reset_password', token=token, _external=True)}"
    )

    # Send the email
    mail.send(msg)