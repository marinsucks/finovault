from flask import Blueprint, jsonify, send_from_directory, render_template, current_app
import os

main = Blueprint('main', __name__)

@main.route("/")
def index():
    files = os.listdir(current_app.config['FINOVAULT_DATA'])
    return render_template("index.html", files=files)

@main.route("/api/files")
def list_files():
    files = os.listdir(current_app.config['FINOVAULT_DATA'])
    return jsonify(files)

@main.route("/download/<path:filename>")
def download_file(filename):
    return send_from_directory(current_app.config['FINOVAULT_DATA'], filename, as_attachment=True)
