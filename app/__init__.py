# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from config import Config
# from flask_login import LoginManager
# from flask_mail import Mail
# from flask_wtf.csrf import CSRFProtect
# from flask_bcrypt import Bcrypt
# from flask_migrate import Migrate

# db = SQLAlchemy()
# bcrypt = Bcrypt()
# migrate = Migrate()
# csrf = CSRFProtect()

# mail = Mail()
# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)
#     db.init_app(app)
#     mail = Mail(app)
#     csrf.init_app(app)
#     # csrf = CSRFProtect(app)
#     migrate.init_app(app, db)

#     login_manager = LoginManager()
#     login_manager.login_view = 'main.login'
#     login_manager.init_app(app)

#     from .models import User
#     from app.routes import main
#     app.register_blueprint(main)
  

#     @login_manager.user_loader
#     def load_user(user_id):
#         return User.query.get(int(user_id))
    
#     from .models import Group, Schedule, Feedback

#     with app.app_context():
#         # from app.routes import route
#         db.create_all()
#         return app


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
csrf = CSRFProtect()

mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)

    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.init_app(app)

    from .models import User
    from app.routes import main
    app.register_blueprint(main)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from .models import Group, Schedule, Feedback

    with app.app_context():
        db.create_all()
        
    return app
