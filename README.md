# 🏠 HousingAnalytics  
### Production-Ready Housing Price Intelligence Platform (Canada)

> Transform raw Statistics Canada housing data into actionable insights through a secure, full-stack analytics dashboard.

---

## 🚀 Live Capabilities

- Upload raw HPI datasets → instantly visualize trends  
- Compare provinces and cities interactively  
- Analyze housing market shifts over time  
- Secure, authenticated, role-aware access  

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

## 🎯 Problem

Housing affordability is one of Canada’s most urgent economic challenges.  

- Statistics Canada datasets are complex and difficult to explore  
- No simple tools exist for non-technical users  
- Analysts spend significant time cleaning data before gaining insights  

---

## 💡 Solution

**HousingAnalytics** is a full-stack Django platform that:

- Ingests raw CSV datasets  
- Validates and structures data automatically  
- Provides interactive visualizations  
- Enables instant exploration without coding  

---

## 🧠 Key Engineering Highlights

### 🔐 Secure Authentication
- Email-based login using Django Auth  
- Extended `UserProfile` model  
- CSRF-protected forms  

### 📂 Data Pipeline
- Schema validation (columns, encoding, data types)  
- Fault-tolerant CSV ingestion  
- Idempotent imports using `update_or_create` (no duplicates)  

### 📈 Visualizations (Chart.js)
- National HPI trend (time-series)  
- Province comparison  
- Toronto vs Vancouver analysis  
- Interactive Market Explorer:
  - Compare up to 4 regions  
  - Custom date range  
  - Toggle chart types  

### ⚙️ Admin Panel
- Full Django admin integration  
- Filtering, search, and ordering  

---

## 🏗 Architecture
Client (HTML/CSS/JS + Chart.js)
↓
Django Views (Business Logic)
↓
Django ORM
↓
SQLite Database


- Follows Django MTV (Model–Template–View)
- Modular and scalable design

---

## 🛠 Tech Stack

| Layer        | Technology |
|-------------|-----------|
| Backend      | Django, Python |
| Frontend     | HTML, CSS, JavaScript |
| Charts       | Chart.js |
| Database     | SQLite |
| Auth         | Django Auth + Custom Profile |

---

## ⚡ Quick Start

```bash
# Clone repo
git clone https://github.com/HitanshuBhatt/Canadian-housing-price-index.git
cd Canadian-housing-price-index/housing_project

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install django

# Apply migrations
python manage.py migrate

# Run server
python manage.py runserver
Open at
http://127.0.0.1:8000

## CSV Format
required format
| Column   | Description                     |
| -------- | ------------------------------- |
| Date     | YYYY-MM-DD                      |
| GEO      | Region (Canada, province, city) |
| Category | Housing type                    |
| VALUE    | Numeric index                   |

## Project Structure
housing_project/
├── manage.py
├── housing_project/
└── dashboard/
    ├── models.py
    ├── views.py
    ├── forms.py
    ├── urls.py
    ├── admin.py
    └── templates/

##📈 Scalability
Idempotent ingestion prevents duplicate data
Designed for PostgreSQL migration
Ready for Docker and cloud deployment
