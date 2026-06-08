from flask import Blueprint

responses = Blueprint('responses', __name__)

@responses.route('/survey/<token>')
def public_survey(token):
    return f'Public survey {token} - coming soon'