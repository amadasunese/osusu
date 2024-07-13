# from . import db
# from datetime import datetime, date
# from flask_login import UserMixin
# from enum import Enum

# class Role(Enum):
#     USER = "User"
#     ADMIN = "Admin"

# # Define the association table first
# group_members = db.Table('group_members',
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
#     db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True)
# )


# class JoinRequest(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
#     status = db.Column(db.String(20), nullable=False, default='pending')  # 'pending', 'approved', 'denied'
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
#     user = db.relationship('User', backref=db.backref('join_requests', cascade='all, delete-orphan'))
#     group = db.relationship('Group', backref=db.backref('join_requests', cascade='all, delete-orphan'))

#     def __repr__(self):
#         return f'<JoinRequest {self.id} - User {self.user_id} - Group {self.group_id} - Status {self.status}>'

    
# # class User(db.Model, UserMixin):
# #     id = db.Column(db.Integer, primary_key=True)
# #     username = db.Column(db.String(50), unique=True, nullable=False)
# #     email = db.Column(db.String(100), unique=True, nullable=False)
# #     hashed_password = db.Column(db.String(100), nullable=False)
# #     role = db.Column(db.Enum(Role), default=Role.USER)
# #     is_admin = db.Column(db.Boolean, default=False)

# #     groups = db.relationship('Group', secondary=group_members, back_populates='members')
# #     created_groups = db.relationship('Group', backref='creator', lazy=True, foreign_keys='Group.created_by')
# #     schedules = db.relationship('Schedule', backref='user', lazy=True)
# #     feedbacks = db.relationship('Feedback', backref='user', lazy=True)
# #     contributions = db.relationship('Contribution', back_populates='user')

# #     def __repr__(self):
# #         return f'<User {self.username} - Role {self.role}>'

# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     hashed_password = db.Column(db.String(100), nullable=False)
#     role = db.Column(db.Enum(Role), default=Role.USER)
#     is_admin = db.Column(db.Boolean, default=False)
#     fullname = db.Column(db.String(50), nullable=False)
#     phonenumber = db.Column(db.String(20), nullable=True)
    
#     groups = db.relationship('Group', secondary=group_members, back_populates='members')
#     created_groups = db.relationship('Group', backref='creator', lazy=True, foreign_keys='Group.created_by')
#     schedules = db.relationship('Schedule', backref='user', lazy=True)
#     feedbacks = db.relationship('Feedback', backref='user', lazy=True)
#     contributions = db.relationship('Contribution', back_populates='user')
#     transactions = db.relationship('Transaction', backref='member', lazy=True)
    
#     def __repr__(self):
#         return f'<User {self.username} - Role {self.role}>'

# class Transaction(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     date = db.Column(db.DateTime, default=datetime.utcnow)
#     amount = db.Column(db.Float, nullable=False)
#     type = db.Column(db.String(10), nullable=False)  # 'contribution' or 'payout'
#     description = db.Column(db.String(100))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


# class Group(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

#     members = db.relationship('User', secondary=group_members, back_populates='groups')
#     schedules = db.relationship('Schedule', backref='group', lazy=True)
#     contributions = db.relationship('Contribution', back_populates='group')

#     def __repr__(self):
#         return f'<Group {self.name}>'

    
# class Contribution(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     amount = db.Column(db.Float, nullable=False)
#     date = db.Column(db.Date, default=date.today)

#     group = db.relationship('Group', back_populates='contributions')
#     user = db.relationship('User', back_populates='contributions')


# class Feedback(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

#     def __repr__(self):
#         return f'<Feedback {self.id} - User {self.user_id}>'


# class Schedule(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
#     date = db.Column(db.Date, nullable=False)
#     amount = db.Column(db.Float, nullable=False)

#     def __repr__(self):
#         return f'<Schedule {self.id} - User {self.user_id} - Group {self.group_id} - Date {self.date} - Amount {self.amount}>'



from . import db
from datetime import datetime, date
from flask_login import UserMixin
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash

class Role(Enum):
    USER = "User"
    ADMIN = "Admin"

# Define the association table first
group_members = db.Table('group_members',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True)
)

class JoinRequestStatus(Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    DENIED = "DENIED"

class JoinRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    # status = db.Column(db.String(20), nullable=False, default='pending')  # 'pending', 'approved', 'denied'
    status = db.Column(db.Enum(JoinRequestStatus), default=JoinRequestStatus.PENDING)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('join_requests', cascade='all, delete-orphan'))
    group = db.relationship('Group', backref=db.backref('join_requests', cascade='all, delete-orphan'))

    def __repr__(self):
        return f'<JoinRequest {self.id} - User {self.user_id} - Group {self.group_id} - Status {self.status}>'



# class JoinRequest(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
#     status = db.Column(db.Enum(JoinRequestStatus), default=JoinRequestStatus.PENDING)
    
#     user = db.relationship('User', backref='join_requests')
#     group = db.relationship('Group', backref='join_requests')

    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    hashed_password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Enum(Role), default=Role.USER)
    is_admin = db.Column(db.Boolean, default=False)
    fullname = db.Column(db.String(50), nullable=False)
    phonenumber = db.Column(db.String(20), nullable=True)
    
    groups = db.relationship('Group', secondary=group_members, back_populates='members')
    created_groups = db.relationship('Group', backref='creator', lazy=True, foreign_keys='Group.created_by')
    schedules = db.relationship('Schedule', backref='user', lazy=True)
    feedbacks = db.relationship('Feedback', backref='user', lazy=True)
    contributions = db.relationship('Contribution', back_populates='user')
    transactions = db.relationship('Transaction', backref='member', lazy=True)

    def __repr__(self):
        return f'<User {self.username} - Role {self.role}>'
    
    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.hashed_password, password)
    

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(10), nullable=False)  # 'contribution' or 'payout'
    description = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)

    # user = db.relationship('User', backref=db.backref('transactions', lazy=True))
    # group = db.relationship('Group', backref=db.backref('transactions', lazy=True))

    def __repr__(self):
        return f'<Transaction {self.id} - Amount {self.amount} - Type {self.type} - Group {self.group_id}>'

# class Transaction(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     date = db.Column(db.DateTime, default=datetime.utcnow)
#     amount = db.Column(db.Float, nullable=False)
#     type = db.Column(db.String(10), nullable=False)  # 'contribution' or 'payout'
#     description = db.Column(db.String(100))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)



class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    members = db.relationship('User', secondary=group_members, back_populates='groups')
    schedules = db.relationship('Schedule', backref='group', lazy=True)
    contributions = db.relationship('Contribution', back_populates='group')
    transactions = db.relationship('Transaction', backref='group', lazy=True)

    def __repr__(self):
        return f'<Group {self.name}>'

class Contribution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, default=date.today)

    group = db.relationship('Group', back_populates='contributions')
    user = db.relationship('User', back_populates='contributions')

    def __repr__(self):
        return f'<Contribution {self.id} - Group {self.group_id} - User {self.user_id} - Amount {self.amount}>'

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # user = db.relationship('User', backref=db.backref('feedbacks', lazy=True))

    def __repr__(self):
        return f'<Feedback {self.id} - User {self.user_id}>'

# class Feedback(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

#     def __repr__(self):
#         return f'<Feedback {self.id} - User {self.user_id}>'
    
class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False)

    # user = db.relationship('User', backref=db.backref('schedules', lazy=True))
    # group = db.relationship('Group', backref=db.backref('schedules', lazy=True))

    def __repr__(self):
        return f'<Schedule {self.id} - User {self.user_id} - Group {self.group_id} - Date {self.date} - Amount {self.amount}>'

# class Schedule(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
#     date = db.Column(db.Date, nullable=False)
#     amount = db.Column(db.Float, nullable=False)

#     def __repr__(self):
#         return f'<Schedule {self.id} - User {self.user_id} - Group {self.group_id} - Date {self.date} - Amount {self.amount}>'

