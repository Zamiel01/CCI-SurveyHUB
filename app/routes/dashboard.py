from flask import Blueprint

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
def index():
    return 'Dashboard - coming soon'