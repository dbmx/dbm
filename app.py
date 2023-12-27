from flask import Flask, render_template

# Create Flask Instance
app = Flask(__name__)


@app.route("/")
def index():
    first_name = "John"
    return render_template("index.html", first_name=first_name)


@app.route("/user/<name>")
def user(name):
    return render_template("user.html", user_name=name)


# Create Custom Error Pages


# Invaild URL - Fixed.
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# Invaild Server Error - Fixed.
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=True)
