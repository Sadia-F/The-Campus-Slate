from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Welcome to The Campus Slate</h1><p>Your college news, all in one place.</p>"

if __name__ == "__main__":
    app.run(debug=True)
    