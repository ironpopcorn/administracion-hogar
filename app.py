""" Administración del Hogar en Flask """
from flask import Flask, render_template

from src.shared.db import db
from src.pages.cuentas import cuentas
from src.pages.departamentos import departamentos
from src.pages.registros import registros
from src.pages.reportes import reportes

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/home.db'
db.app = APP
db.init_app(APP)
db.create_all()

APP.register_blueprint(cuentas)
APP.register_blueprint(departamentos)
APP.register_blueprint(registros)
APP.register_blueprint(reportes)


@APP.route('/')
def home():
    """ Página de Inicio """
    return render_template('home.html')


if __name__ == "__main__":
    APP.run(debug=True)
