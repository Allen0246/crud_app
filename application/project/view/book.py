from flask import Blueprint, redirect, render_template, url_for, request, flash
from .auth import error_handler
from ..model.book import Book
from ..form.book import  BookForm
from flask_login import login_user ,logout_user, login_required, current_user
from .. import db

book=Blueprint('book',__name__)

@book.route('/book')
@login_required 
@error_handler()
def index():
    books=Book.query.all()
    return render_template('book/index.html', books=books)

@book.route('/book/add', methods=['POST', 'GET'])
@login_required
def add():
    form = BookForm(request.form)
    if request.method == 'POST' and form.validate():

        szerzo = request.form.get('szerzo')
        cim = request.form.get('cim')

        book = Book(szerzo,cim)
        db.session.add(book)
        db.session.commit()

        flash('Az új könyv rögzítése sikeresen megtörtént.', 'success')
        return redirect(url_for('book.index'))
    return render_template('book/add.html' , form=form, book=None)

@book.route('/book/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    book = Book.query.filter(Book.id == id).first()
    if not book:
        flash('A könyv nem létezik.', 'danger')
        return redirect(url_for('book.index'))

    form = BookForm(obj=book)

    if request.method == 'POST' and form.validate():
        szerzo = request.form.get('szerzo')
        cim = request.form.get('cim')
        book.set_author(szerzo)
        book.set_tittle(cim)

        db.session.add(book)
        db.session.commit()
        flash('A könyvet sikeresen módosítottuk.','success')
        return redirect(url_for('book.index'))

    return render_template('book/edit.html', form=form, book=book)



@book.route('/book/delete/<id>')
@login_required
def delete(id):
    delete_book= Book.query.filter(Book.id == id).first()
    if not delete_book :
        flash('Nincs ilyen könyv.', 'danger')
        return redirect(url_for('book.index'))
    else:
        try:
            db.session.delete(delete_book)
            db.session.commit()
            flash('Az új könyvet sikeresen töröltük.', 'success')
            return redirect(url_for('book.index'))
        except Exception as e:
            flash('Hiba lépett fel a törlés folyamán: {}'.format(e), 'danger')
            return redirect(url_for('book.index'))