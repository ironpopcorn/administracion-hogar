from src.shared.db import db
import pandas as pd


class Registro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    departamento_id = db.Column(db.Integer, db.ForeignKey('departamento.id'), nullable=False)
    departamento = db.relationship(
        'Departamento', backref=db.backref('registro', lazy=True))
    cuenta_id = db.Column(db.Integer, db.ForeignKey(
        'cuenta.id'), nullable=False)
    cuenta = db.relationship('Cuenta', backref=db.backref('cuenta', lazy=True))
    fecha = db.Column(db.Date, nullable=False)
    valor = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.Enum('pendiente', 'pagado'), nullable=False)

    def __repr__(self):
        return '<Registro {0}, {1}, {2}>'.format(self.fecha, self.cuenta_id, self.valor)

    def to_dict(self):
        return {
            'id' : self.id,
            'departamento_id' : self.departamento_id,
            'departamento' : str(self.departamento),
            'cuenta_id' : self.cuenta_id,
            'cuenta' : str(self.cuenta),
            'fecha' : self.fecha,
            'valor' : self.valor,
            'estado' : self.estado,
        }

    @staticmethod
    def get_all(as_dataframe=False):
        regs = Registro.query.all()
        if as_dataframe:
            df = pd.DataFrame.from_records([r.to_dict() for r in regs])
            if len(regs) > 0:
                df.drop(columns=['departamento_id', 'cuenta_id'], inplace=True)
                df.set_index('id', inplace=True)
            return df

        return regs

    @staticmethod
    def get_all_por_estado(estado):
        regs = Registro.query.filter_by(estado=estado).all()
        df = pd.DataFrame.from_records([r.to_dict() for r in regs])
        if len(regs) > 0:
            df.drop(columns=['departamento_id', 'cuenta_id'], inplace=True)
            df.set_index('id', inplace=True)
        return df

    def save(self):
        db.session.add(self)
        db.session.commit()
