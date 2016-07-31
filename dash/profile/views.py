import datetime
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import profile
from .. import db
from ..models import User
from ..email import send_email
from .forms import ChangePasswordForm, UpdateProfileForm


@profile.route('/', methods=['GET', 'POST'])
@login_required
def index():
    change_password = ChangePasswordForm()
    update_profile = UpdateProfileForm()
    
    if change_password.validate_on_submit():
        if current_user.verify_password(change_password.old_password.data):
            current_user.password = change_password.password.data
            db.session.add(current_user)
            flash('Your password has been changed.')
            send_email(current_user.email, 'You Password has Changed', 
               'profile/email/password_changed', user=current_user)
            return redirect(url_for('profile.index'))
        else:
            flash('Invalid password')
    return render_template('profile/index.html',
                            update_profile=update_profile,
                            change_password=change_password)
