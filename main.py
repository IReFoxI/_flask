from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
# from main import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:654321qweR@localhost/flask_chat'
db = SQLAlchemy(app)

# костыльная БД >
# Message = namedtuple('Message', 'text tag')
# messages =[]


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1024), nullable=False)

    def __init__(self, text, tags):
        self.text = text.strip()
        self.tags = [
            Tag(tag.strip()) for tag in tags.split(',')
        ]


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(32), nullable=False)

    message_id = db.Column(db.Integer, db.ForeignKey('message.id'), nullable=False)
    message = db.relationship('Message', backref=db.backref('tags', lazy=True))


db.create_all()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/hello', methods=['GET'])
def hello():
    return render_template('hello.html', messages=Message.query.all())


@app.route('/add_message', methods=['POST'])
def add_message():
    text = request.form['text']
    tag = request.form['tag']

    db.session.add(Message(text, tag))
    db.session.commit()

    return redirect(url_for('hello'))

# $ env FLASK_APP=hello.py flask run
#  * Serving Flask app "hello"
#  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
