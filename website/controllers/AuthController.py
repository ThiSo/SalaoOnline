from flask import Blueprint, render_template, request, flash, redirect
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from ..models.models import User

def login():
    if  request.method== 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logado com sucesso!', category='sucess')
                login_user(user, remember=True)
                return render_template("home.html", user=current_user)
            else:
                flash('Senha incorreta!', category='error')
        else:
            flash('Este email não existe!', category='error')

    return render_template("login.html", title='Login', user='current_user')


@login_required
def logout():
    logout_user()
    return redirect('login')
