from .user import User
from ..extensions import db
from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

user_management = Blueprint('user_management', __name__, template_folder = 'templates')

@user_management.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user_management.login'))
    return render_template('register.html')


@user_management.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('main.index'))
    return render_template('login.html')
