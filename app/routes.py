# -*- coding: utf-8 -*-
from math import log

from flask import render_template, flash, redirect, abort
from flask_login import current_user, login_user, logout_user, \
    login_required

from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, EcgDate


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home Page')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/index')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect('/index')
        login_user(user, remember=form.remember_me.data)
        return redirect('/index')

    return render_template('login.html', title='Sign in', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/index')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/index')
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect('/login')
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<int:id>')
@login_required
def profile(id):
    if current_user.id != id:
        abort(403)
    user = User.query.filter_by(id=id).first_or_404()

    query = db.session.query(EcgDate).filter_by(user_id=user.id).all()
    if query:
        query = query[-1]
        data = query.data
        xs = data.split()[::2]
        ys = list(map(int, data.split()[1::2]))
        ys = list(map(lambda y: log(y - 1000) - 1, ys))
        values = list(zip(xs, ys))
    else:
        values = []
    return render_template('chart.html', values=values)


@app.route('/api_help')
def api_help():
    return render_template('api_help.html')
