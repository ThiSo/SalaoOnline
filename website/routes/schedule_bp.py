from flask import Blueprint
from ..controllers.ScheduleController import search, new_schedule, history

schedule_bp = Blueprint('schedule_bp', __name__)

schedule_bp.route('/search', methods=['GET', 'POST'])(search)
schedule_bp.route('/new_schedule', methods=['GET', 'POST'])(new_schedule)
schedule_bp.route('/history', methods=['GET', 'POST'])(history)