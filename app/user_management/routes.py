from .user import User
from ..extensions import db
from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_user, logout_user, login_required
from urllib.parse import urlparse
import re

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
            flash("Udało Ci się założyć konto!\nMożesz się zalogować.", 'mess')
            return redirect(url_for('user_management.login'))
        else:
            email = request.form['email']
            flash("Hasła różnią się od siebie!", 'error')
            return render_template('register.html', last_email=email)
    return render_template('register.html')


@user_management.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        path = urlparse(request.referrer)
        if user and user.password == password:
            if 'follow' in path.path:
                tripID = int(re.findall(r'\d+\b', path.path)[0])
                login_user(user)
                return redirect(url_for('trips.follow', tripID=tripID))
            else:
                login_user(user)
                flash("Udało Ci się zalogować!", 'mess')
                return redirect(url_for('main.index'))

        else:
            flash("Błędne dane logowania!", 'error')
            return redirect(url_for('user_management.login'))
    return render_template('login.html')

@user_management.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Wylogowałeś się!", 'mess')
    return redirect(url_for('main.index'))

