import os

from flask import Flask, render_template, request, flash, redirect, jsonify
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from werkzeug.utils import secure_filename

from forms import UserForm


app = Flask(__name__)
Bootstrap(app)
app.config.from_pyfile('settings.py')
db = SQLAlchemy(app)
jwt = JWTManager(app)
ma = Marshmallow(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))


db.create_all()


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        load_only = ('password',)


user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route('/')
def home():
    return render_template('base.html')


@app.route('/user/', methods=['GET', 'POST'])
def greetings():
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(data=request.form)
        name = request.form.get('name', None)
        if form.validate():
            user = User()
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.email = form.email.data
            user.password = form.password.data
            db.session.add(user)
            db.session.commit()
            return redirect(f'/user/{user.id}/')
    return render_template('user.html', form=form)


@app.route('/user/<user_id>/')
def user_detail(user_id):
    user = db.session.query(User).filter_by(id=user_id).first()
    return render_template('user_detail.html', user=user)


@app.route('/users/')
@jwt_required
def user_list():
    users_list = User.query.all()
    users = users_schema.dump(users_list)
    return jsonify(users)


@app.route('/user_edit/<user_id>/', methods=['GET', 'POST'])
def user_edit(user_id):
    user = db.session.query(User).filter_by(id=user_id).first()
    form = UserForm(obj=user)
    if request.method == 'POST':
        form = UserForm(data=request.form)
        if form.validate():
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            db.session.add(user)
            db.session.commit()
            return redirect(f'/user/{user.user_id}/')
    return render_template('user_edit.html', form=form)


@app.route('/user/<user_id>/delete/', methods=['GET', 'POST'])
def user_delete(user_id):
    user = db.session.query(User).filter_by(id=user_id).first()
    if request.method == 'POST':
        db.session.delete(user)
        db.session.commit()
        return redirect('/users/')
    return render_template('confirm_delete.html', user=user)


@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No File part')
            return redirect(request.url)
        file = request.files['file']
        if not file.filename:
            flash('No file selected')
            return redirect(request.url)
        print(file)
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template('upload_file.html')


@app.route('/register/', methods=['POST'])
def register():
    email = request.form['email']
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify(message='Email already exists.'), 409
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        user = User(first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify(message='User created successfully'), 201


@app.route('/login/', methods=['POST'])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']
    user = User.query.filter_by(email=email, password=password).first()
    if user:
        access_token = create_access_token(identity=email)
        return jsonify(message="Login successful", access_token=access_token)
    else:
        return jsonify(message='Invalid credentials.'), 401
