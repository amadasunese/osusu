from flask_migrate import Migrate
from app import create_app

app = create_app()
from app.models import User, Role
from app import db

migrate = Migrate(app, db)

@app.cli.command('update_roles')
def update_roles():
    users = User.query.all()
    for user in users:
        if user.role == "User":
            user.role = Role.USER
        elif user.role == "Admin":
            user.role = Role.ADMIN
        db.session.add(user)
    db.session.commit()

if __name__ == '__main__':
    import click
    @click.group()
    def db():
        pass
    db.add_command(migrate)  # Add migrate command to the db group

    if __name__ == '__main__':
        db()  # Run the db group, which includes migrate


# from flask_migrate import Migrate
# from app import create_app
# app = create_app()
# from app.models import User, Role
# from app import db

# migrate = Migrate(app, db)

# @app.cli.command('update_roles')
# def update_roles():
#     users = User.query.all()
#     for user in users:
#         if user.role == "User":
#             user.role = Role.USER
#         elif user.role == "Admin":
#             user.role = Role.ADMIN
#         db.session.add(user)
#     db.session.commit()

# if __name__ == '__main__':
#     migrate.upgrade() 


# from flask_migrate import Migrate
# from app import create_app
# from flask import cli

# app = create_app()
# from app.models import User, Role
# from app import db

# migrate = Migrate(app, db)

# @cli.command()
# def update_roles():
#     users = User.query.all()
#     for user in users:
#         if user.role == "User":
#             user.role = Role.USER
#         elif user.role == "Admin":
#             user.role = Role.ADMIN
#         db.session.add(user)
#     db.session.commit()

# if __name__ == '__main__':
#     @cli.command()
#     def db():
#         migrate.upgrade()  # Example usage

#     cli.run()
    

# from flask_migrate import Migrate
# # from flask_script import Manager
# from app import create_app, db
# from app.models import User, Role

# from flask import cli
# app = create_app
# # manager = Manager(app)
# migrate = Migrate(app, db)

# @manager.command
# def update_roles():
#     users = User.query.all()
#     for user in users:
#         if user.role == "User":
#             user.role = Role.USER
#         elif user.role == "Admin":
#             user.role = Role.ADMIN
#         db.session.add(user)
#     db.session.commit()

# if __name__ == '__main__':
#     @cli.command()
#     def db():
#         migrate.upgrade()  # Example usage

#     cli.run()



# manager = Manager(app)
# migrate = Migrate(app, db)

# @manager.command
# def update_roles():
#     users = User.query.all()
#     for user in users:
#         if user.role == "User":
#             user.role = Role.USER
#         elif user.role == "Admin":
#             user.role = Role.ADMIN
#         db.session.add(user)
#     db.session.commit()

# if __name__ == '__main__':
#     from flask import cli

#     @cli.command()
#     def db():
#         manager.add_command('db')
#         # Your database migration commands here
#         migrate.upgrade()  # Example usage

#     cli.run()
    
