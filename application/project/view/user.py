from flask import Blueprint, redirect, render_template, url_for, request, flash , session 
from ..model.user import User
from ..form.user import  UserForm
from .. import db, log
from flask_login import login_user ,logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash



user=Blueprint('user',__name__)


@user.route('/user')
def index():
    users = User.query.all()
    return render_template('user/index.html', users=users)

@user.route('/user/add', methods=['POST', 'GET'])
def add():
    form = UserForm(request.form)
    if request.method == 'POST' and form.validate():
       
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            
            hashed_password = generate_password_hash(password, method='sha256')
            user = User(username,password=hashed_password)
            db.session.add(user)
            db.session.commit()

            log.info('[{0}] Az új felhasználó rögzítése sikeresen megtörtént: {1}'.format(current_user.username, username))

        except Exception as e:
            flash('Az új felhasználó rögzítése sikertelen   {0}'.format(e), 'danger')
            return redirect(url_for('user.index'))

        flash('Az új felhasználó rögzítése sikeresen megtörtént.', 'success')
        return redirect(url_for('user.index'))
    return render_template('user/add.html', form=form, user=None)


@user.route('/user/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    user = User.query.filter(User.id == id).first()
    if not user:
        flash('A felhasználó nem létezik.', 'danger')
        return redirect(url_for('user.index'))

    form = UserForm(obj=user)

    if request.method == 'POST' and form.validate():
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password, method='sha256')
        # user.username = username
        user.set_username_and_password(username,password=hashed_password)
        # user.set_username(username)
        # user.set_password(password)

        db.session.add(user)
        db.session.commit()
        flash('A felhasználót sikeresen módosítottuk.','success')
        return redirect(url_for('user.index'))

    return render_template('user/edit.html', form=form, user=user)


@user.route('/user/delete/<id>')
def delete(id):
    delete_user= User.query.filter(User.id == id).first()
    if current_user == delete_user:
        flash(' Saját magadat nem törölheted!' , 'danger')
        return redirect(url_for('user.index'))
    if not delete_user:
            flash('Nincs ilyen felhasználó.', 'danger')
            return redirect(url_for('user.index'))
    else:
        try:
            db.session.delete(delete_user)
            db.session.commit()
            flash('Az új felhasználót sikeresen töröltük.', 'success')
            return redirect(url_for('user.index'))
        except Exception as e:
            flash('Hiba lépett fel a törlés folyamán: {}'.format(e), 'danger')
            return redirect(url_for('user.index'))

        
