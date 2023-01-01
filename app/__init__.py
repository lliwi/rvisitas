import os
from flask import Flask


def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        FROM_EMAIL=os.environ.get('FROM_EMAIL'),
        SENDGRID_KEY=os.environ.get('SENDGRID_API_KEY'),
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        DATABASE_HOST=os.environ.get('FLASK_DATABASE_HOST'),
        DATABASE_PASSWORD=os.environ.get('FLASK_DATABASE_PASSWORD'),
        DATABASE_USER=os.environ.get('FLASK_DATABASE_USER'),
        DATABASE=os.environ.get('FLASK_DATABASE'),
        COMPANY_NAME=os.environ.get('COMPANY_NAME'),
        PRINTER_NAME=os.environ.get('PRINTER_NAME'),
    )

    from . import db
    db.init_app(app)

    from . import rvisitas
    app.register_blueprint(rvisitas.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    return app
