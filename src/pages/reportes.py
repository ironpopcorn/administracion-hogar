from flask import Blueprint, render_template, request
from bokeh.plotting import figure, show
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.models import NumeralTickFormatter

from src.models.registro import Registro
from src.models.departamento import Departamento
from src.models.cuenta import Cuenta

reportes = Blueprint('reportes', __name__)


@reportes.route('/reportes/index.html')
@reportes.route('/reportes')
def index():
    return render_template('reportes/index.html')


@reportes.route('/reportes/pendientes')
def pendientes():
    depa = request.args.get('departamento', default=None, type=int)
    if depa is None:
        depas = Departamento.get_all_to_html_select(
            'departamento', classes="form-control-sm mx-2",)
        df = Registro.get_all_por_estado('pendiente')
        df = df[['id', 'departamento', 'cuenta', 'fecha', 'valor']]
        total = 0
        if len(df) > 0:
            total = df['valor'].sum()
        return render_template('reportes/pendientes.html', departamentos_select=depas, lista_pendientes=df.to_html(index=False, classes=["table-bordered", "table-hover"]), total=total)
    else:
        depas = Departamento.get_all_to_html_select(
            'departamento', classes="form-control-sm mx-2", selected=depa)
        df = Registro.get_all_por_estado('pendiente', departamento=depa)
        df = df[['id', 'departamento', 'cuenta', 'fecha', 'valor']]
        total = 0
        if len(df) > 0:
            total = df['valor'].sum()
        return render_template('reportes/pendientes.html', departamentos_select=depas, lista_pendientes=df.to_html(index=False, classes=["table-bordered", "table-hover"]), total=total)


@reportes.route('/reportes/historico')
def historico():
    depa = request.args.get('departamento', default=None, type=int)
    cuenta = request.args.get('cuenta', default=None, type=int)
    if cuenta is None or depa is None:
        depas = Departamento.get_all_to_html_select(
            'departamento', classes="form-control-sm mx-2")
        ctas = Cuenta.get_all_to_html_select(
            'cuenta', classes="form-control-sm mx-2")
        return render_template('reportes/historico.html', departamentos_select=depas, cuentas_select=ctas)
    else:
        departamento = Departamento.get(depa)
        departamento_name = departamento.calle + ' ' + str(departamento.numero)
        depas = Departamento.get_all_to_html_select('departamento', classes="form-control-sm mx-2", selected=depa)
        cta = Cuenta.get(cuenta)
        ctas = Cuenta.get_all_to_html_select(
            'cuenta', classes="form-control-sm mx-2", selected=cuenta)
        df = Registro.get_all_por_cuenta(cuenta, departamento=depa)
        df = df[['id', 'fecha', 'estado', 'valor']]
        total = 0
        tag_script = ''
        tag_div = ''
        cdn_js = ''
        cdn_css = ''
        if len(df) > 0:
            total = df['valor'].sum()
            graph = figure(x_axis_type='datetime')
            graph.xaxis.axis_label='Mes'
            graph.yaxis.axis_label='Pesos'
            graph.yaxis.formatter = NumeralTickFormatter(format="($ 0.00 a)")
            graph.line(df['fecha'], df['valor'])
            graph.circle(df['fecha'], df['valor'])
            tag_script, tag_div = components(graph)
            cdn_js = CDN.js_files[0]
            cdn_css = CDN.css_files[0]
        return render_template('reportes/historico.html', departamentos_select=depas, departamento_name=departamento_name, cuentas_select=ctas, cuenta_name=cta.nombre, historico=df.to_html(index=False, classes=["table-bordered", "table-hover"]), total=total, tag_script=tag_script, tag_div=tag_div, cdn_js=cdn_js, cdn_css=cdn_css)
    
