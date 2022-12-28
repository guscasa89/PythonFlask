# app/auth/routes.py
import datetime
from . import auth_bp
from app import login_manager
from flask import render_template, redirect, url_for, flash, request, session, current_app
from .models import Votante
from .utils import generate_confirmation_token, send_email, confirm_token
from app.public.models import Padron
from .forms.login import LoginForm
from .forms.register import RegisterForm
from flask_login import current_user, login_user, logout_user


#le decimos a Flask-Login como obtener un usuario
@login_manager.user_loader
def load_user(user_id):
    return Votante.get_by_id(int(user_id))


@auth_bp.route('/apfa/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('public.index_apfa'))

    form = LoginForm()

    if form.validate_on_submit():
        #get by email valida
        votante = Votante.get_by_email(form.email.data)
        if votante is not None and votante.check_password(form.password.data):
            #if si el votante es admin lo dejo loguearse
            #else debo ver si el usuario tiene confirmado mail
            if votante.es_confirmado or votante.is_admin:
                login_user(votante, remember=form.remember_me.data)
                next_page = request.args.get('next', None)
                if not next_page:
                    next_page = url_for('public.index_apfa')
                return redirect(next_page)
            else:
                flash('Mail no confirmado')
                return redirect(url_for('auth.login'))
        else:
            flash('Usuario o contraseña inválido')
            return redirect(url_for('auth.login'))
    # no loggeado, dibujamos el login con el form vacio
    return render_template('login.html', form=form)


@auth_bp.route("/apfa/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('public.index_apfa'))
    form = RegisterForm()
    error = None
    if form.validate_on_submit():
        email = form.email.data
        nro_socio = form.nro_socio.data
        password = form.password.data
        # Comprobamos que no hay ya un usuario con ese nro socio o mail
        #votante = Votante.get_by_socio(nro_socio)
        if Votante.get_by_socio(nro_socio) is not None:
            flash('El nro de socio {} pertenece a otro usuario'.format(nro_socio))
        else:
            if Padron.check_nro_socio(nro_socio):
                if Votante.get_by_email(email) is not None:
                    flash('El mail {} pertenece a otro usuario'.format(email))
                else:
                    votante = Votante(email=email, nro_socio=nro_socio, es_confirmado = False, ya_voto = False, is_admin = False, email_confirmed_at = None)
                    votante.set_password(password)
                    votante.save()
                    token = generate_confirmation_token(votante.email)
                    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
                    html = render_template('activate.html', confirm_url=confirm_url)
                    send_email(votante.email, current_app.config['MAIL_SUBJECT'], html)

                    # Dejamos al usuario logueado
                    login_user(votante, remember=True)
                    return redirect(url_for('public.index_apfa'))
            else:
                flash('El nro de socio {} no es correcto'.format(nro_socio))
    return render_template("register.html", form=form)

@auth_bp.route('/apfa/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    votante = Votante.query.filter_by(email=email).first_or_404()
    if votante.es_confirmado:
        flash('Account already confirmed. Please login.', 'success')
    else:
        votante.es_confirmado = True
        votante.email_confirmed_at = datetime.datetime.now()
        votante.save()

        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('public.index_trivia'))



@auth_bp.route('/apfa/logout')
def logout():
    session.clear()
    logout_user()

    return redirect(url_for('public.index_apfa'))




