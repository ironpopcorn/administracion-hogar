from flask import Blueprint, render_template, request, redirect, url_for

from src.shared.db import db
from src.models.registro import Registro
from src.models.cuenta import Cuenta

reportes = Blueprint('reportes', __name__)


@reportes.route('/reportes/index.html')
@reportes.route('/reportes')
def index():
    return render_template('reportes/index.html')


@reportes.route('/reportes/pendientes')
def pendientes():
    df = Registro.get_all_por_estado('pendiente')
    return render_template('reportes/pendientes.html', lista_pendientes=df.to_html())


@reportes.route('/reportes/historico')
def historico():
    cuenta = request.args.get('cuenta', default=None, type=str)
    ctas = Cuenta.get_all_to_html_select('cuenta')
    if cuenta == None:        
        return render_template('reportes/historico.html', cuentas_select=ctas)
    else:
        return render_template('reportes/historico.html', cuentas_select=ctas, cuenta_name=cuenta)
    
