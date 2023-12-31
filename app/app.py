from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired
import os
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

# Database stuff
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Secret key expected by wtforms REMEMBER TO CHANGE WHEN DEPLOYING ALSO WILL BE UPDATED WITH A SAFER APPROACH LATER
app.config['SECRET_KEY'] = 'hard to guess string'


# Forms

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

class RegisterAttendance(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    course = SelectField(u'Course', choices=[('LS', 'Långsvärd'), ('SOB', 'Svärd och Bucklare'), ('Sabel', 'Sabel')], validators=[DataRequired()])
    submit = SubmitField('Submit')

# Routes

@app.route('/', methods=['GET', 'POST'])
def index():
    
# Kolla mer på hur forms fungerar WTForms
    form = RegisterAttendance()
    if form.validate_on_submit():
        # Want a query where I check if a person with the same name already has registered 
        attendandee = Attendance.query.filter_by()
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        session['date'] = form.date.data
        session['course'] = form.course.data
        return redirect(url_for('index'))
    user_agent = request.headers.get('User-Agent')
    return render_template('index.html', user_agent=user_agent, name=session.get('name'), form=form)


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

# Errorhandler

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# Database models

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__ (self):
        return '<User %r>' % self.username
    

class Attendance(db.Model):
    __tablename_ = 'attendance_registered'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    date = db.Column(db.Date)
    course = db.Column(db.Integer)