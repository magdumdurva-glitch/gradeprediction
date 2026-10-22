"""
Automated Pytest Suite for Student Marks & Grade Prediction Web App.
Covers:
- Flask Web Route Unit Testing
- REST API Endpoint Testing
- ML Prediction & Boundary Logic Testing
"""

import pytest
from app import create_app
from model import calculate_grade, predict_score_and_grade


@pytest.fixture
def client():
    """Configures a Flask test client."""
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ==========================================================
# 1. Web Route Tests
# ==========================================================

def test_home_page_loads(client):
    """GET / should return 200 OK and render the prediction form."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Student Marks &amp; Grade Predictor" in response.data or b"Student Marks & Grade Predictor" in response.data
    assert b"Weekly Study Hours" in response.data
    assert b"Attendance Percentage" in response.data


def test_predict_form_valid_submission(client):
    """POST /predict with valid form data should compute and display grade."""
    response = client.post(
        "/predict",
        data={"hours": "25", "attendance": "85"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Prediction Results" in response.data
    assert b"Grade:" in response.data
    assert b"25" in response.data


def test_predict_form_empty_input(client):
    """POST /predict with missing input should return 400 and an error message."""
    response = client.post(
        "/predict",
        data={"hours": "", "attendance": ""},
    )
    assert response.status_code == 400
    assert b"Please provide both Study Hours and Attendance percentage." in response.data


def test_predict_form_out_of_bounds(client):
    """POST /predict with out-of-range hours should return 400 and validation error."""
    response = client.post(
        "/predict",
        data={"hours": "120", "attendance": "90"},
    )
    assert response.status_code == 400
    assert b"Weekly study hours must be between 0 and 70" in response.data


# ==========================================================
# 2. REST API Endpoint Tests
# ==========================================================

def test_health_check_endpoint(client):
    """GET /api/health should return status 200 and healthy JSON payload."""
    response = client.get("/api/health")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["status"] == "healthy"
    assert json_data["service"] == "student-marks-grade-prediction"


def test_api_predict_valid_payload(client):
    """POST /api/predict with valid JSON should return predicted score and grade."""
    payload = {"hours": 30, "attendance": 90}
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert "predicted_marks" in data["data"]
    assert "grade" in data["data"]
    assert 0.0 <= data["data"]["predicted_marks"] <= 100.0


def test_api_predict_missing_payload(client):
    """POST /api/predict without JSON body should return 400."""
    response = client.post(
        "/api/predict",
        data="not a json",
        content_type="text/plain",
    )
    assert response.status_code == 400


def test_api_predict_invalid_values(client):
    """POST /api/predict with negative attendance should return 400."""
    payload = {"hours": 15, "attendance": -10}
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "error"
    assert "Attendance percentage must be between 0% and 100%" in data["message"]


# ==========================================================
# 3. Model & Logic Unit Tests
# ==========================================================

def test_grade_calculation_thresholds():
    """Unit test verify grade assignment for various score thresholds."""
    grade, _ = calculate_grade(95.0)
    assert grade == "A+"
    grade, _ = calculate_grade(85.0)
    assert grade == "A"
    grade, _ = calculate_grade(75.0)
    assert grade == "B"
    grade, _ = calculate_grade(65.0)
    assert grade == "C"
    grade, _ = calculate_grade(55.0)
    assert grade == "D"
    grade, _ = calculate_grade(42.0)
    assert grade == "F"


def test_model_prediction_boundary_clipping():
    """Ensure predicted marks never exceed 100 or drop below 0."""
    # Maximum inputs
    max_res = predict_score_and_grade(hours=70, attendance=100)
    assert max_res["predicted_marks"] <= 100.0

    # Minimum inputs
    min_res = predict_score_and_grade(hours=0, attendance=0)
    assert min_res["predicted_marks"] >= 0.0
