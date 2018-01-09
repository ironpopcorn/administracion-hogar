from flask import Blueprint, render_template, request, redirect, url_for

from src.shared.db import db
from src.models.cuenta import Cuenta

cuentas = Blueprint('cuentas', __name__)


@cuentas.route('/cuentas/index.html')
@cuentas.route('/cuentas/')
def index():
    df = Cuenta.get_all(as_dataframe=True)
    df = df[['id', 'nombre']]
    return render_template('cuentas/index.html', lista_cuentas=df.to_html(index=False, classes=["table-bordered", "table-hover"]))


@cuentas.route('/cuentas/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        return crear_post()
    else:
        return render_template('cuentas/crear.html')


def crear_post():
    cuenta_nombre = request.form['cuenta_nombre']
    if len(cuenta_nombre) > 0:
        cuenta = Cuenta(nombre=cuenta_nombre)
        cuenta.save()
        
    return redirect(url_for('cuentas.index'))
