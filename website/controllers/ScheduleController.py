from flask import Blueprint, render_template, request, flash, redirect
from werkzeug.security import generate_password_hash
from flask_login import login_user, login_required, current_user
from ..models.models import User, Schedule, Service

from ..database import db

# esta versão do historico mostra uma listagem de funcionarios pois
# a tabela de atendimentos ainda não foi implementada


@login_required
def history():

    atendimentos = db.session.query(Schedule, Service, User).\
        join(Service, Service.schedule_id == Schedule.id).\
        join(User, User.id == Service.client_id).\
        all()
    
    total_ganhos = 0.0

    for atendimento in atendimentos:
        if atendimento.Schedule.type == 'Corte de Cabelo':
            total_ganhos += 75.00 #atendimento.User.age deve ser trocado para o custo do atendimento
        else:
            total_ganhos += 20.00

    total_atendimentos = len(atendimentos)
    media_ganhos = round(total_ganhos/total_atendimentos, 2)

    return render_template("history.html", title='Histórico', user=current_user, services=atendimentos, soma_de_ganhos=total_ganhos, media_de_ganhos=media_ganhos)


@login_required
def search():
    funcionarios = User.query.filter_by(type='F').all()

    if request.method == 'POST':
        funcionario_pesquisado = request.form.get('funcionario')
        for funcionario in funcionarios:
            if funcionario.name == funcionario_pesquisado:
                horarios_disponiveis = db.session.query(Schedule, Service, User).filter_by(employee=funcionario.id).\
                    join(Service, Service.schedule_id == Schedule.id, isouter=True).\
                    join(User, User.id == Service.client_id, isouter=True).\
                    all()

        if horarios_disponiveis != None:
            return render_template('search.html', title='Consultar Horários', user=current_user, employee=funcionario_pesquisado, employees=funcionarios, spec_schedules=horarios_disponiveis)
        else:
            flash('Funcionario inexistente!', category='error')
            return render_template('search.html', title='Consultar Horários', user=current_user, employees=funcionarios)
    else:
        horarios_disponiveis = db.session.query(Schedule, Service, User).\
            join(Service, Service.schedule_id == Schedule.id, isouter=True).\
            join(User, User.id == Service.client_id, isouter=True).\
            all()
        return render_template('search.html', title='Consultar Horários', user=current_user, schedules=horarios_disponiveis, employees=funcionarios, employee=None)


@login_required
def new_schedule():
    all_employees = User.query.filter_by(type='F').all()

    if request.method == 'POST':
        schedule_data = request.form.get('data')
        employee_name = request.form.get('employee_name')
        schedule_date = request.form.get('date')
        schedule_type = request.form.get('type')

        employee = User.query.filter_by(name=employee_name).first()

        if not employee:
            flash('Este funcionário não existe.', category='error')
        else:
            id_employee = employee.id
            new_schedule = Schedule(data=schedule_data, employee=id_employee, date=schedule_date, type=schedule_type)
            db.session.add(new_schedule)
            db.session.commit()
            flash('Horário lançado no sistema com sucesso!', category='sucess')
    return render_template("new_schedule.html", title='Disponibilizar Horário', user=current_user, employees=all_employees)
