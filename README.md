# 🏔️ TrekTramp - Trekking Management Application

A full-stack Trekking Management Application developed using **Flask**, **Vue.js 3**, **SQLite**, **Redis**, and **Celery**. The application provides a complete platform for managing trekking events, staff assignments, participant bookings, payments, reviews, reports, and analytics through role-based access control.

---

# 📌 Project Overview

TrekTramp is designed to simplify the management of trekking activities for adventure organizations.

The system provides three different user roles:

- **Admin**
- **Trek Staff**
- **Trekker (User)**

Each role has its own dashboard and permissions to ensure secure and efficient management of trekking operations.

The application follows a REST API architecture where the Flask backend exposes APIs consumed by the Vue.js frontend.

---

# ✨ Features

## 🔐 Authentication & Security

- JWT Authentication
- Refresh Token Authentication
- Role-Based Authorization
- Secure Password Hashing
- Default Admin Creation
- First Login Password Change for Staff
- Protected API Routes

---

## 👨‍💼 Admin Features

- Dashboard Analytics
- Create New Trek
- Update Trek Information
- Soft Delete Treks
- Create Trek Staff
- Manage Staff Accounts
- Assign Staff to Treks
- Search Users
- Search Staff
- Search Treks
- View All Bookings
- Download Reports (CSV)
- Revenue Analytics
- Popular Trek Statistics
- Staff Performance Statistics

---

## 🧗 Trek Staff Features

- Staff Dashboard
- View Assigned Treks
- Search Assigned Treks
- Manage Trek Details
- Update Available Slots
- Open / Close Treks
- Start Treks
- Complete Treks
- View Registered Participants
- Search Participants

---

## 🥾 Trekker Features

- User Registration
- Login
- Update Profile
- Browse Treks
- Search Treks
- Filter Treks
- View Trek Details
- Book Trek
- Payment Simulation
- Cancel Booking
- Book Again
- View Booking History
- Write Reviews
- Edit Reviews

---

# 📋 Business Logic Implemented

- Prevent Duplicate Bookings
- Prevent Overbooking
- Booking Slot Management
- Payment Simulation
- Automatic Slot Release
- Automatic Cancellation of Unpaid Bookings
- Trek Completion Workflow
- Review Allowed Only After Trek Completion
- Booking Status Tracking
- Payment Status Tracking

---

# ⚡ Redis Caching

Redis is used to improve application performance.

Currently cached:

- Browse Treks API

Features:

- Cache Expiry
- Cache Invalidation
- Faster API Response

---

# ⚙️ Celery Background Jobs

The application uses Celery with Redis Broker.

Implemented asynchronous tasks:

### Daily Reminder

- Sends email reminders to trekkers before upcoming treks.

### Monthly Admin Report

- Generates and emails a monthly HTML report containing:
  - Total Treks
  - Total Users
  - Total Bookings
  - Revenue
  - Popular Treks

### Export Booking History

- Exports user booking history asynchronously as CSV.

### Automatic Booking Cancellation

- Automatically cancels unpaid bookings after the payment window expires.
- Releases trek slots automatically.
- Sends cancellation email to the user.

---

# 📊 Reports

Admin can download:

- Users Report
- Staff Report
- Booking Report
- Trek Report

Reports are exported in CSV format.

---

# 📈 Dashboard Analytics

The application provides:

- Total Treks
- Total Users
- Total Staff
- Total Bookings
- Revenue
- Popular Treks
- Staff Statistics
- Monthly Booking Statistics

---

# 🛠 Technology Stack

## Backend

- Flask
- SQLAlchemy
- SQLite
- Flask-JWT-Extended
- Flask-Mail
- Flask-Caching
- Redis
- Celery

## Frontend

- Vue.js 3
- Vue Router
- Axios
- Bootstrap 5
- Vite

---

# 📂 Project Structure

```
TrekTramp
│
├── backend
│   ├── models
│   ├── routes
│   ├── services
│   ├── tasks.py
│   ├── celery_app.py
│   ├── extensions.py
│   ├── config.py
│   ├── app.py
│   └── run.py
│
├── frontend
│   ├── src
│   │   ├── components
│   │   ├── layouts
│   │   ├── router
│   │   ├── services
│   │   └── views
│   │
│   └── public
│
└── README.md
```

---

# 🗄 Database

The application uses **SQLite** as the database.

The database is created automatically when the backend is started for the first time.

The default administrator account is also created automatically.

---

# 🚀 How to Run the Project

## Step 1 : Clone / Extract Project

```
cd TrekTramp
```

---

# Backend Setup

Move into backend directory.

```
cd backend
```

---

## Create Virtual Environment

Windows

```
python -m venv venv
```

Activate

```
venv\Scripts\activate
```

Linux / macOS

```
python3 -m venv venv

source venv/bin/activate
```

---

## Install Python Packages

```
pip install -r requirements.txt
```

---

## Create Environment File

Create a file named:

```
.env
```

Copy the contents from:

```
.env.example
```

Example:

```
SECRET_KEY=your_secret_key

JWT_SECRET_KEY=your_jwt_secret

SQLALCHEMY_DATABASE_URI=sqlite:///trektramp.db

REDIS_URL=redis://localhost:6379/0

MAIL_USERNAME=your_email@gmail.com

MAIL_PASSWORD=your_app_password
```

---

## Run Backend

```
python run.py
```

Backend runs at

```
http://127.0.0.1:5000
```

---

# Frontend Setup

Open another terminal.

Move to frontend.

```
cd frontend
```

Install packages.

```
npm install
```

Run Vue application.

```
npm run dev
```

Frontend runs at

```
http://localhost:5173
```

---

# Redis Setup

Start Redis server.

Windows

```
redis-server
```

Linux

```
sudo service redis-server start
```

---

# Celery Worker

Open another terminal.

```
cd backend

venv\Scripts\activate

celery -A celery_app.celery worker --pool=solo --loglevel=info
```

---

# Celery Beat Scheduler

Open another terminal.

```
cd backend

venv\Scripts\activate

celery -A celery_app.celery beat --loglevel=info
```

---

# Application URLs

Frontend

```
http://localhost:5173
```

Backend

```
http://127.0.0.1:5000
```

---

# API Documentation

The API specification is available in:

```
api.yaml
```

---

# Notes

- SQLite database is created automatically.
- Default Admin account is created automatically.
- Redis server must be running for caching.
- Celery Worker and Celery Beat must be running for background jobs.
- Email notifications require valid SMTP credentials.

---

# AI Assistance Declaration

This project was developed with the assistance of **ChatGPT (GPT-5)** as a learning and development aid.

AI assistance was primarily used for:

- Understanding Flask and Vue.js concepts
- Debugging errors
- Discussing architecture and design decisions
- Explaining Redis and Celery integration
- Reviewing and improving code quality
- Documentation assistance

The complete application architecture, feature integration, testing, debugging, customization, and final implementation were performed manually by the student.

Estimated AI Assistance: **35–40%**

---

# Developed For

**Modern Application Development II (MAD-II)**

**IIT Madras BS Degree Program**