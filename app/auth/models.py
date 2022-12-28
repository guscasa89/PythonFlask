from app import db
#from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_user import UserMixin, UserManager


class Votante(db.Model, UserMixin):
    __tablename__ = 'apfa_user'
    #__table_args__ = dict(schema="e202735")
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True, nullable=False)
    es_confirmado = db.Column(db.Boolean, nullable=False, default=False)
    ya_voto = db.Column(db.Boolean, nullable=False, default=False)
    nro_socio = db.Column(db.Integer(), db.ForeignKey('padron.nro_socio', ondelete='CASCADE'))
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    email_confirmed_at = db.Column(db.DateTime())

    # Define the relationship to Role via UserRoles
    roles = db.relationship('Role', secondary='apfa_user_roles')

    def __repr__(self):
        return '<User {} - Email {}>'.format(self.name, self.email)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def set_ya_voto(self):
        self.ya_voto = True
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Votante.query.get(id)

    def get_email(self):
        return self.email

    @staticmethod
    def get_by_email(email):
        return Votante.query.filter_by(email=email).first()

    @staticmethod
    def get_by_socio(nro_socio):
        return Votante.query.filter_by(nro_socio=nro_socio).first()


class Role(db.Model):
    __tablename__ = 'apfa_roles'
    #__table_args__ = dict(schema="e202735")
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return '<Role {}>'.format(self.name)

# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'apfa_user_roles'
    #__table_args__ = dict(schema="e202735")
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('apfa_user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('apfa_roles.id', ondelete='CASCADE'))

    def __repr__(self):
        return '<User {} - Role >'.format(self.user_id, self.role_id)
