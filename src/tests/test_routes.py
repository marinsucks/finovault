import os
import tempfile
import pytest
from app import create_app

@pytest.fixture
def client():
    test_dir = tempfile.mkdtemp()
    with open(os.path.join(test_dir, "test.txt"), "w") as f:
        f.write("Hello")

    app = create_app()
    app.config['FILES_DIRECTORY'] = test_dir
    with app.test_client() as client:
        yield client

def test_api_files(client):
    response = client.get("/api/files")
    assert response.status_code == 200
    assert "test.txt" in response.get_json()

def test_download(client):
    response = client.get("/download/test.txt")
    assert response.status_code == 200
    assert response.data == b"Hello"
