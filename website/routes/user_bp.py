from flask import Blueprint
from ..controllers.UserController import signup, sign_up_employee, alter_employee, search, new_schedule, history

user_bp = Blueprint('user_bp', __name__)

user_bp.route('/sign-up', methods=['GET', 'POST'])(signup)
user_bp.route('/sign_up_employee', methods=['GET', 'POST'])(sign_up_employee)
user_bp.route('/alter_employee', methods=['GET', 'POST'])(alter_employee)
user_bp.route('/search', methods=['GET', 'POST'])(search)
user_bp.route('/new_schedule', methods=['GET', 'POST'])(new_schedule)
user_bp.route('/history', methods=['GET', 'POST'])(history)