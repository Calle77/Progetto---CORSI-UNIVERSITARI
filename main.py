########################################################################################
######################          Import packages      ###################################
########################################################################################
from functools import update_wrapper
from operator import pos
from re import S
import re
from flask import Blueprint, render_template, flash, request, redirect
from flask.helpers import url_for
from flask_login import login_required, current_user
from . import create_app, db
from sqlalchemy import *
from .models import Studenti_corso, User, Corso, Lezione
from werkzeug.security import generate_password_hash

########################################################################################7
# our main blueprint
main = Blueprint('main', __name__)


@main.route('/') 
def index():
    if User.query.filter(User.email=="admin@unive.it").first() == None:
        admin = User(firstname = "admin",lastname = "admin", email="admin@unive.it", password = generate_password_hash("admin", method='sha256'), is_admin = True)
        db.session.add(admin)
        db.session.commit()
    return render_template('index.html')


@main.route('/preside')
@login_required
def preside():
    if current_user.is_admin == False:
        if current_user.is_docente == False:
            return redirect(url_for('main.corsi'))
        else: return redirect(url_for('main.docente'))
    utenti = User.query.filter(User.is_docente==True).all()
    return render_template('preside.html', utenti=utenti)


@main.route('/preside/inserimento',methods=['GET', 'POST'])
@login_required
def inserimento_docenti():
    if current_user.is_admin == False:
        if current_user.is_docente == False:
            return redirect(url_for('main.corsi'))
        else: return redirect(url_for('main.docente'))
    print(request.form.get('firstname'))
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    email = request.form.get('email')
    password = request.form.get('password')  
    user = User.query.filter_by(email = email).first() # if this returns a user, then the email already exists in database
    if user: 
        # if a user is found, we want to redirect back to preside page so the admin can try again
        flash('Indirizzo già esistente')
        return redirect(url_for('main.preside'))  
    # create a new professor with the form data. Hash the password so the plaintext version isn't saved.
    new_docente = User(firstname = firstname, lastname = lastname, email = email, password = generate_password_hash(password, method='sha256'), is_docente=True)  
    # add the new professor to the database
    db.session.add(new_docente)
    db.session.commit()  
    return redirect(url_for('main.preside'))


@main.route('/preside/cancellazione', methods=['GET', 'POST'])
@login_required
def cancellazione_docenti():
    if current_user.is_admin == False:
        if current_user.is_docente == False:
            return redirect(url_for('main.corsi'))
        else: return redirect(url_for('main.docente'))
    id = request.form.get('id')
    print(id)
    User.query.filter(User.id == id).delete()
    db.session.commit()
    return redirect(url_for('main.preside'))


@main.route('/docente')
@login_required
def docente():
    if current_user.is_docente == False:
        if current_user.is_admin == False:
            return redirect(url_for('main.corsi'))
        else: return redirect(url_for('main.preside'))
    corsi = Corso.query.all()   
    corsi_docente = Corso.query.filter(Corso.id_docente==current_user.id).all()
    return render_template('docente.html', corsi = corsi, last_access = current_user.last_access, corsi_docente=corsi_docente)


@main.route('/docente/corsi/demografia/<id>') 
@login_required
def vedi_demografia(id):
    num_iscritti = User.query.join(Studenti_corso, User.id == Studenti_corso.cod_user).add_columns(User.id,User.firstname,User.lastname, User.email).filter(Studenti_corso.cod_corso == id).count()
    utenti = User.query.join(Studenti_corso, User.id == Studenti_corso.cod_user).add_columns(User.id,User.firstname,User.lastname, User.email).filter(Studenti_corso.cod_corso == id).all()
    return render_template('demografiaOneCourse.html', utenti=utenti, last_access = current_user.last_access, num_iscritti=num_iscritti)


@main.route('/docente/corsi/inserimento',methods=['GET', 'POST'])
@login_required
def inserimento_corsi():
    if current_user.is_docente == False:
        if current_user.is_admin == False:
            return redirect(url_for('main.corsi'))
        else: return redirect(url_for('main.preside'))
    nome = request.form.get('nome')
    descrizione = request.form.get('descrizione')
    n_disponibili = request.form.get('posti')
    tipocorso = request.form.get('tipo')
    id = current_user.id
    corsoTest = Corso.query.filter_by(nome = nome).first() # if this returns a corso, then the corso already exists in database
    if corsoTest: 
        flash('Questo corso è già esistente')
        return redirect(url_for('main.docente'))
    corso = Corso(nome = nome, descrizione = descrizione, id_docente=id, n_disponibili = n_disponibili, tipo = tipocorso)
    db.session.add(corso)
    db.session.commit()
    return redirect(url_for('main.docente'))


@main.route('/docente/corsi/cancellazione',methods=['GET', 'POST']) 
@login_required
def cancellazione_corsi():
    if current_user.is_docente == False:
        if current_user.is_admin == False:
            return redirect(url_for('main.corsi'))
        else: return redirect(url_for('main.preside'))
    id = request.form.get('id')
    print(id)
    Corso.query.filter(Corso.id == id).delete()
    db.session.commit()
    return redirect(url_for('main.docente'))


@main.route('/docente/lezioni/inserimento',methods=['GET', 'POST'])
@login_required
def inserimento_lezioni():
    if current_user.is_docente == False:
        if current_user.is_admin == False:
            return redirect(url_for('main.corsi'))
        else: return redirect(url_for('main.preside'))
    corso = request.form.get('corso')
    nome = request.form.get('nome')
    data = request.form.get('data')
    orario = request.form.get('orario')

    lezioneTest = Lezione.query.filter_by(nome = nome,cod_corso=corso).first() # if this returns a lezione, then the lezione already exists in database
    if lezioneTest: 
        flash('Questa lezione è già stata inserita')
        return redirect(url_for('main.docente'))

    lezione = Lezione(nome = nome, data = data, fascia_oraria = orario, cod_corso = corso)
    db.session.add(lezione)
    db.session.commit()
    return redirect(url_for('main.docente'))


@main.route('/reservations') 
@login_required
def prenotazioni():
    prenotazioni = Studenti_corso.query.join(Corso, Studenti_corso.cod_corso == Corso.id).join(User, Corso.id_docente == User.id).add_columns(Corso.id,Corso.id_docente, User.firstname, User.lastname, User.email, Corso.nome).filter(Studenti_corso.cod_user == current_user.id).all()
    return render_template('prenotazioni.html', prenotazioni = prenotazioni, last_access = current_user.last_access)


@main.route('/courses') 
@login_required
def corsi():
    corsi_potenziali = Corso.query.filter(~Corso.id.in_(db.session.query(Studenti_corso.cod_corso).filter(Studenti_corso.cod_user == current_user.id)), Corso.n_disponibili > 0).all()
    return render_template('courses.html', corsi_potenziali = corsi_potenziali,last_access = current_user.last_access)


@main.route('/courses/<id>')
@login_required
def iscrizione_corsi(id):
    iscrizione = Studenti_corso(cod_corso=id, cod_user = current_user.id)
    db.session.add(iscrizione)
    db.session.commit()
    return redirect(url_for('main.corsi'))


@main.route('/reservations/<id>') 
@login_required
def cancellazione(id):
    Studenti_corso.query.filter_by(cod_corso=id, cod_user=current_user.id).delete()
    db.session.commit()
    return redirect(url_for('main.prenotazioni'))


@main.route('/reservations/<id>/lezioni') 
@login_required
def lezioni_corso(id):
    lezioni = Lezione.query.filter(Lezione.cod_corso==id).all()
    return render_template('lezioni.html',lezioni = lezioni, last_access = current_user.last_access)


app = create_app() # we initialize our flask app using the __init__.py function
if __name__ == '__main__':
    db.create_all(app=create_app()) # create the SQLite database
    app.run() # run the flask app on debug mode
    
    
    
