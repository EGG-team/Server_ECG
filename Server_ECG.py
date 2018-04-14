from flask import Flask, render_template, flash, redirect
from forms import LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user
from models import User


app = Flask(__name__)
app.config.update(
    dict(
        SECRET_KEY="powerful-secretkey",
        WTF_CSRF_SECRET_KEY="a-csrf-secret-key",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_DATABASE_URI="mysql+mysqlconnector://root:myivan@localhost/ecg_db"
    )
)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Ivan'}
    return render_template('index.html', user=user)


@app.route('/chart')
def chart():
    times = ['','','','','','','','','']

    values = [10,9,8,7,6,4,7,8]
    return render_template('chart.html', values=values, labels=times)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/index')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect('/index')
        login_user(user, remember=form.remember_me.data)
        return redirect('/index')

    return render_template('login.html', title='Sign in', form=form)


if __name__ == '__main__':
    app.run()
