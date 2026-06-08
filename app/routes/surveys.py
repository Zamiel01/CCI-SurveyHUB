from flask import Blueprint

surveys = Blueprint('surveys', __name__)

@surveys.route('/surveys')
def survey_list():
    return 'Survey list - coming soon'