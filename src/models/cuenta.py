from src.shared.db import db
import pandas as pd


class Cuenta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(
        db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return '<Cuenta {0}, {1}>'.format(self.id, self.nombre)

    def __str__(self):
        return self.nombre
    

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
        }

    @staticmethod
    def get(i):
        cta = Cuenta.query.filter_by(id=i).first()
        return cta

    @staticmethod
    def get_all(as_dataframe=False):
        ctas = Cuenta.query.all()
        if as_dataframe:
            df = pd.DataFrame.from_records([c.to_dict() for c in ctas])
            return df
        
        return ctas

    @staticmethod
    def get_all_to_html_select(name, selected=None, classes=""):
        select = '<select class="form-control {1}" name="{0}" id="{0}">'.format(
            name, classes)
        select = select + '<option>Seleccione</option>'
        
        ctas = Cuenta.query.all()
        if len(ctas) > 0:
            for cta in ctas:
                sel=''
                if selected == cta.id:
                    sel=' selected'
                select = select + '<option value="{0}"{2}>{1}</option>'.format(cta.id, cta.nombre, sel)

        select = select + '</select>'
        return select

    def save(self):
        db.session.add(self)
        db.session.commit()
