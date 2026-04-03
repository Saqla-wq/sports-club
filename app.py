import csv
import os
import re
from datetime import datetime
from pathlib import Path

from flask import Flask, flash, render_template, request


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

SPORTS = [
    "Cricket",
    "Hockey",
    "Football",
    "Tennis",
    "Basketball",
]

DATA_DIR = Path("data")
REGISTRATIONS_FILE = DATA_DIR / "registrations.csv"
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
CONTACT_PATTERN = re.compile(r"^[0-9+\-\s]{7,20}$")


def get_form_data():
    return {
        "name": request.form.get("name", "").strip(),
        "email": request.form.get("email", "").strip(),
        "contact": request.form.get("contact", "").strip(),
        "address": request.form.get("address", "").strip(),
        "age": request.form.get("age", "").strip(),
        "sport": request.form.get("sport", "").strip(),
    }


def validate_registration(form_data):
    errors = []

    if not form_data["name"]:
        errors.append("Name is required.")
    if not form_data["email"]:
        errors.append("Email is required.")
    elif not EMAIL_PATTERN.match(form_data["email"]):
        errors.append("Please enter a valid email address.")

    if not form_data["contact"]:
        errors.append("Contact number is required.")
    elif not CONTACT_PATTERN.match(form_data["contact"]):
        errors.append("Contact number should contain only digits, spaces, + or -.")

    if not form_data["address"]:
        errors.append("Address is required.")

    if not form_data["age"]:
        errors.append("Age is required.")
    elif not form_data["age"].isdigit():
        errors.append("Age must be a number.")
    else:
        age = int(form_data["age"])
        if age < 5 or age > 100:
            errors.append("Age must be between 5 and 100.")

    if not form_data["sport"]:
        errors.append("Sport is required.")
    elif form_data["sport"] not in SPORTS:
        errors.append("Please choose a valid sport.")

    return errors


def save_registration(form_data):
    DATA_DIR.mkdir(exist_ok=True)
    file_exists = REGISTRATIONS_FILE.exists()

    with REGISTRATIONS_FILE.open("a", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "registered_at",
            "name",
            "email",
            "contact",
            "address",
            "age",
            "sport",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow(
            {
                "registered_at": datetime.now().isoformat(timespec="seconds"),
                **form_data,
            }
        )


@app.route("/")
def index():
    return render_template("index.html", sports=SPORTS, form_data={})


@app.route("/register", methods=["POST"])
def register():
    form_data = get_form_data()
    errors = validate_registration(form_data)

    if errors:
        for error in errors:
            flash(error, "error")
        return render_template("index.html", sports=SPORTS, form_data=form_data), 400

    save_registration(form_data)
    return render_template("success.html", name=form_data["name"], sport=form_data["sport"])


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    debug = os.environ.get("FLASK_DEBUG", "true").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
