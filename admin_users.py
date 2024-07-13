from flask import Flask, render_template, request, redirect, url_for, flash
from app import create_app
from app.models import db, User
from werkzeug.security import generate_password_hash

app = create_app()

def add_admin(username, hashed_password):
    with app.app_context():
        # Check for existing user
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print("An account with this email already exists.")
            return
        
        if isinstance(hashed_password, bytes):
            hashed_password = hashed_password.decode('utf-8')

        # Hash the password
        hashed_password = generate_password_hash(hashed_password)
        
        admin_user = User(email=email, username=username, hashed_password=hashed_password, is_admin=True)
        db.session.add(admin_user)
        db.session.commit()
        print(f"Admin {username} {hashed_password} added successfully.")

if __name__ == '__main__':
    email = input("Enter admin name: ")
    username = input("Enter admin email: ")
    # last_name = input("Enter admin last name: ")
    # email = input("Enter admin email: ")
    hashed_password = input("Enter admin password: ")
    add_admin(username, hashed_password)
