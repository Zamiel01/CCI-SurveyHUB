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
| Authentication | Flask-Login + Werkzeug password hashing |
| Frontend | HTML, CSS, Bootstrap 5, JavaScript |
| Data Processing | Pandas |
| Charts | Chart.js |
| Exports | Pandas + OpenPyXL |

---

## Project Structure

```
CCI-SurveyHUB/
├── app/
│   ├── __init__.py          # App factory, blueprint registration
│   ├── routes/
│   │   ├── auth.py          # Login and logout (Flask-Login)
│   │   ├── dashboard.py     # Main dashboard — real DB queries
│   │   ├── surveys.py       # Survey list, builder, blocks, questions, choices, publish
│   │   ├── responses.py     # Public response form (token-based access)
│   │   ├── exports.py       # CSV and Excel exports (Week 4)
│   ├── models/
│   │   ├── user.py          # Users table
│   │   ├── survey.py        # Surveys, blocks, questions, choices
│   │   ├── response.py      # Companies, responses, answers
│   │   ├── anomaly.py       # Anomalies table
│   ├── templates/
│   │   ├── base.html        # Base layout with sidebar and navbar
│   │   ├── login.html       # Login page
│   │   ├── dashboard.html   # Dashboard wired to real data
│   │   ├── surveys.html     # Survey list with filters and pagination
│   │   ├── create_survey.html  # Survey builder — blocks, questions, choices
│   │   ├── preview.html     # Survey preview (real nested data)
│   │   ├── public_survey.html  # Public-facing response form
│   │   ├── results.html     # Results and charts (Week 4)
│   │   ├── anomalies.html   # Anomalies management (Week 3)
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
├── instance/
│   └── surveyhub.db         # SQLite database (gitignored)
├── seed.py                  # Database seed script — dummy data
├── requirements.txt
├── run.py
└── .gitignore
```

---

## Features

### Authentication
- Login page with email and password
- Session management via Flask-Login
- All internal pages protected with `@login_required`
- Logout clears the session and redirects to login
- Active/inactive user accounts supported via `is_active` flag

### Survey Management
- Create surveys with title, description, objective and target audience
- Organise questions into blocks for better structure
- Add multiple-choice questions with predefined answer choices
- Add, edit and remove answer choices per question
- Preview survey with real nested data before publishing
- Generate unique public link on publish (`public_token`)
- Track survey status: Draft → Published → Closed → Archived
- Filter survey list by status (All / Published / Draft / Closed)
- Paginated survey list
- Delete protection — surveys with existing responses cannot be deleted

### Data Collection
- Public response form accessible without login via `/survey/<token>`
- Token-based access — only published surveys are reachable
- Companies fill in their information (name, SIRET, email, phone) 
  and answer questions
- Client-side required field validation on the public form
- Submit route stubbed and ready for Week 3 data persistence logic

### Data Quality Control (Planned — Week 3)
Automatic validation will run on every submission:

| Field | Rule |
|-------|------|
| Email | Must contain valid format with @ |
| SIRET | Must be exactly 14 digits |
| Phone | Must be exactly 10 digits |
| Required fields | Cannot be empty |
| Duplicates | Detected by matching SIRET |

All issues will be logged to the anomalies table and visible on the anomalies page.

### Dashboard
- Total surveys created (real count from database)
- Published surveys count
- Total responses received
- Incomplete records count
- Potential duplicates count
- Latest responses feed (5 most recent)
- Response volume chart (Chart.js — Week 4)

### Results and Analysis (Planned — Week 4)
- Response count per survey
- Answer distribution per question
- Bar charts and pie charts via Chart.js
- Most selected choices highlighted

### Exports (Planned — Week 4)
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

### Schema Notes

- `surveys.public_token` stores the unique token used to build the 
  shareable public link, generated only when a survey is published
- `anomalies.company_id` allows direct querying of anomalies by 
  company without joining through responses
- `anomalies.resolved_at` and `resolved_by` provide an audit trail 
  for resolved data quality issues
- `answers.text_value` supports future open-ended question types 
  in addition to predefined choice selections
- `users.active` (note: not `is_active`) tracks whether a user 
  account is enabled — renamed from the original schema design 
  to avoid a naming conflict with Flask-Login's `UserMixin.is_active` 
  property

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
python seed.py
```

Then open `http://127.0.0.1:5000` in your browser.

**Seeded test accounts:**

| Email | Password | Role |
|-------|----------|------|
| jean.dupont@cci.fr | admin123 | admin |
| marie.curie@cci.fr | user123 | user |

---

## Usage

See `documentation/user_guide.md` for full usage instructions.

---

## Development Roadmap

| Week | Focus | Status |
|------|-------|--------|
| Week 1 | Project setup, structure, database schema | ✅ Complete |
| Week 2 | Authentication, dashboard, survey builder, preview, publish | ✅ Complete |
| Week 3 | Public response collection, validation, anomalies | ⏳ Pending |
| Week 4 | Results, charts, exports, final demo | ⏳ Pending |

### Week 2 Summary

| Day | Focus | Outcome |
|-----|-------|---------|
| Day 6 | Authentication | Login/logout working with Flask-Login, routes protected |
| Day 7 | Dashboard | Real database queries replacing static dummy numbers |
| Day 8 | Survey List | Functional status filters, pagination, delete protection |
| Day 9 | Survey Builder | Create survey, add blocks, add questions, add choices — full CRUD |
| Day 10 | Preview + Publish | Real nested preview rendering, publish route with token generation, public survey page wired to database |

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