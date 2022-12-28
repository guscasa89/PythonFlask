from app import db


class Sufragio(db.Model):
    __tablename__ = 'sufragio'
    #__table_args__ = dict(schema="e202735")
    id = db.Column(db.Integer, primary_key=True)
    lista = db.Column(db.Integer, db.ForeignKey('lista.nro_lista'))
    blanco = db.Column(db.Boolean, nullable=True, default=False)
    anulado = db.Column(db.Boolean, nullable=True, default=False)

class Padron(db.Model):
    __tablename__ = 'padron'
    #__table_args__ = dict(schema="e202735")
    nro_socio = db.Column(db.Integer, primary_key=True)

    @staticmethod
    def check_nro_socio(nro_socio):
        if Padron.query.filter_by(nro_socio=nro_socio).first() is not None:
            return True
        else:
            return False

    def get_total_hab():
        return Padron.query.count()

class Lista(db.Model):
    __tablename__ = 'lista'
    #__table_args__ = dict(schema="e202735")
    nro_lista = db.Column(db.Integer, primary_key=True)
    presidente = db.Column(db.String(255), nullable=False)
    vicepresidente = db.Column(db.String(255), nullable=False)
    cant_votos = db.Column(db.Integer, nullable=True, default=0)

    @staticmethod
    def get_by_nro(nro_lista):
        return Lista.query.get(nro_lista)

    def sumar_voto(self):
        self.cant_votos = self.cant_votos + 1

    @staticmethod
    def check_nro_lista(nro_lista):
        if Lista.query.filter_by(nro_lista=nro_lista).first() is not None:
            return True
        else:
            return False

    def save(self):
        db.session.add(self)
        db.session.commit()

class Resultado(db.Model):
    __tablename__ = 'resultado'
    #__table_args__ = dict(schema="e202735")
    id = db.Column(db.Integer, primary_key=True)
    cant_hab = db.Column(db.Integer, nullable=False)
    cant_vot = db.Column(db.Integer, nullable=False)
    cant_vot_x = db.Column(db.Integer, nullable=False)
    cant_vot_y = db.Column(db.Integer, nullable=False)
    cant_vot_z = db.Column(db.Integer, nullable=False)
