# Finovault 📂

**Author:** Marin Becker  
**Contact:** hello@marinbecker.me

## Description

Finovault is a simple, secure, and dockerized web application built with Python (Flask) that allows you to **list** and **download files** from a directory mounted as a Docker volume.  
It is designed for easy deployment and sharing of files in a controlled environment.

---

## Features

- Lists and downloads files from a mounted directory on a modern web UI (Tailwind CSS)
- Direct file download endpoint (`GET /download/<path>`)
- REST API for JSON file tree (`GET /api/files`)
- Dockerized for easy deployment
- Configurable via environment variables
- Automated tests (pytest) included

---

## Quickstart

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/finovault.git
cd finovault
```

### 2. Build the Docker image and run the container

You must specify the directory to serve using the `FINOVAULT_DIR` environment variable (defaults to `./tests/files` if not set):

```bash
export FINOVAULT_DIR=/path_to_your_directory
make
```
or manually:
```bash
docker build -t finovault .

docker run -d \
  -p 5000:5000 \
  -v /path_to_your_directory:/data \
  -e DIR_NAME=$(realpath /path_to_your_directory) \
  --name finovault \
  finovault
```

- Replace `/path_to_your_directory` with the path to the directory you want to share.

### 4. Access the app

Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## Endpoints

| Method | URL                | Description                                 |
|--------|--------------------|---------------------------------------------|
| GET    | `/`                | Web UI listing files to download            |
| GET    | `/download/<path>` | Download the specified file                 |
| GET    | `/api/files`       | Returns the file tree as JSON               |

---

## API Example

### List files (JSON)

```bash
curl http://localhost:5000/api/files
```

**Response:**
```json
{
  "__files__": ["file1.txt", "file2.pdf"],
  "subfolder": {
    "__files__": ["image.png"]
  }
}
```

### Download a file

```bash
curl -O http://localhost:5000/download/cool_song.mp3
```

---

## Running Tests

Tests are run inside the container.  
To execute all tests:

```bash
make tests
```
or manually:
```bash
docker exec -e PYTHONPATH=/src finovault pytest /tests/tests.py -v --color=yes
```

---

## License

MIT License © 2025 Marin Becker


