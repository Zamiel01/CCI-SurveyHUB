from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from app import db
from app.models.survey import Survey
from app.models.response import Response, Company
from app.models.anomaly import Anomaly
from datetime import datetime, timedelta
from sqlalchemy import func, and_

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
@login_required
def index():
    # Count metrics
    total_surveys = Survey.query.count()
    published_surveys = Survey.query.filter_by(status='published').count()
    total_responses = Response.query.count()
    incomplete_records = Response.query.filter_by(completion_status='incomplete').count()
    potential_duplicates = Anomaly.query.filter_by(issue_type='duplicate').count()

    # Pagination for latest responses
    page = request.args.get('page', 1, type=int)
    per_page = 4
    total_responses_count = total_responses
    
    pagination = Response.query.order_by(Response.submitted_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    # Handle out-of-bounds page
    if page > pagination.pages and pagination.pages > 0:
        return redirect(url_for('dashboard.index', page=pagination.pages))
    
    responses = pagination.items
    total_pages = pagination.pages
    
    # Response volume chart data (last 30 days)
    today = datetime.utcnow()
    daily_data = []
    daily_labels = []
    
    for i in range(29, -1, -1):
        day = today - timedelta(days=i)
        day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        
        count = Response.query.filter(
            and_(
                Response.submitted_at >= day_start,
                Response.submitted_at < day_end
            )
        ).count()
        
        daily_data.append(count)
        daily_labels.append(day.strftime('%d %b'))

    return render_template(
        'dashboard.html',
        total_surveys=total_surveys,
        published_surveys=published_surveys,
        total_responses=total_responses,
        incomplete_records=incomplete_records,
        potential_duplicates=potential_duplicates,
        responses=responses,
        page=page,
        total_pages=total_pages,
        total_responses_count=total_responses_count,
        daily_labels=daily_labels,
        daily_data=daily_data
    )

@dashboard.route('/anomalies')
@login_required
def anomalies():
    return render_template('anomalies.html')
