from flask import Flask, render_template

app = Flask(
    __name__, template_folder=".", static_folder="./data", static_url_path="/data"
)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
