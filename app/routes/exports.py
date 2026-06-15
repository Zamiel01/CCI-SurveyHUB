from flask import Blueprint, render_template
from flask_login import login_required

exports = Blueprint('exports', __name__)

@exports.route('/exports')
@login_required
def export_index():
    return render_template('exports.html')
