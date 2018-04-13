from flask import Flask, Markup, render_template, flash, redirect
from datetime import time
from forms import LoginForm


app = Flask(__name__)
app.config.update(dict(
    SECRET_KEY="powerful-secretkey",
    WTF_CSRF_SECRET_KEY="a-csrf-secret-key"
))


@app.route('/')
@app.route('/index')
def hello_world():
    return render_template('index.html')


@app.route('/chart')
def chart():
    times = ['','','','','','','','','']

    values = [10,9,8,7,6,4,7,8]
    return render_template('chart.html', values=values, labels=times)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(
            'Login requested for username="{0}", password="{1}", '
            'remember_me={2}'.format(
                form.username.data, form.password.data, form.remember_me.data
            )
        )
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)


if __name__ == '__main__':
    app.run()
