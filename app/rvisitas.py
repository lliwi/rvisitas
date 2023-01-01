from flask import (
    Blueprint, flash, g, render_template, request, url_for, session, redirect, current_app, make_response
)
from app.db import get_db
from app.text import *

import subprocess
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

bp = Blueprint('reg-visitas', __name__, url_prefix='/')


def send_mail(to, subject, company, name, surname, html_content):
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


@bp.route('/', methods=['GET', 'POST'])
def index():
    lang = request.cookies.get('lang')
    company = current_app.config['COMPANY_NAME']
    printer = current_app.config['PRINTER_NAME']

    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        dni = request.form['dni']
        host = request.form['host']
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

        send_mail(email, company + ' GDPR', company,
                  name, surname, content)

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
