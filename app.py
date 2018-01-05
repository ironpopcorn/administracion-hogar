from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from src.shared.db import db
from src.pages.cuentas import cuentas
from src.pages.departamentos import departamentos
from src.pages.registros import registros
from src.pages.reportes import reportes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/home.db'
db.app = app
db.init_app(app)
db.create_all()

app.register_blueprint(cuentas)
app.register_blueprint(departamentos)
app.register_blueprint(registros)
app.register_blueprint(reportes)

@app.route('/')
def home():
    return render_template('home.html')


if __name__ == "__main__":
    app.run(debug=True)
