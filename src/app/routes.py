from flask import Blueprint, jsonify, render_template, current_app, send_from_directory
from .utils import build_tree
import os


main = Blueprint('main', __name__)

@main.route("/")
def index():
	tree = build_tree(current_app.config['DIR_PATH'])
	return render_template("index.html", tree=tree, directory_name=current_app.config['DIR_NAME'])

@main.route("/api/files")
def list_files():
	tree = build_tree(current_app.config['DIR_PATH'])
	return jsonify(tree)

@main.route('/download/<path:filename>')
def download_file(filename):
	file_path = os.path.join(current_app.config['DIR_PATH'], filename)
	if not os.path.exists(file_path):
		return jsonify({"error": "File not found"}), 404
	if not os.access(file_path, os.R_OK):
		return jsonify({"error": "Permission denied"}), 403
	return send_from_directory(current_app.config['DIR_PATH'], filename, as_attachment=True)