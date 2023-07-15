from flask import Blueprint, render_template, request, flash, redirect
from werkzeug.security import generate_password_hash
from flask_login import login_user, login_required, current_user
from ..models.models import User, Schedule

from ..database import db

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
            return redirect('home')

    return render_template("sign_up.html", title='Sign up', user=current_user)


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


@login_required
def alter_employee():
    return render_template("alter_employee.html", title='Alter Employee', user=current_user)


def search():  
    if request.method == 'POST':
        # horario = request.form.get('horario')
        funcionario_pesquisado = request.form.get('funcionario')

        funcionarios = User.query.filter_by(type='F').all()
        for funcionario in funcionarios:
            if funcionario.name == funcionario_pesquisado:
                horarios_disponiveis = Schedule.query.filter_by(user_id=funcionario.id).all()
                return render_template('search.html', user=current_user, employee=funcionario_pesquisado, schedules=horarios_disponiveis)
            else:
                flash('Funcionario inexistente!', category='error')
                return render_template('search.html', user=current_user)
    else:
        return render_template('search.html', user=current_user)

"""
Formato que search deve seguir
def search():
    if request.method == 'POST':
        horario = request.form.get('horario')
        funcionario = request.form.get('funcionario')

        # Realize a lógica de pesquisa com base no horário e funcionário selecionados

        # Renderize o template com os resultados
        return render_template('search_results.html', results=results)
    else:
        return render_template('search.html')
    """
