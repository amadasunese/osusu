# from . import db
# from datetime import datetime, date

# from flask_login import UserMixin

# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     hashed_password = db.Column(db.String(100), nullable=False)
#     groups = db.relationship('Group', backref='user', lazy=True)  # Many-to-Many relationship

# class Group(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     members = db.relationship('User', secondary='group_members', backref='groups')  # Many-to-Many relationship


# class GroupMember(db.Model):
#     __tablename__ = 'group_members'
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
#     group_id = db.Column(db.Integer, db.ForeignKey('group.id'), primary_key=True)

#     user = db.relationship(User, backref=db.backref('group_members', cascade='all, delete-orphan'))
#     group = db.relationship(Group, backref=db.backref('group_members', cascade='all, delete-orphan'))

#     def __repr__(self):
#         return f'<GroupMember User: {self.user_id}, Group: {self.group_id}>'
    

# class Contribution(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     amount = db.Column(db.Float, nullable=False)
#     date = db.Column(db.Date, default=date.today)

#     group = db.relationship('Group', back_populates='contributions')
#     user = db.relationship('User', back_populates='contributions')

# Group.contributions = db.relationship('Contribution', order_by=Contribution.date, back_populates='group')

# class Feedback(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

#     user = db.relationship('User', backref=db.backref('feedbacks', lazy=True))

#     def __repr__(self):
#         return f'<Feedback {self.id} - User {self.user_id}>'

# from . import db
# from datetime import datetime

# class Schedule(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     date = db.Column(db.Date, nullable=False)
#     amount = db.Column(db.Float, nullable=False)
#     user = db.relationship('User', backref=db.backref('schedules', lazy=True))

#     def __repr__(self):
#         return f'<Schedule {self.id} - User {self.user_id} - Date {self.date} - Amount {self.amount}>'


from . import db
from datetime import datetime, date
from flask_login import UserMixin
from enum import Enum

class Role(Enum):
    USER = "User"
    ADMIN = "Admin"

# Define the association table first
group_members = db.Table('group_members',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True)
)

# class JoinRequest(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
#     status = db.Column(db.String(50), default='pending')
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

#     user = db.relationship('User', backref='join_requests')
#     group = db.relationship('Group', backref='join_requests')


class JoinRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')  # 'pending', 'approved', 'denied'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('join_requests', cascade='all, delete-orphan'))
    group = db.relationship('Group', backref=db.backref('join_requests', cascade='all, delete-orphan'))

    def __repr__(self):
        return f'<JoinRequest {self.id} - User {self.user_id} - Group {self.group_id} - Status {self.status}>'

    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    hashed_password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Enum(Role), default=Role.USER)
    is_admin = db.Column(db.Boolean, default=False)

    groups = db.relationship('Group', secondary=group_members, back_populates='members')
    created_groups = db.relationship('Group', backref='creator', lazy=True, foreign_keys='Group.created_by')
    schedules = db.relationship('Schedule', backref='user', lazy=True)
    feedbacks = db.relationship('Feedback', backref='user', lazy=True)
    contributions = db.relationship('Contribution', back_populates='user')

    def __repr__(self):
        return f'<User {self.username} - Role {self.role}>'


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    members = db.relationship('User', secondary=group_members, back_populates='groups')
    schedules = db.relationship('Schedule', backref='group', lazy=True)
    contributions = db.relationship('Contribution', back_populates='group')

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


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Feedback {self.id} - User {self.user_id}>'


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Schedule {self.id} - User {self.user_id} - Group {self.group_id} - Date {self.date} - Amount {self.amount}>'
