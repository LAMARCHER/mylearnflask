# coding:utf-8
from flask_mail import Message
from flask import render_template
from threading import Thread


def send_mail(app, to, subject, template, **kwargs):
    msg = Message(app.config['FLASK_MAIL_SUBJECT_PREFIX'] + subject,
                  recipients=[to])
    msg.sender = app.config['FLASK_MAIL_SENDER']
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


def send_async_email(mail, app, msg):
    with app.app_context():
        mail.send(msg)
