import functools
from datetime import datetime
from datetime import timedelta
import csv
import pandas as pd
import os
from datetime import date

from flask import (
    Blueprint, flash, g, render_template, request, url_for, session, redirect, current_app, make_response, send_file
)

from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db
from app.text import text_EN, text_ES

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    company = current_app.config['COMPANY_NAME']
    if request.method == 'POST':
        lang = request.args.get('lang')
        username = request.form['username']
        password = request.form['password']

        db, c = get_db()
        error = None
        c.execute(
            'select id, user, password from users where user = %s', (username,)
        )

        user = c.fetchone()

        if user is None:
            error = 'Usuario y/o contraseña inválida'
        elif not check_password_hash(user['password'], password):
            error = 'Usuario y/o contraseña inválida'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('auth.index'))

        flash(error)
        print('si, error')
        if lang == 'EN':
            resp = make_response(render_template(
                'auth/login.html', error=error, text=text_EN, company=company))
            resp.set_cookie('lang', 'EN')
            return resp
        else:
            resp = make_response(render_template(
                'auth/login.html', error=error,  text=text_ES, company=company))
            resp.set_cookie('lang', 'ES')
            return resp
    else:
        lang = request.args.get('lang')

        if lang == 'EN':
            resp = make_response(render_template(
                'auth/login.html', text=text_EN, company=company))
            resp.set_cookie('lang', 'EN')
            return resp
        else:
            resp = make_response(render_template(
                'auth/login.html', text=text_ES, company=company))
            resp.set_cookie('lang', 'ES')
            return resp


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.usert = None
    else:
        db, c = get_db()
        c.execute(
            'select * from users where id = %s', (user_id,)
        )
        g.user = c.fetchone()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/')
@login_required
def index():
    lang = request.args.get('lang')
    company = current_app.config['COMPANY_NAME']

    text_ES = {
        "title": "Panel de administración  "
    }
    text_EN = {
        "title": "Admin panel "
    }

    if lang == 'EN':
        resp = make_response(render_template(
            'auth/index.html', text=text_EN, company=company))
        resp.set_cookie('lang', 'EN')
        return resp
    else:
        resp = make_response(render_template(
            'auth/index.html', text=text_ES, company=company))
        resp.set_cookie('lang', 'ES')
        return resp


@bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    company = current_app.config['COMPANY_NAME']
    lang = request.cookies.get('lang')

    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        username = request.form['username']
        password = request.form['password']

        db, c = get_db()
        error = None
        c.execute(
            'select id from users where user = %s', (username,)
        )
        if not username:
            error = 'Username es requerido'
        if not password:
            error = 'Password es requerido'
        elif c.fetchone() is not None:
            error = 'El usuario {} ya se encuentra registrado.'.format(
                username)

        if error is None:
            c.execute(
                'insert into users (name, surname, user, password) values (%s, %s, %s, %s)',
                (name, surname, username, generate_password_hash(password))
            )
            db.commit()

            db, c = get_db()
            c.execute('select id, name, surname, user from users')
            users = c.fetchall()
            if lang == 'EN':
                return render_template('auth/register.html', text=text_EN, users=users, company=company)
            else:
                return render_template('auth/register.html', text=text_ES, users=users, company=company)
        db, c = get_db()
        c.execute('select id, name, surname, user from users')
        users = c.fetchall()

        flash(error)
        if lang == 'EN':
            return render_template('auth/register.html', error=error, text=text_EN, users=users, company=company)
        else:
            return render_template('auth/register.html', error=error, text=text_ES, users=users, company=company)
        error = None

    else:
        db, c = get_db()
        c.execute('select id, name, surname, user from users')
        users = c.fetchall()
        if lang == 'EN':
            return render_template('auth/register.html', text=text_EN, users=users, company=company)
        else:
            return render_template('auth/register.html', text=text_ES, users=users, company=company)


@bp.route('/delete')
@login_required
def delete():
    id = request.args.get('id')
    db, c = get_db()
    c.execute('delete  from users where id = %s', (id,))
    db.commit()

    db, c = get_db()
    c.execute('select id, name, surname, user from users')
    users = c.fetchall()
    return redirect(url_for('auth.register'))


def to_excel(data):

    isdir = os.path.isdir('app/static/tmp/')
    if isdir == False:
        os.mkdir('app/static/tmp/')

    try:
        isFile = os.path.isfile('app/static/tmp/report.csv')
        if isFile:
            os.remove('app/static/tmp/report.csv')
    except:
        pass

    pd.DataFrame(data).to_csv('app/static/tmp/report.csv')


@bp.route('/report', methods=['GET', 'POST'])
@ login_required
def report():
    company = current_app.config['COMPANY_NAME']
    lang = request.cookies.get('lang')
    file = request.args.get('file')

    if request.method == 'POST':
        date_to = request.form['date_to']
        date_from = request.form['date_from']

        if date_to == date_from:
            date_to = datetime.strptime(date_to, "%Y-%m-%d")
            date_to = date_to + timedelta(days=1)

        db, c = get_db()
        c.execute('select name, surname, company, email, dni, host, gdpr, date  from visitas where date between %s and %s',
                  (date_from, date_to))
        result = c.fetchall()

        to_excel(result)

        if lang == 'EN':
            return render_template('auth/report.html', text=text_EN, result=result, company=company)
        else:
            return render_template('auth/report.html', text=text_ES, result=result, company=company)

    else:
        if file == 'report':
            return send_file('static/tmp/report.csv', as_attachment=True)

        if lang == 'EN':
            return render_template('auth/report.html', text=text_EN, company=company)
        else:
            return render_template('auth/report.html', text=text_ES, company=company)


@bp.route('/monitor', methods=['GET'])
@ login_required
def monitor():
    company = current_app.config['COMPANY_NAME']
    lang = request.cookies.get('lang')
    today = date.today()
    today = datetime.strptime(str(today), "%Y-%m-%d")

    db, c = get_db()
    c.execute('select name, surname, company, email, dni, host, gdpr, date  from visitas where date between %s and %s',
              (today, today + timedelta(days=1)))
    result = c.fetchall()

    if lang == 'EN':
        return render_template('auth/monitor.html', text=text_EN, result=result, company=company, today=today.date())
    else:
        return render_template('auth/monitor.html', text=text_ES, result=result, company=company, today=today.date())


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
