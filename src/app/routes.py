from flask import Blueprint, jsonify, send_from_directory, render_template, current_app
from .utils import build_tree


main = Blueprint('main', __name__)

@main.route("/")
def index():
    tree = build_tree(current_app.config['DIR_PATH'])
    return render_template("index.html", tree=tree, directory_name=current_app.config['DIR_NAME'])

@main.route("/api/files")
def list_files():
    tree = build_tree(current_app.config['DIR_PATH'])
    return jsonify(tree)

@main.route("/download/<path:filename>")
def download_file(filename):
	try:
		return send_from_directory(current_app.config['DIR_PATH'], filename, as_attachment=True)
	except FileNotFoundError:
		return jsonify({"error": "File not found"}), 404
	except PermissionError:
		return jsonify({"error": "Permission denied"}), 403
	except Exception:
		return jsonify({"error": "Unable to access file"}), 500
