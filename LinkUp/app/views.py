#!env/bin/python
from flask import render_template, flash, redirect, request, g, url_for
from datetime import datetime
from app import app, db, lm, current_user, login_user, logout_user, login_required
from .forms import LoginForm, EventForm, EditUserForm, SearchForm
from .models import User, Event
from .oauth import OAuthSignIn
from config import EVENTS_PER_PAGE, MAXIMUM_SEARCH_RESULTS


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        # can add last seen herself
        g.search_form = SearchForm()

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        # this is to be modified later on as the systems becomes sugestive not
        # generative
        nickname=username
        username = User.make_unique_username(username)
        user = User(social_id=social_id, username=username, nickname=nickname, email=email)
        db.session.add(user)
        db.session.commit()
        # make the user follow him/herself
        db.session.add(user.follow(user))
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('index'))

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

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@app.route('/<int:page>')
@login_required
def index(page=1):
    user_nickname = g.user.nickname
    events = g.user.followed_events().paginate(page, EVENTS_PER_PAGE, False)
    return render_template('index.html',
                            title='Home',
                            user_nickname=user_nickname,
                            events=events)

@app.route('/search', methods=['POST'])
@login_required
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('index'))
    return redirect(url_for('search_results', query=g.search_form.search.data))

@app.route('/search_results/<query>')
@login_required
def search_results(query):
    results = Event.query.whoosh_search(query, MAXIMUM_SEARCH_RESULTS).all()
    return render_template('search_results.html',
                            query=query,
                            results=results)

@app.route('/new', methods=['GET', 'POST'])
@login_required
def create_event():
    year = datetime.today().year
    form = EventForm()

    if form.validate_on_submit():
        e = Event(name=form.name.data, description=form.description.data,
                  venu=form.venu.data,date=form.date.data,
                  end_time=form.end_time.data, admission=form.admission.data,
                  category=form.category.data, user_id=g.user.id
                  )
        db.session.add(e)
        db.session.commit()
        return redirect('')

    return render_template('create_event.html',
                    title='New Event',
                    year=year,
                    form=form)

@app.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_event(id):
    year = datetime.today().year
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
                            year=year,
                            form=form)

@app.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_event(id):
    e = Event.query.get(id)

    db.session.delete(e)
    db.session.commit()

    return redirect('')

@app.route('/<username>')
@app.route('/<username>/<int:page>')
@login_required
def user(username, page=1):
    user = User.query.filter_by(username=username).first()
    if user == None:
        flash('User %s not found.' % username)
        return redirect(url_for('index'))
    events = user.events.order_by(Event.id.desc()).paginate(page, EVENTS_PER_PAGE, False)
    return render_template('user_profile.html',
                            user=user,
                            events=events,
                            title=user.nickname)

@app.route('/account/edit', methods=['GET', 'POST'])
@login_required
def edit_user():
    form = EditUserForm()
    if form.validate_on_submit():
        g.user_user.nickname = form.nickname.data
        g.user.username = form.username.data
        g.user.email = form.email.data
        g.user.website = form.website.data
        g.user.bio = form.bio.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user', username=g.user.username))
    else:
        form.nickname.data = g.user.nickname
        form.username.data = g.user.username
        form.email.data = g.user.email
        form.website.data = g.user.website
        form.bio.data = g.user.bio
    return render_template('edit_profile.html',
                    form=form,
                    title=g.user.nickname)

@app.route('/<username>/follow')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User % not found.' % username)
        return redirect(url_for('index'))
    if user == g.user:
        flash('You can\'t follow yourself')
        return redirect(url_for('user', username=username))
    u = g.user.follow(user)
    if u is None:
        flash('Cannot follow ' + username + '.')
        return redirect(url_for('user', username=username))
    db.session.add(u)
    db.session.commit()
    flash('You are now following ' + username + '!')
    return redirect(url_for('user', username=username))

@app.route('/<username>/unfollow')
@login_required
def unfollow(nickname):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User %s not found.' % username)
        return redirect(url_for('index'))
    if user == g.user:
        flash('You can\'t unfollow yourself!')
        return redirect(url_for('user', username=username))
    u = g.user.unfollow(user)
    if u is None:
        flash('Cannot unfollow ' + username + '.')
        return redirect(url_for('user', usename=username))
    db.session.add(u)
    db.session.commit()
    flash('You have stopped following ' + nickname + '.')
    return redirect(url_for('user', nickname=nickname))


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
