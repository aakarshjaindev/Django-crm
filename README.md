# Elderco CRM

A modern, sleek Customer Relationship Management system built with **Django 6.0** and a glassmorphism-inspired dark UI.

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0-green?logo=django&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## Features

- **User Authentication** — Register, login, and logout with session-based auth
- **Customer Records CRUD** — Create, read, update, and delete customer contacts
- **Search** — Real-time search across names, emails, phone numbers, cities, and states
- **Responsive Design** — Glassmorphism dark theme with animations, works on all screen sizes
- **Admin Panel** — Full Django admin with filtering, search, and pagination

---

## Tech Stack

| Layer      | Technology           |
|------------|---------------------|
| Backend    | Django 6.0          |
| Database   | SQLite (dev) / MySQL (prod) |
| Frontend   | Django Templates + Vanilla CSS |
| Font       | Inter (Google Fonts) |

---

## Prerequisites

- Python 3.12+
- pip

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/your-username/Django-crm.git
cd Django-crm
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
cp .env.example .env
```

Edit `.env` and set your values:

```
DJANGO_SECRET_KEY=your-random-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

> **Tip:** Generate a secret key at [djecrety.ir](https://djecrety.ir/)

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 7. Start the development server

```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000/** in your browser.

---

## Running Tests

```bash
python manage.py test website -v 2
```

---

## Project Structure

```
Django-crm/
├── dcrm/                   # Project configuration
│   ├── settings.py         # Django settings (env-based)
│   ├── urls.py             # Root URL configuration
│   ├── wsgi.py             # WSGI entry point
│   └── asgi.py             # ASGI entry point
├── website/                # Main CRM application
│   ├── models.py           # Record model with validators
│   ├── views.py            # Authentication + CRUD views
│   ├── urls.py             # App URL patterns (namespaced)
│   ├── forms.py            # SignUp and Record forms
│   ├── admin.py            # Admin site configuration
│   ├── tests.py            # Unit tests (28 test cases)
│   ├── templates/          # Django HTML templates
│   │   ├── base.html       # Base layout with nav + footer
│   │   ├── home.html       # Dashboard / login page
│   │   ├── record.html     # Record detail view
│   │   ├── register.html   # User registration
│   │   ├── add_record.html # Add new record form
│   │   └── update_record.html  # Edit record form
│   └── static/css/
│       └── style.css       # Complete design system (19 sections)
├── .gitignore
├── .env.example            # Environment variable template
├── requirements.txt        # Python dependencies
├── manage.py
└── README.md
```

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DJANGO_SECRET_KEY` | Cryptographic secret key | `django-insecure-dev-only-key` |
| `DJANGO_DEBUG` | Enable debug mode | `True` |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated hostnames | `localhost,127.0.0.1` |
| `DJANGO_LOG_LEVEL` | Django logger level | `INFO` |

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit using [Conventional Commits](https://www.conventionalcommits.org/) (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is open source and available under the [MIT License](LICENSE).
