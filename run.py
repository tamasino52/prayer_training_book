from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

app = Flask(__name__, static_folder='static')
Bootstrap(app)


@app.route('/')
def episode():
    return render_template('book.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
