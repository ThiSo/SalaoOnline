from flask import Blueprint, render_template, request, flash, redirect
from werkzeug.security import generate_password_hash
from flask_login import login_user, login_required, current_user
from ..models.models import User, Schedule, Service

from ..database import db

@login_required
def schedule_time():  
    schedule_id = int(request.form.get('schedule_id'))
    user_id = current_user.id
    paid = 0
    status_service = 0

    new_service = Service(client_id=user_id, schedule_id=schedule_id, paid=paid, status_service=status_service)
    db.session.add(new_service)

    try:
        db.session.commit()
        flash('Horário agendado com sucesso!', category='sucess')
    except:
        db.session.rollback()
        flash('Erro ao agendar horário!', category='error')
    return redirect('/search')


@login_required
def cancel_time():  
    service_id = int(request.form.get('service_id'))

    Service.query.filter(Service.id==service_id).delete()

    try:
        db.session.commit()
        flash('Horário cancelado com sucesso!', category='sucess')
    except:
        db.session.rollback()
        flash('Erro ao cancelar horário!', category='error')
    return redirect('/search')

@login_required
def pay_service():  
    service_id = int(request.form.get('service_id'))
    Service.query.filter(Service.id==service_id).first().paid = 1

    try:
        db.session.commit()
        flash('Pagamento confirmado com sucesso!', category='sucess')
    except:
        db.session.rollback()
        flash('Erro ao confirmar pagamento!', category='error')
    return redirect('/search')

@login_required
def check_time():
    service_id = int(request.form.get('cliente'))

    try:
        service = Service.query.get(service_id)
        if service:
            service.status_service = 1 
            
            db.session.commit()
            flash('Horário concluído com sucesso!', category='success')
        else:
            flash('Horário não encontrado!', category='error')
    except:
        db.session.rollback()
        flash('Erro ao concluir horário!', category='error')
    
    return redirect('/search')
