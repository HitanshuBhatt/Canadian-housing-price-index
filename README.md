# HousingAnalytics

**A full-stack Django dashboard for exploring Canadian housing price index data.**

Upload raw Statistics Canada CSV datasets and instantly explore national trends, provincial comparisons, and city-level breakdowns through interactive Chart.js visualizations — no data wrangling required.

---

## Features

- **Secure Authentication** — Email-based registration and login built on Django's auth system, with a custom `UserProfile` model to store date of birth. CSRF protection on all forms.
- **Protected Routes** — Upload and charts pages require authentication (`@login_required`). Unauthenticated users are redirected to login automatically.
- **CSV Ingestion Pipeline** — Upload raw Statistics Canada HPI files. The pipeline validates required columns (`Date`, `GEO`, `Category`, `VALUE`), handles encoding (`UTF-8-sig`), skips malformed rows, and uses `update_or_create` for idempotent imports — re-uploading the same file never creates duplicates.
- **Four Chart Views** via Chart.js:
  - National HPI time-series line chart (Canada, 2020–2025)
  - Provincial index bar chart for the latest available date
  - Toronto vs. Vancouver side-by-side trend comparison
  - Interactive Market Explorer — select up to 4 provinces or cities, choose date range, toggle between line and bar chart
- **Django Admin Panel** — Full `HousingData` admin with filtering by region, category, and date; searchable by geo and category; ordered by most recent date.

---

## Tech Stack

| Layer      | Technology                        |
|------------|-----------------------------------|
| Backend    | Python, Django                    |
| Frontend   | HTML, CSS, Vanilla JavaScript     |
| Charts     | Chart.js (CDN)                    |
| Database   | SQLite (development)              |
| Auth       | Django Auth + Custom UserProfile  |

---

## 📊 Demo Preview
### Homepage

![Home](assets/homepage.png)
### Login Page

![Charts](assets/loginpage.png)

### SignUp Page

![Upload](assets/signuppage.png)

### Upload Page

![upload](assets/uploadpage.png)

### Charts Page 

![upload](assets/chartspage.png)
![upload](assets/chartspage2.png)
![upload](assets/chartspage3.png)
![upload](assets/chartspage4.png)

---

## Project Structure

```
Canadian-housing-price-index/
└── housing_project/
    ├── manage.py
    ├── db.sqlite3
    ├── housing_project/
    │   ├── settings.py
    │   ├── urls.py
    │   ├── wsgi.py
    │   └── asgi.py
    └── dashboard/
        ├── models.py          # HousingData, UserProfile
        ├── views.py           # login, signup, logout, home, upload_csv, charts
        ├── forms.py           # CSVUploadForm, LoginForm, SignUpForm
        ├── urls.py
        ├── admin.py
        ├── migrations/
        └── templates/
            └── dashboard/
                ├── base.html        # Base file containing base layout 
                ├── home.html        # Home Page
                ├── login.html       # LoginForm
                ├── signup.html      # SignUpForm
                ├── upload.html     # CSVUploadForm 
                └── charts.html     # Charts page 
```

---

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/HitanshuBhatt/Canadian-housing-price-index.git
cd Canadian-housing-price-index/housing_project

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install django

# 4. Apply database migrations
python manage.py migrate

# 5. (Optional) Create a superuser for the admin panel
python manage.py createsuperuser

# 6. Start the development server
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## CSV Format

The upload page expects a CSV file with exactly these four columns:

| Column     | Format / Notes                              |
|------------|---------------------------------------------|
| `Date`     | `YYYY-MM-DD`                                |
| `GEO`      | Region name — e.g. `Canada`, `Ontario`, `Toronto, Ontario` |
| `Category` | Housing type — e.g. `house`                 |
| `VALUE`    | Numeric index value                          |

Statistics Canada New Housing Price Index files match this format with minimal preparation.

---

## Architecture

The application follows Django's MTV (Model–Template–View) pattern:

```
Browser (HTML + Chart.js)
        ↓
  Django Views  (business logic, query assembly, JSON serialization)
        ↓
  Django ORM
        ↓
  SQLite Database
```

All chart data is computed server-side in `views.py` and passed to templates as JSON-serialized context variables. The Interactive Market Explorer renders client-side using the pre-loaded `full_dataset` payload — no AJAX calls required.

---

## Roadmap

- PostgreSQL support for production deployments
- Docker + Gunicorn + nginx configuration
- Export filtered datasets to CSV
- Additional Statistics Canada dataset categories (condo, townhouse, etc.)
