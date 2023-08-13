from flask import Blueprint
from ..controllers.ServiceController import schedule_time, cancel_time

service_bp = Blueprint('service_bp', __name__)

service_bp.route('/schedule_time', methods=['POST'])(schedule_time)
service_bp.route('/cancel_time', methods=['POST'])(cancel_time)