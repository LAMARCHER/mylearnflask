# coding:utf-8
from datetime import datetime
from flask import render_template, session, redirect, url_for, abort, flash
from flask_login import login_required, current_user

from . import main
from .forms import NameForm, EditProfileForm
from app.decorators import admin_required, permission_required
from app.models import Permission
from .. import db
from app.models import User


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

'''
@main.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)
    '''


@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return 'For administrators!'


@main.route('/moderator')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def for_moderators_only():
    return 'For comment moderators.'


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user .name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)
