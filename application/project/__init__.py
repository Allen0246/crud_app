from flask import Flask, render_template, session, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import timedelta


app = Flask(__name__, instance_relative_config=True)
app.config.from_object('project.config.config')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)

# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://crud:jelszo123@localhost:5432/crud"
db = SQLAlchemy(app)

#LOGINMANAGER
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'A megtekintéshez lépjen be!'
login_manager.refresh_view = 'auth.login'
login_manager.needs_refresh_message = 'Lépjen be újra!'
login_manager.init_app(app)

## LOGGING
from .extensions.logging import create_log_file
# CREATE SYSTEM LOG
log = create_log_file('CRUD_APP_LOG')
log.info('Start...')


# MODEL
from .model.user import User
from .model.book import Book


# CREATE TABLES
db.create_all()
db.session.commit()


# VIEW/BLUEPRINT
from .view.user import user
from .view.book import book
from .view.auth import auth


# BLUEPRINTS
app.register_blueprint(user)
app.register_blueprint(book)
app.register_blueprint(auth)


# MAIN ROUTE
@app.route('/')
def index():
    return render_template ('home.html')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# LOG OUT AFTER 100 MINUTES
@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=100)


# 404 MESSAGE
@app.errorhandler(404)
def page_not_found(e):
    flash('code: 404, title: Page not found.','danger')
    return redirect(url_for('index'))

# GENERAL ERROR HANDLER
@app.errorhandler(Exception)
def handle_exception(e):
    flash('EZT HASZNÁLJA:{}'.format(e),'danger')
    return redirect(url_for('index'))


@app.template_filter('uppercase')
def timectime(char):
    try:
        char = char.upper()
    except Exception as e:
        log.critical(e)
        char = ''
    return char