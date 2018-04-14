from flask import Flask, render_template, flash, redirect, jsonify, abort, \
    request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user, logout_user, \
    login_required
from werkzeug.security import generate_password_hash


app = Flask(__name__)
app.config.update(
    dict(
        SECRET_KEY="powerful-secretkey",
        WTF_CSRF_SECRET_KEY="a-csrf-secret-key",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_DATABASE_URI="mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}".format('root', 'myivan', 'localhost', '3306', 'ecg_db')
    )
)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

import models
import forms


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(user_id)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home Page')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/index')
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.username.data).first()
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
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        user = models.User(email=form.email.data)
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
    user = models.User.query.filter_by(id=id).first_or_404()

    query = db.session.query(models.EcgDate).filter_by(user_id=user.id).all()
    if not query:
        query = query[-1]
        data = query.data
        values = list(zip(data.split()[::2], data.split()[1::2]))
    else:
        values = []
    return render_template('chart.html', values=values)


@app.route('/api/v1.0/ecg_data', methods=['GET'])
def get_user():
    return jsonify({'user': 'pidor'})


@app.route('/api/v1.0/users', methods=['POST'])
def create_user():
    # print(request.json)
    # TODO login from api
    if not request.json or 'name' not in request.json:
        abort(400)
    worker = DbWorker()
    new_user = worker.add_new_user(request.json['name'],
                                   request.json.get('description', None))
    return jsonify({'user': new_user}), 201


@app.route('/api/v1.0/ecg_data', methods=['POST'])
def add_ecg_data():
    if not request.json or 'data' not in request.json or \
            'email' not in request.json or \
            'password' not in request.json:
        abort(400)
    user = db.session.query(models.User).filter_by(
        email=request.json['email']).one()
    if not user.check_password(request.json['password']):
        abort(401)
    db.session.add(
        models.EcgDate(
            data=request.json['data'],
            user_id=user.id
        )
    )
    db.session.commit()
    return "OK", 201


if __name__ == '__main__':
    app.run()
