from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app import db
from app.models.survey import Survey, Block, Question, Choice
from app.models.response import Response, Answer

surveys = Blueprint('surveys', __name__)

@surveys.route('/surveys')
@login_required
def survey_list():
    # Get filter and pagination params
    status_filter = request.args.get('status', '', type=str)
    page = request.args.get('page', 1, type=int)
    per_page = 5
    
    # Build base query
    query = Survey.query.order_by(Survey.created_at.desc())
    
    # Apply status filter if provided and valid
    valid_statuses = ['draft', 'published', 'closed', 'archived']
    if status_filter and status_filter in valid_statuses:
        query = query.filter_by(status=status_filter)
    
    # Paginate
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    survey_items = pagination.items
    total_pages = pagination.pages
    
    # Compute response counts for each survey
    surveys_with_counts = []
    for survey in survey_items:
        response_count = Response.query.filter_by(survey_id=survey.id).count()
        surveys_with_counts.append({
            'survey': survey,
            'response_count': response_count
        })
    
    return render_template(
        'surveys.html',
        surveys=surveys_with_counts,
        page=page,
        total_pages=total_pages,
        total_surveys=pagination.total,
        current_status=status_filter,
        valid_statuses=valid_statuses
    )

@surveys.route('/surveys/create')
@login_required
def create_survey():
    """Create a draft survey and redirect to the builder."""
    survey = Survey(
        title='Untitled Survey',
        description='',
        objective='',
        target_audience='',
        status='draft',
        created_by=current_user.id
    )
    db.session.add(survey)
    db.session.commit()
    flash('Survey created. You can now build it.', 'success')
    return redirect(url_for('surveys.survey_builder', id=survey.id))

@surveys.route('/surveys/<int:id>/builder')
@login_required
def survey_builder(id):
    """Render the survey builder page."""
    survey = Survey.query.get_or_404(id)
    return render_template('survey_builder.html', survey=survey)

@surveys.route('/surveys/<int:id>/update', methods=['POST'])
@login_required
def update_survey(id):
    """Update survey settings from the builder."""
    survey = Survey.query.get_or_404(id)
    survey.title = request.form.get('title', survey.title).strip()
    survey.description = request.form.get('description', survey.description).strip()
    survey.objective = request.form.get('objective', survey.objective).strip()
    survey.target_audience = request.form.get('target_audience', survey.target_audience).strip()
    survey.status = request.form.get('status', survey.status).strip()
    db.session.commit()
    flash('Survey settings saved.', 'success')
    return redirect(url_for('surveys.survey_builder', id=survey.id))

@surveys.route('/surveys/<int:id>/blocks/add', methods=['POST'])
@login_required
def add_block(id):
    """Add a new block to the survey."""
    survey = Survey.query.get_or_404(id)
    title = request.form.get('title', '').strip()
    if not title:
        flash('Block title is required.', 'danger')
        return redirect(url_for('surveys.survey_builder', id=survey.id))
    
    position = Block.query.filter_by(survey_id=survey.id).count() + 1
    block = Block(
        survey_id=survey.id,
        title=title,
        position=position
    )
    db.session.add(block)
    db.session.commit()
    flash('Block added.', 'success')
    return redirect(url_for('surveys.survey_builder', id=survey.id))

@surveys.route('/blocks/<int:id>/questions/add', methods=['POST'])
@login_required
def add_question(id):
    """Add a new multiple-choice question to the block."""
    block = Block.query.get_or_404(id)
    text = request.form.get('text', '').strip()
    if not text:
        flash('Question text is required.', 'danger')
        return redirect(url_for('surveys.survey_builder', id=block.survey_id))
    
    position = Question.query.filter_by(block_id=block.id).count() + 1
    question = Question(
        block_id=block.id,
        text=text,
        question_type='multiple_choice',
        required=True,
        position=position
    )
    db.session.add(question)
    db.session.commit()
    flash('Question added.', 'success')
    return redirect(url_for('surveys.survey_builder', id=block.survey_id))

@surveys.route('/questions/<int:id>/choices/add', methods=['POST'])
@login_required
def add_choice(id):
    """Add a new choice to the question."""
    question = Question.query.get_or_404(id)
    choice_text = request.form.get('choice_text', '').strip()
    if not choice_text:
        flash('Choice text is required.', 'danger')
        return redirect(url_for('surveys.survey_builder', id=question.block.survey_id))
    
    position = Choice.query.filter_by(question_id=question.id).count() + 1
    choice = Choice(
        question_id=question.id,
        choice_text=choice_text,
        position=position
    )
    db.session.add(choice)
    db.session.commit()
    flash('Choice added.', 'success')
    return redirect(url_for('surveys.survey_builder', id=question.block.survey_id))

@surveys.route('/surveys/<int:id>/delete', methods=['POST'])
@login_required
def delete_survey(id):
    survey = Survey.query.get_or_404(id)
    
    # Check if survey has responses
    response_count = Response.query.filter_by(survey_id=survey.id).count()
    if response_count > 0:
        flash('Cannot delete survey with existing responses.', 'danger')
        return redirect(url_for('surveys.survey_list'))
    
    db.session.delete(survey)
    db.session.commit()
    flash('Survey deleted successfully.', 'success')
    return redirect(url_for('surveys.survey_list'))

@surveys.route('/surveys/<int:id>/preview')
@login_required
def preview_survey(id):
    """Render the survey preview page (read-only)."""
    survey = Survey.query.get_or_404(id)
    return render_template('preview.html', survey=survey)

@surveys.route('/surveys/<int:id>/publish', methods=['POST'])
@login_required
def publish_survey(id):
    """Publish the survey and generate a public token."""
    survey = Survey.query.get_or_404(id)
    
    if survey.status == 'published':
        flash('Survey is already published.', 'info')
        return redirect(url_for('surveys.survey_builder', id=survey.id))
    
    survey.status = 'published'
    survey.generate_token()
    db.session.commit()
    
    public_url = url_for('responses.public_survey', token=survey.public_token, _external=True)
    flash(f'Survey published successfully! Public link: {public_url}', 'success')
    return redirect(url_for('surveys.survey_builder', id=survey.id))

@surveys.route('/surveys/<int:id>/edit')
@login_required
def edit_survey(id):
    return redirect(url_for('surveys.survey_builder', id=id))

@surveys.route('/surveys/<int:id>/results')
@login_required
def survey_results(id):
    """Display survey results with charts."""
    survey = Survey.query.get_or_404(id)
    
    # Get all responses for this survey
    responses = Response.query.filter_by(survey_id=survey.id).all()
    total_responses = len(responses)
    
    # Calculate completion rate
    complete_responses = sum(1 for r in responses if r.completion_status == 'complete')
    completion_rate = round((complete_responses / total_responses) * 100, 1) if total_responses > 0 else 0
    
    # Build results data per question
    question_results = []
    
    for block in survey.blocks:
        for question in block.questions:
            # Count answers per choice
            choice_data = []
            for choice in question.choices:
                count = Answer.query.filter_by(
                    question_id=question.id,
                    choice_id=choice.id
                ).count()
                choice_data.append({
                    'text': choice.choice_text,
                    'count': count,
                    'percentage': round((count / total_responses) * 100, 1) if total_responses > 0 else 0
                })
            
            question_results.append({
                'question': question,
                'choice_data': choice_data,
                'labels': [c['text'] for c in choice_data],
                'counts': [c['count'] for c in choice_data]
            })
    
    return render_template(
        'results.html',
        survey=survey,
        total_responses=total_responses,
        complete_responses=complete_responses,
        completion_rate=completion_rate,
        question_results=question_results
    )
