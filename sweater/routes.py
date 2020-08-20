from flask import request, render_template, redirect, url_for, flash
from flask_login import login_user
from werkzeug.security import chech_password_hash

from models import User
from sweater import app, db
from sweater.models import Message


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


@app.route('/login', methods=['GET','POST'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = User.query.filter_by(login=login).first()
        if chech_password_hash(user.password, password):
            login_user(user)

            next_page = request.args.get('next')

            redirect(next_page)
        else:
            flash('Login or password is incorrect')
    else:
        flash('Please enter the correct login and password')

        return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    pass
@app.route('/logout', methods=['GET','POST'])
def logout():
    pass
