from collections import namedtuple
from flask import Flask, request, render_template, redirect, url_for


app = Flask(__name__)

Message = namedtuple('Message', 'text tag')
messages =[]


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/hello', methods=['GET'])
def hello():
    return render_template('hello.html', messages=messages)


@app.route('/add_message', methods=['POST'])
def add_message():
    text = request.form['text']
    tag = request.form['tag']
    messages.append(Message(text, tag))

    return redirect(url_for('hello'))

# $ env FLASK_APP=hello.py flask run
#  * Serving Flask app "hello"
#  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
