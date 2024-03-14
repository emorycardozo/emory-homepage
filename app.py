from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


# if __name__ == "__main__":
#     app.run(debug=True)

@app.route("/resume")
def resume():
    return render_template("resume.html")


@app.route("/unama")
def unama():
    return render_template("unama.html")


@app.route("/diogosenior")
def diogosenior():
    return render_template("diogosenior.html")


@app.route("/priscilasenior")
def priscilasenior():
    return render_template("priscilasenior.html")


@app.route("/eldorado")
def eldorado():
    return render_template("eldorado.html")


@app.route("/hellenmonarcha")
def hellenmonarcha():
    return render_template("hellenmonarcha.html")


@app.route("/eu")
def emory():
    return render_template("emorycardozo.html")


@app.route("/linktree")
def linktree():
    return render_template("linktree.html")


@app.route("/agenda")
def agenda():
    return render_template("agenda.html")
