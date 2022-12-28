# app/restricted/routes.py


from flask_user import roles_required

from app import db, admin
from flask_login import current_user, login_required
#from flask_principal import Permission, RoleNeed, UserNeed, identity_loaded
from flask import render_template,request, url_for, redirect
from flask_admin.contrib.sqla import ModelView

from app.auth.models import Votante, Role, UserRoles
from flask_admin import AdminIndexView


class MyModelView(ModelView):
    def is_accessible(self):
        has_auth = current_user.is_authenticated
        role_admin = False
        if has_auth:
            role_admin = current_user.is_admin
        return has_auth and role_admin
'''
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('public.auth.login', next=request.url))
        '''


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        has_auth = current_user.is_authenticated
        role_admin = False
        if has_auth:
            role_admin = current_user.is_admin
        return has_auth and role_admin



# agregamos al admin de todos los modelos

admin.add_view(MyModelView(Votante, db.session))
admin.add_view(MyModelView(Role, db.session))



