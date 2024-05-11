from flask import Response, render_template, redirect, url_for, current_app, stream_with_context, request
from flask_login import login_user, current_user, login_required

from auth.forms import LoginForm
from auth.models import User


import sqlalchemy
from typing import Iterator
import time
import json
import os
from datetime import timedelta


@current_app.before_request
def make_session_permanent():
    current_app.permanent_session_lifetime = timedelta(minutes=15)

@current_app.route('/login', methods=['GET', 'POST'])
def login() -> str:
    if current_user.is_authenticated: return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = current_app.login_database.session.scalar(sqlalchemy.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password_hash(form.password.data): return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@current_app.route('/')
@current_app.route('/index')
@login_required
def index() -> str:
    return render_template('index.html')