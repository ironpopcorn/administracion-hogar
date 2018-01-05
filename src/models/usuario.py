from src.shared.db import db


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(80), unique=True, nullable=False)
    contraseña = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)    

    def __repr__(self):
        return '<Usuario %r>' % self.usuario
