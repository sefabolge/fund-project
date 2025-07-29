# Fund Importer App

A simple Django application that allows users to upload CSV files containing fund data, view the parsed list with filters and totals, clear all funds, and access the data via a REST API.

- Upload CSV files containing fund data
- Parse and import funds into the database
- Filter funds by strategy
- View total fund count and AUM
- Clear all existing funds
- Access fund data via a REST API
---

##  Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/sefabolge/fund-project.git
cd fund-project
```

### 2.Create & Activate Virtual Environment
```
python -m venv .venv
source .venv/bin/activate        # On macOS/Linux
.venv\Scripts\activate           # On Windows
```

### 3.Install Dependencies & run migrations
```
pip install -r requirements.txt

# Apply migrations
python manage.py makemigrations  # Optional (only if you make model changes)
python manage.py migrate         # Required

# Start the Development Server
python manage.py runserver

```
### 4. Run Test
```
python manage.py test
```

### 5. API Endpoints
```
GET /api/funds/
GET /api/funds/?strategy={strategy}
GET /api/funds/<id>/
```

