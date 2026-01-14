# Smart Attendance MVP

A QR-based smart attendance system with a live backend, student check-in page, and faculty analytics dashboard.

---

## 🚀 Live System

- **Backend API (FastAPI – deployed):**  
  https://smartattendance-mvp.onrender.com

- **Swagger API Docs:**  
  https://smartattendance-mvp.onrender.com/docs

---

## 🧩 System Overview

This project consists of three main parts:

### 1️⃣ Backend (FastAPI)
- Creates attendance sessions
- Marks student attendance
- Pushes data to Google Sheets
- Provides analytics-ready data
- Exposes REST APIs with Swagger docs

### 2️⃣ Student Attendance Page (Web UI)
- Simple web page for students
- Students submit attendance using Session ID / QR
- Connected directly to live backend APIs

### 3️⃣ Faculty Dashboard (Analytics)
- Attendance data stored in Google Sheets
- Analytics visualized using Looker Studio
- Faculty can track attendance percentage, sessions, trends

---

## ✨ Features

- Session creation
- Attendance marking
- Google Sheets integration
- Analytics export
- Swagger API documentation
- Deployed backend (no local setup required for demo)

---

## 🛠 Tech Stack

- **Backend:** FastAPI (Python)
- **Database:** SQLite
- **Sheets:** Google Sheets API
- **Analytics:** Looker Studio
- **Hosting:** Render
- **Frontend:** HTML, CSS, JavaScript

---

## 🧪 How to Use (Demo Flow)

### Step 1: Create a Session
- Open Swagger UI: `/docs`
- Call `POST /session/create`
- Copy the generated `session_id`

### Step 2: Student Marks Attendance
- Open Student Attendance Page
- Enter `session_id`
- Submit attendance

### Step 3: Faculty Views Analytics
- Open the connected Google Sheet
- View analytics dashboard (Looker Studio)

---

## 💻 Run Locally (Optional)

pip install -r requirements.txt

uvicorn main:app --reload
