from flask import Flask, render_template, request
import os


app = Flask(__name__)

SPORTS = [
    "Cricket",
    "Hockey",
    "Football",
    "Tennis",
    "Basketball",
]


@app.route("/")
def index():
    return render_template("index.html", sports=SPORTS)


@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    email = request.form.get("email")
    contact = request.form.get("contact")
    address = request.form.get("address")
    age = request.form.get("age")
    sport = request.form.get("sport")

    if not name:
        return render_template("error.html", message="Missing name")
    if not email:
        return render_template("error.html", message="Missing email")
    if not contact:
        return render_template("error.html", message="Missing contact number")
    if not address:
        return render_template("error.html", message="Missing address")
    if not age:
        return render_template("error.html", message="Missing age")
    if not age.isdigit() or int(age) <= 0:
        return render_template("error.html", message="Invalid age")
    if not sport:
        return render_template("error.html", message="Missing sport")
    if sport not in SPORTS:
        return render_template("error.html", message="Invalid sport")

    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
