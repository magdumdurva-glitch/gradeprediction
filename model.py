"""
Student Marks & Grade Prediction Model
Uses Scikit-Learn's LinearRegression to estimate student marks based on:
1. Study hours (per week)
2. Attendance percentage (0 - 100%)
"""

import os
import joblib
import numpy as np
from sklearn.linear_model import LinearRegression

MODEL_FILE_PATH = os.path.join(os.path.dirname(__file__), "model.joblib")


def train_and_save_model(file_path: str = MODEL_FILE_PATH) -> LinearRegression:
    """
    Trains a Linear Regression model using synthetic student dataset
    and saves the model artifact using joblib.
    """
    np.random.seed(42)
    n_samples = 300

    # Synthetic features:
    # Study hours per week: between 0 and 40
    study_hours = np.random.uniform(0, 40, n_samples)
    # Attendance percentage: between 40 and 100
    attendance = np.random.uniform(40, 100, n_samples)

    # Ground truth formula with Gaussian noise
    # Base intercept = 12, study hours weight = 1.35, attendance weight = 0.42
    noise = np.random.normal(0, 2.5, n_samples)
    marks = 12.0 + (1.35 * study_hours) + (0.42 * attendance) + noise
    marks = np.clip(marks, 0.0, 100.0)

    X = np.column_stack((study_hours, attendance))
    y = marks

    model = LinearRegression()
    model.fit(X, y)

    joblib.dump(model, file_path)
    return model


def get_model(file_path: str = MODEL_FILE_PATH) -> LinearRegression:
    """
    Loads the trained model from disk or trains it if not present.
    """
    if os.path.exists(file_path):
        try:
            return joblib.load(file_path)
        except Exception:
            return train_and_save_model(file_path)
    return train_and_save_model(file_path)


def calculate_grade(marks: float) -> tuple[str, str]:
    """
    Determines the letter grade and academic remark based on estimated marks.
    """
    if marks >= 90.0:
        return "A+", "Outstanding performance! Keep maintaining this standard."
    elif marks >= 80.0:
        return "A", "Excellent work! High chance of scoring top honours."
    elif marks >= 70.0:
        return "B", "Very good! Consistent revision will push you to an A."
    elif marks >= 60.0:
        return "C", "Good progress, but increasing study hours will help significantly."
    elif marks >= 50.0:
        return "D", "Pass. Needs improved attendance and structured study habits."
    else:
        return "F", "At Risk / Fail. Immediate attention and extra tutoring required."


def predict_score_and_grade(hours: float, attendance: float) -> dict:
    """
    Validates user input, predicts marks, and assigns a grade.

    Raises:
        ValueError: If input values are non-numeric or outside acceptable bounds.
    """
    try:
        hours_val = float(hours)
        attendance_val = float(attendance)
    except (TypeError, ValueError) as err:
        raise ValueError("Study hours and attendance must be valid numbers.") from err

    if hours_val < 0.0 or hours_val > 70.0:
        raise ValueError("Weekly study hours must be between 0 and 70.")

    if attendance_val < 0.0 or attendance_val > 100.0:
        raise ValueError("Attendance percentage must be between 0% and 100%.")

    model = get_model()
    features = np.array([[hours_val, attendance_val]])
    predicted_raw = model.predict(features)[0]
    predicted_marks = float(np.clip(predicted_raw, 0.0, 100.0))
    rounded_marks = round(predicted_marks, 2)

    grade, remarks = calculate_grade(rounded_marks)

    return {
        "hours": hours_val,
        "attendance": attendance_val,
        "predicted_marks": rounded_marks,
        "grade": grade,
        "remarks": remarks,
    }


if __name__ == "__main__":
    trained_model = train_and_save_model()
    print("Model successfully trained and saved to:", MODEL_FILE_PATH)
    sample = predict_score_and_grade(hours=25, attendance=85)
    print("Sample prediction:", sample)
