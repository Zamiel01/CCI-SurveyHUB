from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required

exports = Blueprint('exports', __name__)

@exports.route('/exports')
@login_required
def export_index():
    return render_template('exports.html')

@exports.route('/surveys/<int:id>/export/csv')
@login_required
def export_csv(id):
    flash('CSV export coming in Week 4.', 'info')
    return redirect(url_for('surveys.survey_results', id=id))

@exports.route('/surveys/<int:id>/export/excel')
@login_required
def export_excel(id):
    flash('Excel export coming in Week 4.', 'info')
    return redirect(url_for('surveys.survey_results', id=id))
