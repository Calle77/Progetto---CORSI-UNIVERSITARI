########################################################################################
######################          Import packages      ###################################
########################################################################################
from flask_login import UserMixin
from sqlalchemy.sql.schema import ForeignKey
import enum
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True) # primary keys are required by SQLAlchemy
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    last_access = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default = False)
    is_docente = db.Column(db.Boolean, default = False)
    email = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(1000))


class Corso(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True) # primary keys are required by SQLAlchemy
    nome = db.Column(db.String(100))
    n_disponibili = db.Column(db.Integer, default = 100)
    tipo = db.Column(db.String(100))
    id_docente = db.Column(db.Integer, db.ForeignKey(User.id))
    descrizione = db.Column(db.String(5000))


class Studenti_corso(db.Model):
    cod_corso = db.Column(db.Integer,db.ForeignKey(Corso.id), primary_key = True)
    cod_user = db.Column(db.Integer,db.ForeignKey(User.id), primary_key = True)


class Lezione(db.Model):
    nome = db.Column(db.String(100), primary_key = True)
    fascia_oraria = db.Column(db.String(100))
    cod_corso = db.Column(db.Integer,db.ForeignKey(Corso.id), primary_key = True)
    data = db.Column(db.String)
    