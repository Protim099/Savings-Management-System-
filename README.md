# Savings Management System

A full-stack savings management application built with Django REST Framework, React, and MongoDB.

## Stack
- Frontend: React + Vite + Bootstrap 5 + Chart.js
- Backend: Python + Django + Django REST Framework
- Database: MongoDB via MongoEngine
- Authentication: JWT
- PDF: ReportLab
- CORS: django-cors-headers

## Demo accounts
After running the backend seed command:
- Admin: admin@example.com / Admin@123
- Staff: staff@example.com / Staff@123
- Customer: customer@example.com / Customer@123

Change these passwords before deployment.

## Run Backend
```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
copy .env.example .env
python manage.py seed_demo
python manage.py runserver
```

MongoDB should be running locally or provide MONGODB_URI in `.env`.

## Run Frontend
```bash
cd frontend
npm install
npm run dev
```

The frontend expects the API at `http://127.0.0.1:8000/api`.

## Notes
This is a portfolio-ready starter implementation. For production, configure HTTPS, strong secrets, a managed MongoDB cluster, secure cookie/token strategy, rate limiting, backups, monitoring, and real payment-provider verification.
