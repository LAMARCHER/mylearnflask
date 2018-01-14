# coding:utf-8
from datetime import datetime
from flask import render_template, session, redirect, url_for
from flask_login import login_required

from . import main
from .forms import NameForm
# from .. import db
# from app.models import User


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        return redirect(url_for('main.index'))
    return render_template('index.html', form=form, name=session.get('name'),
                           know=session.get('know', False),
                           current_time=datetime.utcnow())

"""
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            db.session.commit()
            send_mail(template='mail/new_user', user=user, subject='New User', to='13598508974@139.com',)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
        '''
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('looks like you changed your name~~')
        session['name'] = form.name.data
        return redirect(url_for('index'))
        '''
    return render_template('index.html', current_time=datetime.now(), form=form, name=session.get('name'),
                           known=session.get('known', False))
"""


@main.route('/secret')
@login_required
def secret():
    return 'only login user are allowed.'


@main.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)
