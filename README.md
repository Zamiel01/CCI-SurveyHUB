# CCI SurveyHUB

> Create. Collect. Verify. Analyse.

A web application designed for the Chamber of Commerce and Industry (CCI) to centralise 
the creation, distribution, collection and analysis of business surveys.

---

## Project Overview

CCI SurveyHUB was built to solve a real data management problem observed during an 
internship at the CCI. Survey responses were scattered across multiple Excel files, 
company records contained missing or invalid data, and analysis was slow and unreliable.

This application brings everything into one place:
- Create structured surveys with blocks and multiple-choice questions
- Share surveys with companies through a public link
- Automatically detect data quality issues on submission
- Visualise results through a simple dashboard
- Export clean data to CSV or Excel for Power BI reporting

---

## Stack

| Layer | Technology |
|-------|------------|
| Backend | Python Flask |
| Database | SQLite + Flask-SQLAlchemy |
| Frontend | HTML, CSS, Bootstrap 5, JavaScript |
| Data Processing | Pandas |
| Charts | Chart.js |
| Exports | Pandas + OpenPyXL |

---

## Project Structure

```
CCI-SurveyHUB/
├── app/
│   ├── __init__.py          # App factory
│   ├── routes/
│   │   ├── auth.py          # Login and logout
│   │   ├── dashboard.py     # Main dashboard
│   │   ├── surveys.py       # Survey creation and management
│   │   ├── questions.py     # Blocks and questions
│   │   ├── responses.py     # Public response form
│   │   ├── exports.py       # CSV and Excel exports
│   ├── models/
│   │   ├── user.py          # Users table
│   │   ├── survey.py        # Surveys, blocks, questions, choices
│   │   ├── response.py      # Companies, responses, answers
│   │   ├── anomaly.py       # Anomalies table
│   ├── templates/
│   │   ├── base.html        # Base layout with navbar
│   │   ├── login.html       # Login page
│   │   ├── dashboard.html   # Dashboard
│   │   ├── surveys.html     # Survey list
│   │   ├── create_survey.html
│   │   ├── preview.html     # Survey preview
│   │   ├── results.html     # Results and charts
│   │   ├── anomalies.html   # Anomalies management
│   ├── static/
│   │   ├── css/
│   │   │   └── main.css
│   │   ├── js/
│   │   │   └── main.js
├── documentation/
│   ├── README.md
│   ├── user_guide.md
│   ├── installation.md
│   └── bug_tracking.md
├── requirements.txt
├── run.py
└── .gitignore
```

---

## Features

### Survey Management
- Create surveys with title, description, objective and target audience
- Organise questions into blocks for better structure
- Add multiple-choice questions with predefined answer choices
- Preview survey before publishing
- Generate unique public link on publish
- Track survey status: Draft → Published → Closed → Archived

### Data Collection
- Public response form accessible without login
- Companies fill in their information and answer questions
- Responses stored in a clean relational database

### Data Quality Control
Automatic validation runs on every submission:

| Field | Rule |
|-------|------|
| Email | Must contain valid format with @ |
| SIRET | Must be exactly 14 digits |
| Phone | Must be exactly 10 digits |
| Required fields | Cannot be empty |
| Duplicates | Detected by matching SIRET |

All issues are logged to the anomalies table and visible on the anomalies page.

### Dashboard
- Total surveys created
- Published surveys count
- Total responses received
- Incomplete records count
- Potential duplicates count
- Latest responses feed

### Results and Analysis
- Response count per survey
- Answer distribution per question
- Bar charts and pie charts via Chart.js
- Most selected choices highlighted

### Exports
- All responses (CSV or Excel)
- Clean responses only
- Anomalies report
- Aggregated statistics
- Power BI ready file

---

## Database Schema

9 tables covering the full survey lifecycle:

| Table | Purpose |
|-------|---------|
| users | Internal CCI staff and admins |
| surveys | Survey metadata and status |
| blocks | Question groups inside a survey |
| questions | Individual survey questions |
| choices | Predefined answer options |
| companies | Business respondent information |
| responses | One completed or partial survey submission |
| answers | Selected choices per response |
| anomalies | Detected data quality issues |

---

## Installation

See `documentation/installation.md` for full setup instructions.

Quick start:

```bash
git clone https://github.com/yourusername/CCI-SurveyHUB.git
cd CCI-SurveyHUB
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Then open `http://127.0.0.1:5000` in your browser.

---

## Usage

See `documentation/user_guide.md` for full usage instructions.

---

## Development Roadmap

| Week | Focus | Status |
|------|-------|--------|
| Week 1 | Project setup, structure, database schema | ✅ Complete |
| Week 2 | Survey creation module, admin space | 🔄 In Progress |
| Week 3 | Public response form, validation, anomalies | ⏳ Pending |
| Week 4 | Results, charts, exports, final demo | ⏳ Pending |

---

## Daily Progress Log

### Day 6 — Authentication (Login & Session Management)

- Built the login form with Flask-Login integration
- Wrote the login route to authenticate against the users table using werkzeug password checking
- Protected all internal routes with `@login_required`
- Built the logout route to clear the session
- Test login with seeded users: `jean.dupont@cci.fr` / `admin123`
- Redirect unauthenticated users to `/login`
- Show error message on wrong credentials
- Added toast notifications for flash messages (success, error, info)
- Fixed flash message isolation between login and register tabs
- Implemented "Remember me" functionality for session persistence

---

## Team

| Person | Responsibility |
|--------|---------------|
| Person 1 | Web interface, Flask routes, templates, Bootstrap design |
| Person 2 | Database models, validation logic, exports, charts |

---

## Documentation

| File | Content |
|------|---------|
| README.md | Project overview and setup |
| user_guide.md | How to use the application |
| installation.md | Step by step technical setup |
| bug_tracking.md | Bugs encountered and fixes applied |

---

## Limitations (MVP)

This is a first version MVP. The following features are out of scope 
for this release:

- Conditional logic between questions
- Automatic email campaigns
- Advanced user role management
- Direct Power BI API connection
- Predictive analysis module
- Mobile application
- Open-ended text questions

---

## License

Internal project — CCI internship context.
Not intended for public distribution.

---

## Acknowledgements

Inspired by professional survey platforms such as Qualtrics.
Built as an internal MVP adapted to the specific needs of the CCI.