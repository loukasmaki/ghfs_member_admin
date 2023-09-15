from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

# Secret key expected by wtforms REMEMBER TO CHANGE WHEN DEPLOYING ALSO WILL BE UPDATED WITH A SAFER APPROACH LATER
app.config['SECRET_KEY'] = 'hard to guess string'


# Forms

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

class RegisterAttendance(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    course = SelectField('Course', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Routes

@app.route('/', methods=['GET', 'POST'])
def index():
    
# Kolla mer på hur forms fungerar WTForms
    form = RegisterAttendance()
    if form.validate_on_submit():
        old.name = session.get('name')
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
