from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")
    
@app.route("/coursesearch")
def coursesearch():
    return render_template("coursesearch.html")

@app.route("/askbaldwin")
def askbaldwin():
    return render_template("askbaldwin.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/login")
def login():
    return render_template("login.html")

    
if __name__ == "__main__":
    app.run(debug=True)