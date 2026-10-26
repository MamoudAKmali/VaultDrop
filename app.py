import os
from flask import Flask, render_template

app = Flask(__name__)


# ─── الصفحة الرئيسية ────────────────────────────────────────────────────────
@app.route('/')
def home():
    return render_template('secure-fileshare.html')


if __name__ == '__main__':
    app.run(debug=True)