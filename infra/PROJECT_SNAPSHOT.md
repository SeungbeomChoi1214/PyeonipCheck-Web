# PROJECT_SNAPSHOT.md


## 🏗️ Project Structure
# 2026-1-2 UPDATE

TP_Vscode/
├── frontend/ // React.js UI Application
│ ├── src/
│ │ ├── components/ // UI Components
│ │ │ ├── PredictPage.js // Main prediction results display
│ │ │ ├── UniversitySelector.js // University selection interface
│ │ │ ├── ScoreInput.js // Score input form
│ │ │ └── ResultDashboard.js // Analytics dashboard
│ │ ├── App.js // Main React app component
│ │ └── index.js // React entry point
│ ├── package.json // Frontend dependencies
│ └── public/ // Static assets
├── scripts/ // Data processing & migration scripts
│ ├── generate_simulation.py // Student score simulation generator
│ ├── update_tiers.py // University tier bulk updater
│ ├── update_tuk_data.py // TUK-specific data injector
│ └── verify_data.py // Database integrity checker
├── pdfs/ // University admission guideline PDFs
├── output/ // Processed data exports
├── raw_data/ // Raw extracted data
├── main.py // FastAPI backend server
├── models.py // SQLAlchemy ORM models
├── services.py // Business logic & algorithms
├── database.py // Database connection & session management
├── requirements.txt // Python dependencies
├── university.db // SQLite database file
└── TP_Simulation_Data.xlsx // Master simulation dataset

## 🛠️ Tech Stack Summary

### Backend
- **Framework**: FastAPI 0.128.0
- **Database**: SQLite with SQLAlchemy 2.0.45 ORM
- **Data Processing**: Pandas 2.3.3, NumPy 2.4.0, SciPy 1.16.3
- **PDF Processing**: PyPDF2, pdfplumber 0.11.8
- **Server**: Uvicorn 0.40.0

### Frontend
- **Framework**: React 18.3.1
- **HTTP Client**: Axios 1.13.2
- **Animation**: Framer Motion 11.18.2
- **Charts**: Recharts 2.15.4
- **Build Tool**: React Scripts 5.0.1

### Database Schema
- **Universities**: Tier system (S/A/B/C), waitlist ratios, exam types
- **AdmissionTracks**: Major/General tracks with statistical distributions
- **StudentScores**: Real + simulated applicant data with spam detection

## 🔑 Key Module Description

### `main.py` - FastAPI Backend Server
Core API server providing university admission prediction endpoints. Implements tier-based ranking algorithms using normal distribution calculations and waitlist analysis for 36+ Korean universities.

### `models.py` - Database Schema Definition
SQLAlchemy ORM models defining university tiers, admission tracks, and student scoring system. Features enum-based tier classification (S/A/B/C) with corresponding waitlist ratios and exam type configurations.

### `services.py` - Business Logic Engine
Contains core algorithms for department-to-track mapping, tier-based standard deviation calculations, and intelligent waitlist insight generation. Implements keyword-based major classification and university-specific analysis comments.

### `frontend/src/components/PredictPage.js` - Main UI Component
React component rendering comprehensive admission analysis results with animated charts, gap analysis, and expert insights. Features responsive design with tier-based color coding and dynamic waitlist recommendations.

### `scripts/generate_simulation.py` - Data Simulation Engine
Generates realistic student score distributions for 500+ applicants per department using tier-adjusted normal distributions. Processes Excel-based university data and applies keyword-based score corrections for accurate modeling.

## 📊 System Architecture

**Data Flow**: PDF → Raw Data → Excel Processing → SQLite → FastAPI → React UI
**Prediction Engine**: Tier-based σ adjustment → Normal distribution ranking → Waitlist analysis → Expert insights
**Scalability**: Modular script system for bulk university data updates and tier management

## 🎯 Business Domain

Korean university transfer admission prediction system with focus on engineering and business programs. Provides data-driven insights for 36+ universities with tier-based competition analysis and waitlist probability calculations.