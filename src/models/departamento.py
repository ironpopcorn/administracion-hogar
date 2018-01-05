from src.shared.db import db
import pandas as pd


class Departamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    calle = db.Column(db.String(25), unique=True, nullable=False)
    numero = db.Column(db.Integer, nullable=False)
    comuna = db.Column(db.String(25), nullable=False)
    habitantes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Departamento {0}, {1}, {2}>'.format(self.id, 
                                                     self.calle, 
                                                     str(self.numero))

    def __str__(self):
        return self.calle + ' ' + str(self.numero)

    def to_dict(self):
        return {
            'id' : self.id,
            'calle' : self.calle,
            'numero' : self.numero,
            'comuna' : self.comuna,
            'habitantes' : self.habitantes,
        }

    @staticmethod
    def get_all(as_dataframe=False):
        depas = Departamento.query.all()
        if as_dataframe:
            df = pd.DataFrame.from_records([d.to_dict() for d in depas])
            if len(depas) > 0:
                df.set_index('id', inplace=True)
            return df

        return depas

    @staticmethod
    def get_all_to_html_select(name):
        select = '<select name="{0}">'.format(name)
        select = select + '<option>Seleccione</option>'
        
        depas = Departamento.query.all()
        if len(depas) > 0:
            for depa in depas:
                select = select + '<option value="{0}">{1} {2}</option>'.format(depa.id, depa.calle, depa.numero)

        select = select + '</select>'
        return select

    def save(self):
        db.session.add(self)
        db.session.commit()
    