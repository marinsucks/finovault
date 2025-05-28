import os
import tempfile
import shutil
import pytest
from flask import Flask
from app.utils import build_tree
from app import create_app



# ---------- UNIT TESTS FOR build_tree ----------

def test_build_tree_empty_dir():
	with tempfile.TemporaryDirectory() as tmpdir:
		tree = build_tree(tmpdir)
		assert tree == {}

def test_build_tree_files_only():
	with tempfile.TemporaryDirectory() as tmpdir:
		filenames = ['a.txt', 'b.txt']
		for fname in filenames:
			open(os.path.join(tmpdir, fname), 'w').close()
		tree = build_tree(tmpdir)
		assert set(tree['__files__']) == set(filenames)

def test_build_tree_nested_dirs():
	with tempfile.TemporaryDirectory() as tmpdir:
		os.makedirs(os.path.join(tmpdir, 'dir1/dir2'))
		open(os.path.join(tmpdir, 'file1.txt'), 'w').close()
		open(os.path.join(tmpdir, 'dir1', 'file2.txt'), 'w').close()
		open(os.path.join(tmpdir, 'dir1', 'dir2', 'file3.txt'), 'w').close()
		tree = build_tree(tmpdir)
		assert '__files__' in tree
		assert 'dir1' in tree
		assert '__files__' in tree['dir1']
		assert 'dir2' in tree['dir1']
		assert '__files__' in tree['dir1']['dir2']

def test_build_tree_permission_denied(tmp_path):
	subdir = tmp_path / "noaccess"
	subdir.mkdir()
	file = subdir / "file.txt"
	file.write_text("secret")
	# Remove read permissions
	subdir.chmod(0o000)
	try:
		with pytest.raises(PermissionError):
			build_tree(str(subdir))
	finally:
		# Restore permissions so pytest can clean up
		subdir.chmod(0o700)

# ---------- FLASK APP INTEGRATION TESTS ----------

@pytest.fixture
def client(tmp_path):
	# Copy test files into a temp dir
	test_files_dir = os.path.join(os.path.dirname(__file__), "files")
	temp_data_dir = tmp_path / "data"
	shutil.copytree(test_files_dir, temp_data_dir)
	app = create_app()
	app.config['TESTING'] = True
	app.config['DIR_PATH'] = str(temp_data_dir)
	app.config['DIR_NAME'] = "Test Files"
	with app.test_client() as client:
		yield client

def test_index_route(client):
	resp = client.get("/")
	assert resp.status_code == 200
	assert b"Test Files" in resp.data

def test_api_files_route(client):
	resp = client.get("/api/files")
	assert resp.status_code == 200
	data = resp.get_json()
	assert isinstance(data, dict)
	assert "__files__" in data or data  # could be empty

def test_download_existing_file(client):
	resp = client.get("/download/cool_song.mp3")
	assert resp.status_code == 200
	assert resp.headers['Content-Disposition'].startswith('attachment;')

def test_download_file_in_subdir(client):
	resp = client.get("/download/privatepics/mycrush.jpg")
	assert resp.status_code == 200
	assert resp.headers['Content-Disposition'].startswith('attachment;')

def test_download_nonexistent_file(client):
	resp = client.get("/download/does_not_exist.txt")
	assert resp.status_code == 404
	assert resp.get_json()["error"] == "File not found"

def test_download_permission_denied(client, tmp_path):
	# Create a file with no read permissions
	secret_dir = tmp_path / "secret"
	secret_dir.mkdir()
	secret_file = secret_dir / "secret.txt"
	secret_file.write_text("top secret")
	secret_file.chmod(0o000)
	app = create_app()
	app.config['TESTING'] = True
	app.config['DIR_PATH'] = str(tmp_path)
	app.config['DIR_NAME'] = "Test Files"
	with app.test_client() as test_client:
		try:
			resp = test_client.get(f"/download/secret/secret.txt")
			assert resp.status_code == 403
			assert resp.get_json()["error"] == "Permission denied"
		finally:
			secret_file.chmod(0o600)