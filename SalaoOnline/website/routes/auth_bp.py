from flask import Blueprint
from ..controllers.AuthController import login, client_page, employee_page, manager_page, logout

auth_bp = Blueprint('auth_bp', __name__)

auth_bp.route('/login', methods=['GET', 'POST'])(login)
auth_bp.route('/client_page', methods=['GET', 'POST'])(client_page)
auth_bp.route('/employee_page', methods=['GET', 'POST'])(employee_page)
auth_bp.route('/manager_page', methods=['GET', 'POST'])(manager_page)
auth_bp.route('/logout', methods=['GET', 'POST'])(logout)