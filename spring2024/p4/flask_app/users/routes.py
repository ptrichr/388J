from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user
import base64
from io import BytesIO
from .. import bcrypt
from werkzeug.utils import secure_filename
from ..forms import RegistrationForm, LoginForm, UpdateUsernameForm, UpdateProfilePicForm
from ..models import User

users = Blueprint("users", __name__)

""" ************ User Management views ************ """


# TODO: implement
@users.route("/register", methods=["GET", "POST"])
def register():
    # if user is already logged in, send to home page
    if current_user.is_authenticated:
        return redirect(url_for('movies.index'))
    
    form = RegistrationForm()
    
    # if form submission details are alright save in db
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, 
                    email=form.email.data, 
                    password=hashed)
        user.save()
        
        #redirect to login page
        return redirect(url_for('users.login'))
    
    # otherwise re-render page
    return render_template('register.html', title="Register", form=form)


# TODO: implement the form
@users.route("/login", methods=["GET", "POST"])
def login():
    # if user is already logged in, send to home page
    if current_user.is_authenticated:
        return redirect(url_for('movies.index'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()
        
        if (user is not None and bcrypt.check_password_hash(user.password, form.password.data)):
            login_user(user)
            return redirect(url_for('users.account'))
        else:
            flash(message="Authentication Error. Please Try Logging in Again")
    
    return render_template('login.html', title="Login", form=form)


# TODO: implement
@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('movies.index'))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    update_username_form = UpdateUsernameForm()
    update_profile_pic_form = UpdateProfilePicForm()
    
    if request.method == "POST":        
        if update_username_form.submit_username.data and update_username_form.validate():
            # TODO: handle update username form submit
            current_user.modify(username=update_username_form.username.data)
            
        if update_profile_pic_form.submit_picture.data and update_profile_pic_form.validate():
            # TODO: handle update profile pic form submit
            img = update_profile_pic_form.picture.data   # get submitted img
            filename = secure_filename(img.filename)  # get the filename securely
            content_type = f'images/{filename[-3:]}'  # get the extension via slice
            
            if current_user.profile_pic.get() is None:
                current_user.profile_pic.put(img.stream, content_type=content_type)
            else:
                current_user.profile_pic.replace(img.stream, content_type=content_type)
        
            current_user.save()
            
        if not update_username_form.errors:
            return redirect(url_for('users.account'))  # redirect to reflect changes

    # TODO: handle get requests
    
    # encodes the image in base64
    b = BytesIO(current_user.profile_pic.read())
    pfp_encode = base64.b64encode(b.getvalue()).decode()
    
    # render the page with any image updates, or the old image
    return render_template('account.html', 
                           image=pfp_encode, 
                           update_username_form=update_username_form, 
                           update_profile_pic_form=update_profile_pic_form)