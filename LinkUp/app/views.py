#!env/bin/python
from flask import render_template, flash, redirect, g
from app import app, db
from .forms import LoginForm, EventForm
from .models import Event
from config import EVENTS_PER_PAGE

@app.route('/')
@app.route('/<int:page>')
def index(page=1):
    user = {'nickname': 'milla'} # fake user
    # to be changed
    events = Event.query.order_by(Event.id.desc()).paginate(page, EVENTS_PER_PAGE, False)
    # to events = Events.query.get(Chiquery) in the models file

    return render_template('index.html',
                            title='Home',
                            user=user,
                            events=events)


# work still needs to be done one this
# method.
# users should be able to log in using
# OAUTH and username and password
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for username="%s", remember_me=%s'
                .format(form.username.data, form.remember_me.data))
        return redirect('')
    return render_template('login.html',
                            title='Sign In',
                            form=form)


@app.route('/event', methods=['GET', 'POST'])
def create_event():
    form = EventForm()

    if form.validate_on_submit():
        e = Event(name=form.name.data, description=form.description.data,
                  venu=form.venu.data,date=form.date.data,
                  end_time=form.end_time.data, admission=form.admission.data,
                  category=form.category.data
                  )
        db.session.add(e)
        db.session.commit()
        return redirect('')

    return render_template('create_event.html',
                    title='New Event',
                    form=form)

@app.route('/event/<int:id>/edit', methods=['GET', 'POST'])
def edit_event(id):
    form = EventForm()
    e = Event.query.get(id)

    if form.validate_on_submit():
        e.name=form.name.data
        e.description=form.description.data
        e.venu=form.venu.data
        e.date=form.date.data
        e.end_time=form.end_time.data
        e.admission=form.admission.data
        e.category=form.category.data

        db.session.add(e)
        db.session.commit()
        return redirect('')

    form.name.data=e.name
    form.description.data=e.description
    form.venu.data=e.venu
    form.date.data=e.date
    form.end_time.data=e.end_time
    form.admission.data=e.admission
    form.category.data=e.category

    return render_template('edit_event.html',
                            title='Edit Event',
                            form=form)

@app.route('/event/<int:id>/delete', methods=['GET', 'POST'])
def delete_event(id):
    e = Event.query.get(id)

    db.session.delete(e)
    db.session.commit()

    return redirect('')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
