from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if  request.method== 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logado com sucesso!', category='sucess')
                login_user(user, remember=True)
                if user.type == 'C':
                    return redirect(url_for('auth.client_page'))
                elif user.type == 'F':
                    return redirect(url_for('auth.employee_page'))
                else:
                    return redirect(url_for('auth.manager_page'))
            else:
                flash('Senha incorreta!', category='error')
        else:
            flash('Este email não existe!', category='error')

    return render_template("login.html", title='login', user='current_user')


@auth.route('/client_page', methods=['GET', 'POST'])
@login_required
def client_page():
    return render_template("client_page.html", title='Client Page', user=current_user)


@auth.route('/employee_page', methods=['GET', 'POST'])
@login_required
def employee_page():
    return render_template("employee_page.html", title='Employee Page', user=current_user)


@auth.route('/manager_page', methods=['GET', 'POST'])
@login_required
def manager_page():
    return render_template("manager_page.html", title='Manager Page', user=current_user)


@auth.route('/sign_up_employee', methods=['GET', 'POST'])
@login_required
def sign_up_employee():
    if request.method =='POST':
        employee_name = request.form.get('name')
        employee_age = request.form.get('age')
        employee_phone = request.form.get('phone')
        employee_email = request.form.get('email')
        employee_password = request.form.get('password')
        type = 'F'

        user = User.query.filter_by(email=employee_email).first()

        if user:
            flash('Ja existe um funcionario com esse email.', category='error')
        elif len(employee_email) < 4:
            flash('O email do funcionario deve ter ao menos 4 letras', category='error')
        elif len(employee_name) < 4:
            flash('O nome do funcionario deve ter ao menos 3 letras', category='error')
        elif int(employee_age) < 18:
            flash('O funcionario deve ser maior de 18 anos para ter uma conta.', category='error')
        elif len(employee_phone) < 8:
            flash('O telefone do usuario deve ter ao menos 8 digitos.', category='error')
        elif len(employee_password) < 7:
            flash('A senha do funcionario deve ter ao menos 7 caracteres.', category='error')
        else:
            new_user = User(name=employee_name, age=employee_age, phone=employee_phone, 
                            email=employee_email, 
                            password=generate_password_hash(employee_password, method='scrypt'), type=type)
            db.session.add(new_user)
            db.session.commit()
            flash('Funcionario cadastrado com sucesso!', category='sucess')
    return render_template("sign_up_employee.html", title='Sign up new Employee', user=current_user)


@auth.route('/alter_employee', methods=['GET', 'POST'])
@login_required
def alter_employee():
    return render_template("alter_employee.html", title='Alter Employee', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method =='POST':
        name = request.form.get('name')
        age = request.form.get('age')
        phone = request.form.get('phone')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        type = 'C'

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Este email ja existe.', category='error')
        elif len(email) < 4:
            flash('seu email deve ter ao menos 4 caracteres', category='error')
        elif len(name) < 4:
            flash('Seu nome deve possuir ao menos 3 letras', category='error')
        elif int(age) < 18:
            flash('Voce deve ser maior de idade para criar uma conta.', category='error')
        elif len(phone) < 8:
            flash('Seu telefone deve ter ao menos 8 digitos.', category='error')
        elif password1 != password2:
            flash('Senhas nao coincidem.', category='error')
        elif len(password1) < 7:
            flash('Sua senha deve ter ao menos 7 caracteres.', category='error')
        else:
            new_user = User(name=name, age=age, phone=phone, 
                            email=email, password=generate_password_hash(password1, method='scrypt'), type=type)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Conta criada com sucesso!', category='sucess')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", title='Sign up', user=current_user)
