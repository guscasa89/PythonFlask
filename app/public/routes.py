# app/public/routes.py

from . import public_bp
from app import login_required, current_user
from flask import render_template, session, flash
from .forms.administrar import AdministrarForm
from .forms.votar import VotarForm
from .models import Padron, Lista
from app.auth.models import Votante
import random
import datetime


@public_bp.route('/apfa')
def index_apfa():
    return render_template('index.html')


@public_bp.route("/apfa/resultados", methods=["GET"])
def resultados():
    listas = Lista.query.all()

    total_hab = Padron.get_total_hab()

    dicc_listas = {}

    for l in listas:
        if l.nro_lista not in dicc_listas:
            list_aux = []
            list_aux.append(l.cant_votos)
            porcentaje = l.cant_votos*100/total_hab
            porcentaje_red = round(porcentaje, 2)
            list_aux.append(porcentaje_red)
            if l.nro_lista == 0:
                dicc_listas.update({"blanco": list_aux})
            elif l.nro_lista == 1:
                dicc_listas.update({"anulado": list_aux})
            else:
                dicc_listas.update({l.nro_lista: list_aux})

    return render_template('resultados.html', resu=dicc_listas)


@public_bp.route('/apfa/sufragar', methods=['GET', 'POST'])
@login_required
def sufragar():
    form = VotarForm()
    listas = Lista.query.all()

    listado_form = []
    for l in listas:
        if l.nro_lista == 0:
            listado_form.append("blanco")
        elif l.nro_lista == 1:
            listado_form.append("anulado")
        else:
            listado_form.append(str(l.nro_lista))

    form.listas.choices = [(lista, lista) for lista in listado_form ]
    form.listas.default = 'blanco'

    nro_lista = form.listas.data

    if form.validate_on_submit():
        #nro_lista = form.listas.data
        if current_user.ya_voto:
            flash('Usted ya tiene voto registrado')
        else:
            if nro_lista.isdigit():
                lista = Lista.get_by_nro(nro_lista)
            else:
                if nro_lista == 'blanco':
                    lista = Lista.get_by_nro(0)
                else:
                    lista = Lista.get_by_nro(1)
            lista = lista.sumar_voto()
            votante = Votante.get_by_email(current_user.email)
            votante.set_ya_voto()
            #lista.save()
            return render_template("gracias.html")


    return render_template('votar.html', form=form, listas=listado_form)



@public_bp.route('/apfa/administrar', methods=["GET", "POST"])
@login_required
def administrar():
    form = AdministrarForm()
    error = None
    if form.validate_on_submit():
        nro_lista = form.nro_lista.data
        presidente = form.presidente.data
        vicepresidente = form.vicepresidente.data
        # Comprobamos que no hay ya una lista con ese nro
        if Lista.check_nro_lista(nro_lista):
            flash('El nro de lista {} ya existe'.format(nro_lista))
        else:
            lista = Lista(nro_lista=nro_lista, presidente=presidente, vicepresidente=vicepresidente, cant_votos=0)
            lista.save()
            return render_template("administrar.html", form=form, msj="ok")
    return render_template("administrar.html", form=form, msj=None)





@public_bp.route('/test_template')
def test_principal_free():
    lista_de_cosas = ["item1", "item2", "item3"]
    return render_template('test_template.html', subtitulo="subtitulo", texto="este es el texto", lista=lista_de_cosas, precio="7676.8")



