from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/simple_chart')
def chart():
    values = [0,1,2,3,4,5,6,7,8,9]
    return render_template('chart.html', values = values)


if __name__ == '__main__':
    app.run()
