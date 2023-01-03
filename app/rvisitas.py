from flask import (
    Blueprint, flash, g, render_template, request, url_for, session, redirect, current_app, make_response
)
from app.db import get_db
from app.text import *

import subprocess
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

bp = Blueprint('reg-visitas', __name__, url_prefix='/')


def send_mail_endgrid(to, subject, company, name, surname, html_content):
    sg = sendgrid.SendGridAPIClient(api_key=current_app.config['SENDGRID_KEY'])
    from_email = Email(current_app.config['FROM_EMAIL'])
    to_email = To(to, substitutions={
        "-company-": company,
        "-name-": name,
        "-surname-": surname
    })

    mail = Mail(from_email, to_email, subject, html_content=html_content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response)


def send_mail_smtp(to, subject, company, name, surname, html_content):
    host = current_app.config['SMTP_HOST']
    port = current_app.config['SMTP_PORT']
    user = current_app.config['SMTP_USER']
    password = current_app.config['SMTP_PASSWORD']
    from_email = current_app.config['FROM_EMAIL']
    html_content = html_content.replace("-company-", company)
    html_content = html_content.replace("-name-", name)
    html_content = html_content.replace("-surname-", surname)

    message = MIMEText(html_content, "html")
    message['Subject'] = subject

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(user, password)
        server.sendmail(
            from_email, to, message.as_string()
        )


@bp.route('/', methods=['GET', 'POST'])
def index():
    lang = request.cookies.get('lang')
    company = current_app.config['COMPANY_NAME']

    if request.method == 'POST':
        name = request.form['name'].capitalize()
        surname = request.form['surname'].capitalize()
        email = request.form['email'].lower()
        dni = request.form['dni'].upper()
        host = request.form['host'].capitalize()
        gdpr = request.form['gdpr']

        if gdpr == 'on':
            gdpr = True

        db, c = get_db()
        c.execute(
            'insert into visitas (name, surname, email, dni, host, gdpr) values (%s, %s,%s, %s, %s, %s)',
            (name, surname, email, dni, host, gdpr)
        )
        db.commit()

        if lang == 'EN':
            content = mail_content_EN
        else:
            content = mail_content_ES

        if current_app.config['SENDGRID_KEY'] != "":
            send_mail_endgrid(email, company + ' GDPR',
                              company, name, surname, content)
        elif current_app.config['SMTP_HOST'] != "":
            send_mail_smtp(email, company + ' GDPR',
                           company, name, surname, content)
        else:
            pass

        return render_template('index.html', company=company)

    else:
        lang = request.args.get('lang')
        file = request.args.get('file')

        if lang == 'ES':
            resp = make_response(render_template(
                'form.html', text=text_ES, company=company))
            resp.set_cookie('lang', 'ES')
            return resp
        elif lang == 'EN':
            resp = make_response(render_template(
                'form.html', text=text_EN, company=company))
            resp.set_cookie('lang', 'EN')
            return resp
        elif file == 'GDPR':
            return render_template('gdpr.html')
        else:
            return render_template('index.html', company=company)

    return render_template('index.html', company=company)
