from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime

from src.shared.db import db
from src.models.registro import Registro
from src.models.departamento import Departamento
from src.models.cuenta import Cuenta

registros = Blueprint('registros', __name__)


@registros.route('/registros/index.html')
@registros.route('/registros/')
def index():
    df = Registro.get_all(as_dataframe=True)
    return render_template('registros/index.html', lista_registros=df.to_html())


@registros.route('/registros/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        return crear_post()
    else:
        depas = Departamento.get_all_to_html_select('reg_departamento_id')
        ctas = Cuenta.get_all_to_html_select('reg_cuenta_id')
        return render_template('registros/crear.html', departamentos_select=depas, cuentas_select=ctas)

def crear_post():
    departamento_id = int(request.form['reg_departamento_id'])
    cuenta_id = int(request.form['reg_cuenta_id'])
    fecha = datetime.strptime(request.form['reg_fecha'] + '-01', '%Y-%m-%d')
    valor  = int(request.form['reg_valor'])
    estado = 'pendiente'

    registro = Registro(departamento_id=departamento_id,
                        cuenta_id=cuenta_id,
                        fecha=fecha,
                        valor=valor,
                        estado=estado)
    registro.save()
    return redirect(url_for('registros.index'))
