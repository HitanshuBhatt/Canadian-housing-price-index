HousingAnalytics
A full-stack web application for visualising Canadian Housing Price Index (HPI) data from Statistics Canada. Upload your own CSV, explore national trends, compare provinces and cities, and interact with a custom date-range chart — all behind a secure login system.
Problem Statement
Housing affordability is one of Canada's most discussed topics, yet raw Statistics Canada CSV data is inaccessible to most people. There is no simple, self-hosted tool that lets you upload StatCan CSVs and immediately explore interactive provincial and city-level housing price trends without writing a single line of data analysis code.
Solution Overview
HousingAnalytics is a Django web application that ingests Statistics Canada housing CSV files, stores the data in a relational database, and renders four interactive Chart.js visualisations. It includes full user authentication (signup, login, logout with profile initials), role-gated data upload, and an interactive market explorer with custom date ranges and province/city filtering.
Features
•	Secure user registration and email-based login with Django auth
•	CSV upload with server-side validation (column presence, data types, encoding)
•	National trend line chart — Canada-wide monthly HPI from 2020 to 2025
•	Province comparison bar chart — latest available date across 10 provinces
•	Toronto vs Vancouver head-to-head line chart
•	Interactive Market Explorer — select up to 4 provinces or cities, toggle chart type, set custom date range
•	Profile initials avatar with dropdown logout menu
•	Admin panel registration for HousingData model with filters, search, and ordering
•	Idempotent CSV import using update_or_create — safe to re-upload without duplicates
Tech Stack
Backend:  Python 3, Django 6
Frontend:  Vanilla HTML/CSS/JS, Chart.js (CDN)
Database:  SQLite (via Django ORM)
Auth:  Django built-in User model + custom UserProfile (DOB extension)
Data Format:  CSV — Statistics Canada Housing Price Index format
Architecture Overview
The project follows Django's MTV (Model-Template-View) pattern:
•	Models: HousingData (date, geo, category, value) and UserProfile (extends User with DOB)
•	Views: login_view, signup_view, logout_view, home, upload_csv, charts — all in dashboard/views.py
•	Templates: base.html (auth pages) + standalone full-nav templates for home, upload, and charts
•	Forms: CSVUploadForm, LoginForm, SignUpForm with custom validation
•	URLs: All routes registered under dashboard/urls.py, included from housing_project/urls.py
Setup & Installation
Prerequisites
•	Python 3.10+
•	pip
•	Git
Steps
1.	Clone the repository
git clone https://github.com/HitanshuBhatt/housing-analytics.git
cd housing-analytics/housing_project
2.	Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
3.	Install dependencies
pip install django
4.	Apply migrations
python manage.py migrate
5.	Create superuser (optional, for admin panel)
python manage.py createsuperuser
6.	Run the development server
python manage.py runserver
Open http://127.0.0.1:8000 in your browser
Usage
•	Sign up for an account at /signup/
•	Log in at /login/
•	Go to Upload Data, upload a Statistics Canada Housing Price Index CSV with columns: Date, GEO, Category, VALUE
•	Navigate to View Charts to explore visualisations
•	Use the Interactive Market Explorer to select up to 4 regions and set a custom date range
Screenshots
[Screenshot: Home Page — dataset summary and navigation]
[Screenshot: Upload Page — CSV upload form with validation]
[Screenshot: Charts Page — national trend, province bar, Toronto vs Vancouver, and interactive explorer]
CSV Format
The application expects CSV files with at minimum the following columns (case-insensitive):
•	Date — format YYYY-MM-DD
•	GEO — province, city, or 'Canada'
•	Category — e.g. 'house', 'apartment'
•	VALUE — decimal index value
Folder Structure
housing_project/
  manage.py
  housing_project/         # Django project config (settings, urls, wsgi, asgi)
  dashboard/
    models.py              # HousingData, UserProfile
    views.py               # All view logic
    forms.py               # CSVUploadForm, LoginForm, SignUpForm
    urls.py                # Route definitions
    admin.py               # Admin panel registration
    migrations/            # Database migration files
    templates/dashboard/   # HTML templates
Future Improvements
•	REST API with Django REST Framework for frontend decoupling
•	PostgreSQL migration for production-grade persistence
•	Docker + docker-compose for one-command deployment
•	pytest unit and integration test coverage
•	GitHub Actions CI pipeline (lint, test, deploy)
•	Category selector on the charts page (house, apartment, condo)
•	Export chart data as CSV or PNG
•	Deployment to Railway, Render, or AWS
Contributing
Pull requests are welcome. Please open an issue first to discuss proposed changes. Ensure code follows PEP8 and that all forms include CSRF protection.
License
MIT License. See LICENSE for details.

SECTION 2 — LinkedIn & Resume Optimization
LinkedIn Project Description
Built a full-stack Canadian Housing Price Index dashboard using Django, Python, and Chart.js. The application lets users securely upload Statistics Canada CSV files, then explore housing trends through four interactive visualisations — national trend, province comparison, Toronto vs Vancouver, and a custom market explorer with date-range filtering. Implemented email-based authentication, server-side CSV validation, idempotent data import, and a responsive UI. Deployed locally with SQLite; production-ready architecture planned with PostgreSQL and Docker.
Resume Bullet Points
•	Engineered a full-stack data dashboard with Django and Chart.js, processing Statistics Canada housing CSV files into 4 interactive visualisations covering 10 provinces and 20+ cities across a 5-year date range
•	Implemented secure email-based user authentication with Django ORM, custom UserProfile model extension, and CSRF-protected forms — reducing authentication attack surface vs default username login
•	Designed idempotent CSV import pipeline using update_or_create transactions with server-side validation (encoding, schema, data types), enabling safe repeated uploads without duplicate records
•	Built interactive market explorer with dynamic Chart.js rendering, supporting simultaneous comparison of up to 4 geographic regions across a user-defined date range and togglable chart types
•	Structured Django project following MTV architecture with modular views, form validation, and admin panel configuration — demonstrating production-aware code organisation for a Canadian employer audience
