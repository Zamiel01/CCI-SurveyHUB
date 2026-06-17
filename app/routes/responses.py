from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from app.models.survey import Survey

responses = Blueprint('responses', __name__)

@responses.route('/survey/<token>')
def public_survey(token):
    survey = Survey.query.filter_by(public_token=token, status='published').first()
    if not survey:
        abort(404)
    return render_template('public_survey.html', survey=survey)

@responses.route('/survey/<token>/submit', methods=['POST'])
def submit_survey(token):
    survey = Survey.query.filter_by(public_token=token, status='published').first()
    if not survey:
        abort(404)
    flash('Response collection coming in Week 3.', 'info')
    return redirect(url_for('responses.public_survey', token=token))
