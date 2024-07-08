from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from . import db, bcrypt
from .models import User, Group, Contribution, Feedback, Schedule, JoinRequest, group_members
from flask_mail import Message
from . import mail
from . import create_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import RegistrationForm, LoginForm, ProfileForm, CreateGroupForm, AddMemberForm
from app.forms import FeedbackForm, ScheduleForm, JoinRequestForm


# app = create_app()

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

def send_email(subject, recipient, template, **kwargs):
    msg = Message(subject, recipients=[recipient])
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)

@main.route('/notify_payment')
@login_required
def notify_payment():
    send_email('Payment Confirmation', current_user.email, 'payment_confirmation')
    return 'Email sent!'


# @main.route('/profile', methods=['GET', 'POST'])
# @login_required
# def profile():
#     if request.method == 'POST':
#         current_user.email = request.form['email']
#         db.session.commit()
#         flash('Your profile has been updated.')
#     return render_template('profile.html')


@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('main.profile'))
    elif request.method == 'GET':
        form.email.data = current_user.email
    return render_template('profile.html', form=form)


# @main.route('/dashboard')
# def dashboard():
#     # Retrieve user data and display it
#     return render_template('dashboard.html')

# @main.route('/dashboard')
# @login_required
# def dashboard():
#     join_requests = JoinRequest.query.filter_by(group_id=current_user.id).all()
#     contributions = Contribution.query.filter_by(user_id=current_user.id).all()
#     return render_template('dashboard.html', join_requests=join_requests, contributions=contributions)



# @main.route('/dashboard')
# @login_required
# def dashboard():
#     if current_user.is_admin:
#         groups = Group.query.all()
#     else:
#         groups = Group.query.filter(Group.members.any(id=current_user.id)).all()
#     join_requests = JoinRequest.query.filter_by(group_id=current_user.id).all()
#     contributions = Contribution.query.filter_by(user_id=current_user.id).all()
#     group = Group.query.filter_by(id=current_user.id).all()
#     form = FeedbackForm()
#     return render_template('dashboard.html',
#                            join_requests=join_requests,
#                            contributions=contributions,
#                            form=form,
#                            groups=groups,
#                            group=group)

@main.route('/dashboard')
@login_required
def dashboard():
    user_group_ids = [group.id for group in current_user.groups]
    available_groups = Group.query.filter(~Group.id.in_(user_group_ids)).all()
    join_requests = JoinRequest.query.filter_by(group_id=current_user.id).all()
    
    contributions = Contribution.query.filter_by(user_id=current_user.id).all()
    form = FeedbackForm()
    return render_template('dashboard.html', 
                           available_groups=available_groups, 
                           join_requests=join_requests,
                           contributions=contributions,
                           form=form)



@main.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))  # Ensure the endpoint name is correct

    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered.', 'warning')
            return redirect(url_for('main.register'))

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, hashed_password=hashed_password)
        db.session.add(user)
        try:
            db.session.commit()
            flash('Account created successfully! You can now log in.', 'success')
            return redirect(url_for('main.login'))
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again.', 'danger')
            # Optionally log the error for further investigation
            print(e)

    return render_template('register.html', title='Register', form=form)


# @main.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         user = User.query.filter_by(username=username).first()
#         if user and check_password_hash(user.hashed_password, password):
#             login_user(user)
#             return redirect(url_for('main.dashboard'))
#         else:
#             flash('Invalid username or password')
#     return render_template('login.html')

@main.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.hashed_password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


# @main.route('/create_group', methods=['POST'])
# @login_required
# def create_group():
#     name = request.form['name']
#     new_group = Group(name=name, created_by=current_user.id)
#     db.session.add(new_group)
#     db.session.commit()
#     return redirect(url_for('main.dashboard'))


# @main.route('/create_group', methods=['GET', 'POST'])
# @login_required
# def create_group():
#     form = CreateGroupForm()
#     if form.validate_on_submit():
#         group = Group(name=form.name.data, created_by=current_user.id)
#         db.session.add(group)
#         db.session.commit()
#         flash('Group created successfully.', 'success')
#         return redirect(url_for('main.index'))
#     return render_template('create_group.html', form=form)


@main.route('/create_group', methods=['GET', 'POST'])
@login_required
def create_group():
    form = CreateGroupForm()
    # Populate the members field with all users except the current user
    form.members.choices = [(user.id, user.username) for user in User.query.filter(User.id != current_user.id).all()]

    if form.validate_on_submit():
        group = Group(name=form.name.data, created_by=current_user.id)
        db.session.add(group)
        db.session.commit()

        # Add selected members to the group
        for user_id in form.members.data:
            group_member = group_members.insert().values(user_id=user_id, group_id=group.id)
            db.session.execute(group_member)
        
        # Add the current user (creator) to the group
        group_member = group_members.insert().values(user_id=current_user.id, group_id=group.id)
        db.session.execute(group_member)
        
        db.session.commit()
        flash('Group created successfully!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('create_group.html', form=form)


@main.route('/group_list')
def group_list():
    groups = Group.query.all()
    return render_template('group_list.html', groups=groups)

# @main.route('/join_group/<group_id>', methods=['GET'])
# @login_required
# def join_group(group_id):
#     group = Group.query.filter_by(id=group_id).first()
#     if group and current_user not in group.members:
#         group.members.append(current_user)
#         db.session.commit()
#     return redirect(url_for('main.dashboard'))


# @main.route('/group/<int:group_id>')
# @login_required
# def view_group(group_id):
#     group = Group.query.get_or_404(group_id)
#     contributions = Contribution.query.filter_by(group_id=group_id).order_by(Contribution.date).all()
#     return render_template('group.html', group=group, contributions=contributions)

# @main.route('/leave_group/<int:group_id>', methods=['GET'])
# @login_required
# def leave_group(group_id):
#     group = Group.query.get_or_404(group_id)
#     if current_user in group.members:
#         group.members.remove(current_user)
#         db.session.commit()
#     return redirect(url_for('main.dashboard'))



# @main.route('/group/<int:group_id>/add_member', methods=['GET', 'POST'])
# @login_required
# def add_member(group_id):
#     form = AddMemberForm()
#     group = Group.query.get_or_404(group_id)
#     if group.created_by != current_user.id and current_user.role != Role.ADMIN:
#         flash('You do not have permission to add members.', 'danger')
#         return redirect(url_for('main.group', group_id=group_id))
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user:
#             group.members.append(user)
#             db.session.commit()
#             flash('Member added successfully.', 'success')
#         else:
#             flash('User not found.', 'danger')
#         return redirect(url_for('main.group', group_id=group_id))
#     return render_template('add_member.html', form=form, group=group)

@main.route('/group/<int:group_id>/add_member', methods=['GET', 'POST'])
@login_required
def add_member(group_id):
    group = Group.query.get_or_404(group_id)
    if current_user != group.created_by:
        abort(403)
    form = AddMemberForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            group.members.append(user)
            db.session.commit()
            flash('Member added successfully', 'success')
        else:
            flash('User not found', 'danger')
    return render_template('add_member.html', form=form, group=group)


@main.route('/group/<int:group_id>/delete', methods=['POST'])
@login_required
def delete_group(group_id):
    group = Group.query.get_or_404(group_id)
    if current_user.id != group.created_by and not current_user.is_admin:
        abort(403)
    
    db.session.delete(group)
    db.session.commit()
    flash('Group deleted successfully!', 'success')
    return redirect(url_for('main.dashboard'))




# @main.route('/group/<int:group_id>')
# @login_required
# def group_detail(group_id):
#     group = Group.query.get_or_404(group_id)
#     if current_user not in group.members:
#         abort(403)
#     return render_template('group_detail.html', group=group)


@main.route('/group/<int:group_id>', methods=['GET', 'POST'])
@login_required
def group_detail(group_id):
    group = Group.query.get_or_404(group_id)
    if current_user not in group.members:
        abort(403)
    
    form = AddMemberForm()
    form.members.choices = [(user.id, user.username) for user in User.query.all() if user.id not in [member.id for member in group.members]]

    if form.validate_on_submit():
        for user_id in form.members.data:
            group_member = group_members.insert().values(user_id=user_id, group_id=group.id)
            db.session.execute(group_member)
        db.session.commit()
        flash('Members added successfully!', 'success')
        return redirect(url_for('main.group_detail', group_id=group.id))

    return render_template('group_detail.html', group=group, form=form)




# @main.route('/group/<int:group_id>/manage_requests')
# @login_required
# def manage_requests(group_id):
#     group = Group.query.get_or_404(group_id)
#     if current_user != group.created_by:
#         abort(403)
#     join_requests = JoinRequest.query.filter_by(group_id=group_id).all()
#     return render_template('manage_requests.html', join_requests=join_requests, group=group)

@main.route('/submit_feedback', methods=['POST'])
@login_required
def submit_feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        feedback = Feedback(user_id=current_user.id, content=form.content.data)
        db.session.add(feedback)
        db.session.commit()
        flash('Feedback submitted successfully', 'success')
    return redirect(url_for('main.dashboard'))


# @main.route('/group/<int:group_id>/remove_member/<int:user_id>', methods=['POST'])
# @login_required
# def remove_member(group_id, user_id):
#     group = Group.query.get_or_404(group_id)
#     user = User.query.get_or_404(user_id)
#     if group.created_by != current_user.id and current_user.role != Role.ADMIN:
#         flash('You do not have permission to remove members.', 'danger')
#         return redirect(url_for('main.group', group_id=group_id))
#     group.members.remove(user)
#     db.session.commit()
#     flash('Member removed successfully.', 'success')
#     return redirect(url_for('main.group', group_id=group_id))

@main.route('/group/<int:group_id>/remove_member/<int:user_id>', methods=['POST'])
@login_required
def remove_member(group_id, user_id):
    group = Group.query.get_or_404(group_id)
    if current_user.id != group.created_by and not current_user.is_admin:
        abort(403)
    
    group_member = group_members.delete().where(
        group_members.c.user_id == user_id,
        group_members.c.group_id == group_id
    )
    db.session.execute(group_member)
    db.session.commit()
    flash('Member removed successfully!', 'success')
    return redirect(url_for('main.group_detail', group_id=group.id))



# @main.route('/group/<int:group_id>/request_join', methods=['POST'])
# @login_required
# def request_join(group_id):
#     group = Group.query.get_or_404(group_id)
#     if current_user in group.members:
#         flash('You are already a member of this group.', 'info')
#         return redirect(url_for('main.group', group_id=group_id))
#     # Create a join request (this could be a new model or an attribute in an existing model)
#     # For simplicity, we are directly adding the user
#     group.members.append(current_user)
#     db.session.commit()
#     flash('Join request sent.', 'success')
#     return redirect(url_for('main.group', group_id=group_id))


@main.route('/group/<int:group_id>/request_join', methods=['POST'])
@login_required
def request_join(group_id):
    group = Group.query.get_or_404(group_id)
    if current_user in group.members:
        flash('You are already a member of this group.', 'info')
        return redirect(url_for('main.group_detail', group_id=group_id))
    
    # Check if a join request already exists
    existing_request = JoinRequest.query.filter_by(user_id=current_user.id, group_id=group_id).first()
    if existing_request:
        flash('You have already requested to join this group.', 'info')
        return redirect(url_for('main.group_detail', group_id=group_id))

    # Create a new join request
    join_request = JoinRequest(user_id=current_user.id, group_id=group_id)
    db.session.add(join_request)
    db.session.commit()
    flash('Join request sent.', 'success')
    return redirect(url_for('main.group_detail', group_id=group_id))


@main.route('/group/<int:group_id>/manage_requests')
@login_required
def manage_requests(group_id):
    group = Group.query.get_or_404(group_id)
    if current_user.id != group.created_by and not current_user.is_admin:
        abort(403)

    join_requests = JoinRequest.query.filter_by(group_id=group_id, status='pending').all()
    return render_template('manage_requests.html', group=group, join_requests=join_requests)



@main.route('/group/<int:group_id>/approve_request/<int:request_id>', methods=['POST'])
@login_required
def approve_request(group_id, request_id):
    join_request = JoinRequest.query.get_or_404(request_id)
    group = Group.query.get_or_404(group_id)
    if current_user.id != group.created_by and not current_user.is_admin:
        abort(403)

    join_request.status = 'approved'
    group.members.append(join_request.user)
    db.session.commit()
    flash('Join request approved.', 'success')
    return redirect(url_for('main.manage_requests', group_id=group_id))

@main.route('/group/<int:group_id>/deny_request/<int:request_id>', methods=['POST'])
@login_required
def deny_request(group_id, request_id):
    join_request = JoinRequest.query.get_or_404(request_id)
    group = Group.query.get_or_404(group_id)
    if current_user.id != group.created_by and not current_user.is_admin:
        abort(403)

    join_request.status = 'denied'
    db.session.commit()
    flash('Join request denied.', 'info')
    return redirect(url_for('main.manage_requests', group_id=group_id))




# @main.route('/group/<int:group_id>/accept_request/<int:user_id>', methods=['POST'])
# @login_required
# def accept_request(group_id, user_id):
#     group = Group.query.get_or_404(group_id)
#     user = User.query.get_or_404(user_id)
#     if group.created_by != current_user.id and current_user.role != Role.ADMIN:
#         flash('You do not have permission to accept requests.', 'danger')
#         return redirect(url_for('main.group', group_id=group_id))
#     group.members.append(user)
#     db.session.commit()
#     flash('Member added successfully.', 'success')
#     return redirect(url_for('main.group', group_id=group_id))

# @main.route('/group/<int:group_id>/reject_request/<int:user_id>', methods=['POST'])
# @login_required
# def reject_request(group_id, user_id):
#     group = Group.query.get_or_404(group_id)
#     user = User.query.get_or_404(user_id)
#     if group.created_by != current_user.id and current_user.role != Role.ADMIN:
#         flash('You do not have permission to reject requests.', 'danger')
#         return redirect(url_for('main.group', group_id=group_id))
#     # Remove join request (this could be a new model or an attribute in an existing model)
#     # For simplicity, we are directly rejecting the user
#     db.session.commit()
#     flash('Join request rejected.', 'success')
#     return redirect(url_for('main.group', group_id=group_id))

# @main.route('/accept_request/<int:group_id>/<int:user_id>', methods=['POST'])
# @login_required
# def accept_request(group_id, user_id):
#     join_request = JoinRequest.query.filter_by(group_id=group_id, user_id=user_id).first_or_404()
#     group = Group.query.get_or_404(group_id)
#     user = User.query.get_or_404(user_id)
#     if current_user != group.created_by:
#         abort(403)
#     group.members.append(user)
#     db.session.commit()
#     flash('Request accepted.', 'success')
#     return redirect(url_for('main.manage_requests', group_id=group_id))

# @main.route('/reject_request/<int:group_id>/<int:user_id>', methods=['POST'])
# @login_required
# def reject_request(group_id, user_id):
#     join_request = JoinRequest.query.filter_by(group_id=group_id, user_id=user_id).first_or_404()
#     group = Group.query.get_or_404(group_id)
#     if current_user != group.created_by:
#         abort(403)
#     db.session.delete(join_request)
#     db.session.commit()
#     flash('Request rejected.', 'success')
#     return redirect(url_for('main.manage_requests', group_id=group_id))


@main.route('/group/<int:group_id>/roster')
@login_required
def roster(group_id):
    group = Group.query.get_or_404(group_id)
    return render_template('roster.html', group=group)



# @main.route('/schedule', methods=['GET', 'POST'])
# @login_required
# def schedule():
#     if request.method == 'POST':
#         new_date = request.form['date']
#         new_amount = request.form['amount']
#         # Assume existing Schedule model and user_id
#         new_schedule = Schedule(user_id=current_user.id, date=new_date, amount=new_amount)
#         db.session.add(new_schedule)
#         db.session.commit()
#         return redirect(url_for('main.dashboard'))
#     return render_template('schedule.html')


# @main.route('/schedule', methods=['GET', 'POST'])
# @login_required
# def schedule():
#     form = ScheduleForm()
#     if form.validate_on_submit():
#         new_schedule = Schedule(user_id=current_user.id, date=form.date.data, amount=form.amount.data)
#         db.session.add(new_schedule)
#         db.session.commit()
#         flash('Schedule added successfully!')
#         return redirect(url_for('main.dashboard'))
#     return render_template('schedule.html', form=form)

# @main.route('/schedule', methods=['GET', 'POST'])
# @login_required
# def schedule():
#     form = ScheduleForm()
#     if form.validate_on_submit():
#         new_schedule = Schedule(
#             user_id=current_user.id,
#             group_id=form.group.data,
#             date=form.date.data,
#             amount=form.amount.data
#         )
#         db.session.add(new_schedule)
#         db.session.commit()
#         flash('Schedule added successfully!')
#         return redirect(url_for('main.dashboard'))
#     return render_template('schedule.html', form=form)


@main.route('/schedule', methods=['GET', 'POST'])
@login_required
def schedule():
    form = ScheduleForm()
    
    # Filter groups to only those the current user belongs to
    user_groups = Group.query.filter(Group.members.any(id=current_user.id)).all()
    form.group.choices = [(group.id, group.name) for group in user_groups]

    if form.validate_on_submit():
        new_schedule = Schedule(
            user_id=current_user.id,
            group_id=form.group.data,
            date=form.date.data,
            amount=form.amount.data
        )
        db.session.add(new_schedule)
        db.session.commit()
        flash('Schedule added successfully!')
        return redirect(url_for('main.dashboard'))

    return render_template('schedule.html', form=form, user_groups=user_groups)



@main.route('/reports')
@login_required
def reports():
    contributions = Contribution.query.filter_by(user_id=current_user.id).all()
    # Prepare data for visualization
    data = [{'date': c.date.strftime('%Y-%m-%d'), 'amount': c.amount} for c in contributions]
    return render_template('reports.html', data=data)


@main.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback():
    if request.method == 'POST':
        content = request.form['content']
        new_feedback = Feedback(user_id=current_user.id, content=content)
        db.session.add(new_feedback)
        db.session.commit()
        return redirect(url_for('main.dashboard'))
    return render_template('feedback.html')

@main.route('/user/invite')
@login_required
def user_invite():
    invite_link = url_for('main.register', _external=True) + '?ref=' + current_user.id
    return render_template('invite.html', invite_link=invite_link)






# @main.route('/join_group', methods=['GET', 'POST'])
# @login_required
# def join_group():
#     groups = Group.query.filter(~Group.members.contains(current_user)).all()
#     if request.method == 'POST':
#         group_id = request.form['group_id']
#         group = Group.query.get_or_404(group_id)
#         if current_user in group.members:
#             flash('You are already a member of this group.', 'info')
#             return redirect(url_for('main.group_detail', group_id=group_id))
        
#         # Create a join request
#         join_request = JoinRequest(user_id=current_user.id, group_id=group_id)
#         db.session.add(join_request)
#         db.session.commit()
#         flash('Join request sent.', 'success')
#         return redirect(url_for('main.group_detail', group_id=group_id))

#     form = JoinRequestForm()
    
#     return render_template('join_group.html',
#                            groups=groups,
#                            form=form)


@main.route('/join_group', methods=['GET', 'POST'])
@login_required
def join_group():
    groups = Group.query.filter(~Group.members.contains(current_user)).all()
    form = JoinRequestForm()
    
    # Populate the choices for the SelectField
    form.group_id.choices = [(group.id, group.name) for group in groups]
    
    if form.validate_on_submit():
        group_id = form.group_id.data
        group = Group.query.get_or_404(group_id)
        if current_user in group.members:
            flash('You are already a member of this group.', 'info')
            return redirect(url_for('main.group_detail', group_id=group_id))
        
        # Check if a join request already exists
        existing_request = JoinRequest.query.filter_by(user_id=current_user.id, group_id=group_id).first()
        if existing_request:
            flash('You have already requested to join this group.', 'info')
            return redirect(url_for('main.group_detail', group_id=group_id))

        # Create a new join request
        join_request = JoinRequest(user_id=current_user.id, group_id=group_id)
        db.session.add(join_request)
        db.session.commit()
        flash('Join request sent.', 'success')
        return redirect(url_for('main.group_detail', group_id=group_id))
    
    return render_template('join_group.html', groups=groups, form=form)