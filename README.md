# Smart Attendance MVP

A cloud-based automated student attendance monitoring and analytics system built for hackathon MVP submission.

## Problem
Manual attendance is time-consuming, error-prone, and lacks analytics for identifying disengaged or at-risk students.

## Solution
A session-based automated attendance system where faculty create time-bound sessions and students mark attendance digitally. Attendance data is stored in Google Sheets and analytics help identify attendance patterns and at-risk students.

## Features
- Faculty session creation (time-bound)
- Student attendance marking using session ID
- Attendance analytics and at-risk student identification
- Google Sheets as cloud database
- Swagger API documentation

## Tech Stack
- Backend: FastAPI (Python)
- Database: Google Sheets API (Google technology)
- Frontend: HTML + JavaScript
- Hosting:
  - Backend: Render
  - Frontend: Netlify

## Live Demo
- Frontend Web App: **https://smartattendance-mvp.netlify.app/**
- Backend API (Swagger): **https://smartattendance-mvp.onrender.com/docs**

## Run Locally
pip install -r requirements.txt
uvicorn main:app --reload
