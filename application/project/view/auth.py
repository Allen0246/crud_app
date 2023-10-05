from flask import Blueprint, redirect, render_template, url_for, request, flash
from project.model.user import User
from ..form.register import  RegisterForm
from ..form.login import LoginForm
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user ,logout_user, login_required
from .. import db, log
from functools import wraps

auth = Blueprint('auth', __name__)

@auth.route('/register' , methods=['POST', 'GET'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if username and password and confirm_password:
            if password == confirm_password:
                hashed_password = generate_password_hash(password, method='sha256')
                print(hashed_password)
                try:
                    new_user = User(
                        username=username,
                        password=hashed_password,
                    )
                    db.session.add(new_user)
                    db.session.commit()
                except Exception as e:
                    flash('FELHASZNÁLÓ LÉTEZIK MÁR ! : {0}'.format(e), 'danger')
                    return redirect(url_for('auth.register'))

            else:
                flash('A kettő jelszó nem egyezik, próbálja újra ! ' , 'danger')
                return redirect(url_for('auth.register'))

        flash('Sikeres regisztráció !', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form = form)

@auth.route('/login', methods= ['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Sikeres bejelentkezés !' , 'success')
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash('HIBÁS JELSZÓ ! ', 'danger')
                return redirect(url_for('auth.login'))
        else:
            flash('FELHASZNÁLÓ NEM TALÁLHATÓ !' , 'danger')
            return redirect(url_for('auth.login'))
    else:
        return render_template('login.html', form = form) 


@auth.route('/logout')
@login_required 
def logout():
    logout_user()
    flash ('Sikeres kijelentkezés !', 'success')
    return redirect (url_for('index'))


# ERROR HANDLER DECORATOR
def error_handler():
    def _error_handler(f):
        @wraps(f)
        def decorated_view(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                log.info(e)
                flash('Unknown error: {}'.format(e),'danger')
                return redirect(url_for('index'))
        return decorated_view
    return _error_handler

