from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", user=current_user)  


@views.route('/search', methods=['GET', 'POST'])
def search():  
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
