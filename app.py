from flask import Flask, render_template, request, flash, redirect
from flask_bootstrap import Bootstrap
from wtforms import Form, StringField

from models import User, Session
from forms import UserForm


app = Flask(__name__)
Bootstrap(app)
app.config.from_pyfile('settings.py')


@app.route('/')
def home():
    return render_template('base.html')


@app.route('/user/', methods=['GET', 'POST'])
def greetings():
    session = Session()
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(data=request.form)
        name = request.form.get('name', None)
        if form.validate():
            user = User()
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.username = form.username.data
            session.add(user)
            session.commit()
            return redirect(f'/user/{user.username}/')
    return render_template('user.html', form=form)


@app.route('/user/<username>/')
def user_detail(username):
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    return render_template('user_detail.html', user=user)


@app.route('/users/')
def user_list():
    session = Session()
    users = session.query(User).all()
    return render_template('user_list.html', users=users)


@app.route('/user_edit/<username>/', methods=['GET', 'POST'])
def user_edit(username):
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    form = UserForm(obj=user)
    if request.method == 'POST':
        form = UserForm(data=request.form)
        if form.validate():
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            session.add(user)
            session.commit()
            return redirect(f'/user/{user.username}/')
    return render_template('user_edit.html', form=form)


@app.route('/user/<username>/delete/', methods=['GET', 'POST'])
def user_delete(username):
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    if request.method == 'POST':
        session.delete(user)
        session.commit()
        return redirect('/users/')
    return render_template('confirm_delete.html', user=user)
