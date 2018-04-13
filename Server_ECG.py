from flask import Flask, Markup, render_template
from datetime import time

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def hello_world():
    return render_template('index.html')


@app.route('/chart')
def chart():
    times = ['','','','','','','','','']

    values = [10,9,8,7,6,4,7,8]
    return render_template('chart.html', values=values, labels=times)


if __name__ == '__main__':
    app.run()
