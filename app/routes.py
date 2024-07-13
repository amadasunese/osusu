from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from . import db, bcrypt
from .models import User, Group, Contribution, Feedback, Schedule, JoinRequest, group_members
from app.models import Transaction, Role, JoinRequestStatus
from flask_mail import Message
from . import mail
from . import create_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import RegistrationForm, LoginForm, ProfileForm, CreateGroupForm, AddMemberForm
from app.forms import FeedbackForm, ScheduleForm, JoinRequestForm, EditUserForm, TransactionForm
from werkzeug.security import generate_password_hash, check_password_hash

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


@main.route('/about')
# @login_required
def about():
    return render_template('about.html')

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

# @main.route('/dashboard')
# @login_required
# def dashboard():
#     user_group_ids = [group.id for group in current_user.groups]
#     available_groups = Group.query.filter(~Group.id.in_(user_group_ids)).all()
#     join_requests = JoinRequest.query.filter_by(group_id=current_user.id).all()
    
#     contributions = Contribution.query.filter_by(user_id=current_user.id).all()
#     form = FeedbackForm()
#     users = User.query.all()
#     pending_requests = JoinRequest.query.filter_by(status=JoinRequestStatus.PENDING).all()
#     return render_template('dashboard.html', 
#                            available_groups=available_groups, 
#                            join_requests=join_requests,
#                            contributions=contributions,
#                            form=form,
#                            users=users,
#                            pending_requests=pending_requests)

@main.route('/dashboard')
@login_required
def dashboard():
    user_group_ids = [group.id for group in current_user.groups]
    available_groups = Group.query.filter(~Group.id.in_(user_group_ids)).all()
    
    join_requests = JoinRequest.query.filter_by(user_id=current_user.id).all()
    contributions = Contribution.query.filter_by(user_id=current_user.id).all()
    form = FeedbackForm()
    users = User.query.all()
    pending_requests = JoinRequest.query.filter_by(status=JoinRequestStatus.PENDING).all()
    
    return render_template('dashboard.html', 
                           available_groups=available_groups, 
                           join_requests=join_requests,
                           contributions=contributions,
                           form=form,
                           users=users,
                           pending_requests=pending_requests)

@main.route('/users')
@login_required
def list_users():
    users = User.query.all()
    form = EditUserForm()
    return render_template('list_users.html',
                           users=users,
                           form=form)


# @main.route('/user/<int:user_id>/edit', methods=['GET', 'POST'])
# @login_required
# def edit_user(user_id):
#     user = User.query.get_or_404(user_id)
#     form = EditUserForm(obj=user)
#     if form.validate_on_submit():
#         user.username = form.username.data
#         user.email = form.email.data
#         user.role = form.role.data
#         user.is_admin = form.is_admin.data
#         user.fullname = form.fullname.data
#         user.phonenumber = form.phonenumber.data
#         db.session.commit()
#         flash('User details updated successfully.', 'success')
#         return redirect(url_for('main.list_users'))
#     return render_template('edit_user.html', form=form, user=user)


# @main.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
# def edit_user(user_id):
#     user = User.query.get_or_404(user_id)
#     form = EditUserForm(obj=user)

#     if form.validate_on_submit():
#         user.username = form.username.data
#         user.email = form.email.data
#         user.role = form.role.data
#         user.is_admin = form.is_admin.data
#         user.fullname = form.fullname.data
#         user.phonenumber = form.phonenumber.data

#         if form.current_password.data and form.new_password.data:
#             if user.verify_password(form.current_password.data):
#                 user.set_password(form.new_password.data)
#             else:
#                 flash('Current password is incorrect', 'danger')
#                 return render_template('edit_user.html', form=form, user=user)
        
#         db.session.commit()
#         flash('User details updated successfully', 'success')
#         return redirect(url_for('main.user_profile', user_id=user.id))

#     return render_template('edit_user.html', form=form, user=user)

# @main.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
# def edit_user(user_id):
#     user = User.query.get_or_404(user_id)
#     form = EditUserForm(obj=user)

#     if form.validate_on_submit():
#         user.username = form.username.data
#         user.email = form.email.data
#         user.role = Role[form.role.data]  # Converting string to Role Enum
#         user.is_admin = form.is_admin.data
#         user.fullname = form.fullname.data
#         user.phonenumber = form.phonenumber.data

#         if form.current_password.data and form.new_password.data:
#             if user.verify_password(form.current_password.data):
#                 user.set_password(form.new_password.data)
#             else:
#                 flash('Current password is incorrect', 'danger')
#                 return render_template('edit_user.html', form=form, user=user)
        
#         db.session.commit()
#         flash('User details updated successfully', 'success')
#         return redirect(url_for('edit_user', user_id=user.id))

#     return render_template('edit_user.html', form=form, user=user)


@main.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = EditUserForm(obj=user)

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.role = Role[form.role.data]  # Converting string to Role Enum
        user.is_admin = form.is_admin.data
        user.fullname = form.fullname.data
        user.phonenumber = form.phonenumber.data

        if form.current_password.data and form.new_password.data:
            if user.verify_password(form.current_password.data):
                user.set_password(form.new_password.data)
            else:
                flash('Current password is incorrect', 'danger')
                return render_template('edit_user.html', form=form, user=user)
        
        db.session.commit()
        flash('User details updated successfully', 'success')
        return redirect(url_for('main.list_users', user_id=user.id))

    return render_template('edit_user.html', form=form, user=user)



@main.route('/user/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully.', 'success')
    return redirect(url_for('main.list_users'))



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
        user = User(username=form.username.data,
                    email=form.email.data,
                    hashed_password=hashed_password,
                    fullname=form.fullname.data,
                    phonenumber=form.phonenumber.data)
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


###########################
# Admin management        #
###########################

@main.route("/admin/dashboard")
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.dashboard'))
    users = User.query.all()
    transactions = Transaction.query.order_by(Transaction.date.desc()).all()
    return render_template('admin_dashboard.html', users=users, transactions=transactions)



############################
# Create and Manage groups #
############################

# Group creation
@main.route('/create_group', methods=['GET', 'POST'])
@login_required
def create_group():
    form = CreateGroupForm()
    """
    Populate the members field with all users except the current user
    """
    form.members.choices = [(user.id, user.username) for user in User.query.filter(User.id != current_user.id).all()]

    if form.validate_on_submit():
        group = Group(name=form.name.data, created_by=current_user.id)
        db.session.add(group)
        db.session.commit()

        """
        Add selected members to the group
        """
        for user_id in form.members.data:
            group_member = group_members.insert().values(user_id=user_id, group_id=group.id)
            db.session.execute(group_member)
        
        """
        Add the current user (creator) to the group
        """
        group_member = group_members.insert().values(user_id=current_user.id, group_id=group.id)
        db.session.execute(group_member)
        
        db.session.commit()
        flash('Group created successfully!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('create_group.html', form=form)


# # View list of existing groups
# @main.route('/group_list')
# def group_list():
#     groups = Group.query.all()
#     users = User.query.all()
#     return render_template('group_list.html',
#                            groups=groups,
#                            users=users)


@main.route('/group_list')
@login_required
def group_list():
    groups = Group.query.all()
    user_dict = {user.id: user.username for user in User.query.all()}
    return render_template('group_list.html', groups=groups, user_dict=user_dict)


# Add members to the group
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


# Remove member(s) from a group
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


# Delete unwanted group
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


# Show details of each group
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


# Allow users to join group of their choice
@main.route('/join_group', methods=['GET', 'POST'])
@login_required
def join_group():
    groups = Group.query.filter(~Group.members.contains(current_user)).all()
    form = JoinRequestForm()
    
    """
    Populate the choices for the SelectField
    """
    form.group_id.choices = [(group.id, group.name) for group in groups]
    
    if form.validate_on_submit():
        group_id = form.group_id.data
        group = Group.query.get_or_404(group_id)
        if current_user in group.members:
            flash('You are already a member of this group.', 'info')
            return redirect(url_for('main.group_detail', group_id=group_id))
        
        """
        Check if a join request already exists
        """
        existing_request = JoinRequest.query.filter_by(user_id=current_user.id, group_id=group_id).first()
        if existing_request:
            flash('You have already requested to join this group.', 'info')
            return redirect(url_for('main.group_detail', group_id=group_id))

        """
        Create a new join request
        """
        join_request = JoinRequest(user_id=current_user.id, group_id=group_id)
        db.session.add(join_request)
        db.session.commit()
        flash('Join request sent.', 'success')
        return redirect(url_for('main.group_detail', group_id=group_id))
    
    return render_template('join_group.html', groups=groups, form=form)


# Manage join group request from users
@main.route('/group/<int:group_id>/manage_requests')
@login_required
def manage_requests(group_id):
    group = Group.query.get_or_404(group_id)
    if current_user.id != group.created_by and not current_user.is_admin:
        abort(403)

    join_requests = JoinRequest.query.filter_by(group_id=group_id, status='pending').all()
    form = JoinRequestForm()
    return render_template('manage_requests.html',
                           group=group,
                           join_requests=join_requests,
                           form=form)


# Approve request to join group
@main.route('/group/<int:group_id>/approve_request/<int:request_id>', methods=['POST'])
@login_required
def approve_request(group_id, request_id):
    join_request = JoinRequest.query.get_or_404(request_id)
    group = Group.query.get_or_404(group_id)
    if current_user.id != group.created_by and not current_user.is_admin:
        abort(403)

    join_request.status = JoinRequestStatus.APPROVED
    group.members.append(join_request.user)
    db.session.commit()
    flash('Join request approved.', 'success')
    return redirect(url_for('main.manage_requests', group_id=group_id))


# Deny request to join group
@main.route('/group/<int:group_id>/deny_request/<int:request_id>', methods=['POST'])
@login_required
def deny_request(group_id, request_id):
    join_request = JoinRequest.query.get_or_404(request_id)
    group = Group.query.get_or_404(group_id)
    if current_user.id != group.created_by and not current_user.is_admin:
        abort(403)

    join_request.status = JoinRequestStatus.DENIED
    db.session.commit()
    flash('Join request denied.', 'info')
    return redirect(url_for('main.manage_requests', group_id=group_id))



# Group Contribution Roaster
@main.route('/group/<int:group_id>/roster')
@login_required
def roster(group_id):
    group = Group.query.get_or_404(group_id)
    return render_template('roster.html', group=group)


# Group payment schedule
@main.route('/schedule', methods=['GET', 'POST'])
@login_required
def schedule():
    form = ScheduleForm()
    
    """
    Filter groups to only those the current user belongs to
    """
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


# Report of contribution
@main.route('/reports')
@login_required
def reports():
    contributions = Contribution.query.filter_by(user_id=current_user.id).all()
    """
    Prepare data for visualization
    """
    data = [{'date': c.date.strftime('%Y-%m-%d'), 'amount': c.amount} for c in contributions]
    return render_template('reports.html', data=data)


# Members/Users feedback
# @main.route('/feedback', methods=['GET', 'POST'])
# @login_required
# def feedback():
#     if request.method == 'POST':
#         content = request.form['content']
#         new_feedback = Feedback(user_id=current_user.id, content=content)
#         db.session.add(new_feedback)
#         db.session.commit()
#         return redirect(url_for('main.dashboard'))
#     return render_template('feedback.html')


# Invitation to register and join a group
@main.route('/user/invite')
@login_required
def user_invite():
    invite_link = url_for('main.register', _external=True) + '?ref=' + current_user.id
    return render_template('invite.html', invite_link=invite_link)





@main.route('/submit_feedback', methods=['GET', 'POST'])
@login_required
def submit_feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        feedback = Feedback(user_id=current_user.id, content=form.content.data)
        db.session.add(feedback)
        db.session.commit()
        flash('Feedback submitted successfully', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('feedback.html', form=form)



# @main.route("/add_contribution", methods=['GET', 'POST'])
# @login_required
# def add_contribution():
#     form = TransactionForm()
#     if form.validate_on_submit():
#         transaction = Transaction(amount=form.amount.data, type='contribution', description=form.description.data, user_id=current_user.id)
#         db.session.add(transaction)
#         db.session.commit()
#         flash('Your contribution has been added successfully!', 'success')
#         return redirect(url_for('dashboard'))
#     return render_template('add_transaction.html', title='Add Contribution', form=form)

@main.route('/add_contribution', methods=['GET', 'POST'])
def add_contribution():
    form = TransactionForm()
    
    # Assume you have the user_id available
    user_id = current_user.id  # Replace with actual user_id
    
    # Fetch the groups the user belongs to
    user_groups = Group.query.join(group_members).filter(group_members.c.user_id == user_id).all()
    
    # Populate group choices
    form.group_id.choices = [(group.id, group.name) for group in user_groups]
    
    if request.method == 'GET':
        form.user_id.data = user_id

    if form.validate_on_submit():
        transaction = Transaction(
            amount=form.amount.data,
            description=form.description.data,
            user_id=form.user_id.data,
            group_id=form.group_id.data
        )
        db.session.add(transaction)
        db.session.commit()
        return redirect(url_for('index'))  # Redirect to an appropriate page

    return render_template('add_transaction.html', form=form)