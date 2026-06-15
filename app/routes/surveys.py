from flask import Blueprint, render_template
from flask_login import login_required

surveys = Blueprint('surveys', __name__)

@surveys.route('/surveys')
@login_required
def survey_list():
    return render_template('surveys.html')
