from .user import User
from ..extensions import db
from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import login_user, logout_user, login_required

user_management = Blueprint('user_management', __name__, template_folder='templates')

@user_management.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conf_password = request.form['conf_password']
        if password == conf_password:
            user = User(email=email, password=password)
            db.session.add(user)
            db.session.commit()
            alert = "Udało Ci się założyć konto!" \
                    "Możesz się zalogować"
            return render_template('login.html', alert=alert)
        else:
            email = request.form['email']
            alert = "Hasła różnią się od siebie!"
            return render_template('register.html', alert=alert, last_email=email)
    return render_template('register.html')


@user_management.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            login_user(user)
            alert = "Udało Ci się zalogować!"
            return render_template('index.html', alert=alert)
        else:
            alert = "Błędne dane logowania!"
            return render_template('login.html', alert=alert)
    return render_template('login.html')

@user_management.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

