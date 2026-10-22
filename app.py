"""
Student Marks & Grade Prediction Web App
Flask Web Application with REST endpoints and Pytest-ready routes.
"""

from flask import Flask, render_template, request, jsonify
from model import predict_score_and_grade, get_model


def create_app():
    app = Flask(__name__)

    # Pre-load/train model on application startup
    get_model()

    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.html")

    @app.route("/predict", methods=["POST"])
    def predict_form():
        try:
            hours = request.form.get("hours", "").strip()
            attendance = request.form.get("attendance", "").strip()

            if not hours or not attendance:
                return render_template(
                    "index.html",
                    error="Please provide both Study Hours and Attendance percentage.",
                    hours=hours,
                    attendance=attendance,
                ), 400

            result = predict_score_and_grade(hours=hours, attendance=attendance)
            return render_template("index.html", result=result, hours=hours, attendance=attendance)

        except ValueError as e:
            return render_template(
                "index.html",
                error=str(e),
                hours=request.form.get("hours", ""),
                attendance=request.form.get("attendance", ""),
            ), 400
        except Exception:
            return render_template(
                "index.html",
                error="An unexpected server error occurred during prediction.",
            ), 500

    @app.route("/api/predict", methods=["POST"])
    def predict_api():
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"status": "error", "message": "JSON body is required"}), 400

        hours = data.get("hours")
        attendance = data.get("attendance")

        if hours is None or attendance is None:
            return jsonify({
                "status": "error",
                "message": "Both 'hours' and 'attendance' fields are required.",
            }), 400

        try:
            result = predict_score_and_grade(hours=hours, attendance=attendance)
            return jsonify({"status": "success", "data": result}), 200
        except ValueError as e:
            return jsonify({"status": "error", "message": str(e)}), 400
        except Exception as e:
            return jsonify({"status": "error", "message": "Internal error"}), 500

    @app.route("/api/health", methods=["GET"])
    def health_check():
        return jsonify({
            "status": "healthy",
            "service": "student-marks-grade-prediction",
            "version": "1.0.0",
        }), 200

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("index.html", error="404 - Page not found."), 404

    @app.errorhandler(500)
    def internal_error(e):
        return render_template("index.html", error="500 - Internal server error."), 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
