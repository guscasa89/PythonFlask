#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from app.public.models import Sufragio, Resultado, Padron
from app.auth.models import Votante, Role
from app import create_app, db
import re


app = create_app()
with app.app_context():
    db.session.commit()
    db.drop_all()
    db.create_all()

    #Usuarios
    q_u1 = Votante(email = "gcasavieja@antel.com.uy",
                   es_confirmado = True,
                   ya_voto = False,
                   is_admin = True)
    # el pass lo seteamos con el método set_password para que se guarde con hash
    q_u1.set_password("1234")

    db.session.add(q_u1)

    # padron
    archivo = open("padron.html", "r", encoding="utf8")
    padron = archivo.read()
    pattern = re.compile("</span>(\d\d\d)</div>")
    matching = pattern.findall(padron)
    nros_socio = []
    for n in matching:
        nros_socio.append(n)

    for n in nros_socio:
        p_legajo = Padron(nro_socio=n)
        db.session.add(p_legajo)

    db.session.commit()


    padrones = Padron.query.all()
    for p in padrones:
        print(p.nro_socio)

    '''

    if not User.query.filter(User.email == 'admin@antel.com.uy').first():
        user = User(name="admin",  email="admin@antel.com.uy")
        user.set_password("admin123")
        db.session.add(user)
        db.session.commit()

    # Create 'admin@example.com' user with 'Admin' and 'Agent' roles
    if not User.query.filter(User.email == 'admin@antel.com.uy').first():
        user = User(name="admin2",  email="admin@antel.com.uy", is_admin=True)
        user.set_password("blabla")
        r1 = Role(name='Admin')
        user.roles.append(r1)
        r2 = Role(name='Agent')
        user.roles.append(r2)
        db.session.add(user)
        db.session.commit()
    '''
    db.session.close()




