from flask import Blueprint, render_template
from flask_login import login_required

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
@login_required
def index():
    return render_template('dashboard.html')

@dashboard.route('/anomalies')
@login_required
def anomalies():
    return render_template('anomalies.html')
