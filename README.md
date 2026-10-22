# Student Marks & Grade Prediction Web App 🎓

[![CI/CD Pipeline](https://github.com/OWNER/student-grade-prediction-app/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/OWNER/student-grade-prediction-app/actions/workflows/ci-cd.yml)
[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.14-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask%203.1-black.svg)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Container-Docker-2496ED.svg)](https://www.docker.com/)
[![Tests](https://img.shields.io/badge/Tests-Pytest%20Passing-success.svg)](https://docs.pytest.org/)

An automated Machine Learning web application that predicts a student's final marks and letter grade based on their **weekly study hours** and **attendance percentage** using a Linear Regression model. Built for the **Agile Software Development DevOps (ASD DevOps) Assignment 2** at **A. P. Shah Institute of Technology**.

---

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture & Features](#architecture--features)
3. [Repository Structure](#repository-structure)
4. [Local Setup & Installation](#local-setup--installation)
5. [Running Unit Tests with Pytest](#running-unit-tests-with-pytest)
6. [Dockerization (Build & Run)](#dockerization-build--run)
7. [GitHub Actions CI/CD Pipeline](#github-actions-cicd-pipeline)
8. [API Documentation](#api-documentation)

---

## 🌟 Project Overview
- **Objective:** Automate the complete build, test, and containerized deployment workflow for a Python Flask application using GitHub Actions and Docker.
- **ML Model:** Linear Regression trained to compute final score:
  $$\text{Marks} = \beta_0 + \beta_1 \cdot \text{StudyHours} + \beta_2 \cdot \text{Attendance} + \epsilon$$
- **Grade Mapping:**
  - `90% - 100%`: Grade **A+** (Outstanding)
  - `80% - 89.9%`: Grade **A** (Excellent)
  - `70% - 79.9%`: Grade **B** (Very Good)
  - `60% - 69.9%`: Grade **C** (Good)
  - `50% - 59.9%`: Grade **D** (Pass)
  - `< 50%`: Grade **F** (Fail / At Risk)

---

## 📁 Repository Structure

```text
student-grade-prediction-app/
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # GitHub Actions 3-stage CI/CD pipeline
├── static/
│   └── css/
│       └── style.css          # Responsive styling
├── templates/
│   └── index.html             # Flask web frontend
├── tests/
│   └── test_app.py            # Comprehensive Pytest test cases
├── .dockerignore              # Files excluded from Docker build context
├── .gitignore                # Files excluded from Git tracking
├── app.py                     # Flask application factory and routes
├── Dockerfile                 # Multi-stage/slim Docker container recipe
├── model.joblib               # Serialized ML model
├── model.py                   # Model training and prediction logic
├── README.md                  # Project documentation
└── requirements.txt           # Python package dependencies
```

---

## 💻 Local Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/<YOUR_USERNAME>/student-grade-prediction-app.git
cd student-grade-prediction-app
```

### 2. Create and activate a virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
python app.py
```
Open your browser and navigate to: **`http://localhost:5000`**

---

## 🧪 Running Unit Tests with Pytest

Run the test suite locally:
```bash
pytest tests/ -v
```

Output:
```text
tests/test_app.py::test_home_page_loads PASSED
tests/test_app.py::test_predict_form_valid_submission PASSED
tests/test_app.py::test_predict_form_empty_input PASSED
tests/test_app.py::test_predict_form_out_of_bounds PASSED
tests/test_app.py::test_health_check_endpoint PASSED
tests/test_app.py::test_api_predict_valid_payload PASSED
tests/test_app.py::test_api_predict_missing_payload PASSED
tests/test_app.py::test_api_predict_invalid_values PASSED
tests/test_app.py::test_grade_calculation_thresholds PASSED
tests/test_app.py::test_model_prediction_boundary_clipping PASSED
============================== 10 passed in 2.66s ==============================
```

---

## 🐳 Dockerization (Build & Run)

### 1. Build Docker image
```bash
docker build -t student-grade-prediction:latest .
```

### 2. Run Docker container
```bash
docker run -d -p 5000:5000 --name grade-predictor student-grade-prediction:latest
```

Access the application in your browser at `http://localhost:5000`.

### 3. Verify health & stop container
```bash
curl http://localhost:5000/api/health
docker stop grade-predictor
```

---

## 🚀 GitHub Actions CI/CD Pipeline

The `.github/workflows/ci-cd.yml` workflow executes on every `push` and `pull_request` to `main` branch.

### Pipeline Stages:
1. **Build (`build`)**:
   - Checks out the repository.
   - Sets up Python 3.11 with pip caching.
   - Installs `requirements.txt`.
   - Validates Python syntax via `python -m compileall .`.
   - Generates/validates the ML model artifact `model.joblib`.
2. **Test (`test`)**:
   - Depends on `build` (`needs: build`).
   - Executes 10 automated unit and integration tests using `pytest`.
   - Generates and uploads JUnit test reports as build artifacts.
3. **Deploy (`deploy`)**:
   - Depends on `test` (`needs: test`).
   - Sets up Docker Buildx.
   - Builds the production Docker container image.
   - Spins up container, verifies `/api/health` and `/api/predict` via `curl`.
   - (Optional) Pushes container image to Docker Hub if secrets are configured.

---

## 🔌 API Documentation

### 1. Health Check
- **Endpoint:** `GET /api/health`
- **Response:**
```json
{
  "service": "student-marks-grade-prediction",
  "status": "healthy",
  "version": "1.0.0"
}
```

### 2. Predict Score & Grade
- **Endpoint:** `POST /api/predict`
- **Headers:** `Content-Type: application/json`
- **Body:**
```json
{
  "hours": 25.0,
  "attendance": 85.0
}
```
- **Response:**
```json
{
  "status": "success",
  "data": {
    "hours": 25.0,
    "attendance": 85.0,
    "predicted_marks": 81.0,
    "grade": "A",
    "remarks": "Excellent work! High chance of scoring top honours."
  }
}
```
