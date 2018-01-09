from flask import Blueprint, render_template, request, redirect, url_for

from src.shared.db import db
from src.models.departamento import Departamento

departamentos = Blueprint('departamentos', __name__)


@departamentos.route('/departamentos/index.html')
@departamentos.route('/departamentos/')
def index():
    df = Departamento.get_all(as_dataframe=True)
    df = df[['id', 'calle', 'numero', 'comuna', 'habitantes']]
    return render_template('departamentos/index.html', lista_departamentos=df.to_html(index=False, classes=["table-bordered", "table-hover"]))


@departamentos.route('/departamentos/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        return crear_post()
    else:
        return render_template('departamentos/crear.html')

def crear_post():
    calle = request.form['depa_calle']
    numero = int(request.form['depa_numero'])
    comuna = request.form['depa_comuna']
    habitantes = int(request.form['depa_habitantes'])

    depa = Departamento(calle=calle, 
                        numero=numero, 
                        comuna=comuna, 
                        habitantes=habitantes)
    depa.save()
    return redirect(url_for('departamentos.index'))
