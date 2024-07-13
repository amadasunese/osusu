import os
from decouple import config

class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///osusu.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')

    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = config("SECRET_KEY", default="can-you-guess?")
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SECURITY_PASSWORD_SALT = config("SECURITY_PASSWORD_SALT", default="important")

    # MAIL_SERVER = "smtp.gmail.com"
    # MAIL_PORT = 465
    # MAIL_USE_SSL = True
    # MAIL_USE_SSL=False,
    # MAIL_USERNAME = 'amadasunese@gmail.com'
    # MAIL_PASSWORD = 'qxxo axga dzia jjsw'
    # MAIL_DEFAULT_SENDER = 'amadasunese@gmail.com'

  

    # MAIL_SERVER = 'smtp.example.com'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # MAIL_USE_SSL=False,
    # MAIL_USERNAME = 'your-email@example.com'
    # MAIL_PASSWORD = 'your-email-password'
    # MAIL_DEFAULT_SENDER = 'your-email@example.com'

# app.config.update(
#     MAIL_SERVER='smtp.gmail.com',
#     MAIL_PORT=587,
#     MAIL_USE_TLS=True,
#     MAIL_USE_SSL=False,
#     MAIL_USERNAME='your-email@gmail.com',
#     MAIL_PASSWORD='your-email-password',
#     MAIL_DEFAULT_SENDER='your-email@gmail.com'
# )
