from flask import Blueprint

exports = Blueprint('exports', __name__)

@exports.route('/exports')
def export_index():
    return 'Exports - coming soon'