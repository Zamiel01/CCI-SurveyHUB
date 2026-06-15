from flask import Blueprint, render_template

responses = Blueprint('responses', __name__)

@responses.route('/survey/<token>')
def public_survey(token):
    return render_template('public_survey.html', token=token)
