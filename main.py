import os
import sqlite3
from flask import Flask, flash, request, redirect, jsonify
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'zip', 'zipx', 'rar', 'tar.gz'}
DATABASE = './database.db'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=['GET'])
def endpoints():
    return '''
        <!doctype html>
        <title>EONS Marketing Solutions SEO API</title>
        <h1>SEO API</h1>
        <p>
            [POST] /upload_file (enctype=multipart/form-data)
            <ul>
                <li>[string] empresa</li>
                <li>[string] email</li>
                <li>[file] file</li>
            </ul>
        </p>
    '''


@app.route("/upload_file", methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    db_save(request.form["empresa"], request.form["email"], filename)
    return jsonify(success=True)


def db_save(company, email, filename):
    con = sqlite3.connect("database.db")
    cur = con.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS requests (id INTEGER PRIMARY KEY AUTOINCREMENT, empresa text, email text, arquivo text, status bool)")
    cur.execute(
        f"INSERT INTO requests (empresa, email, arquivo) VALUES ('{company}', '{email}', '{filename}')")

    con.commit()
    con.close()


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
