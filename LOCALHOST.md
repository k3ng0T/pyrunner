# 💻 Localhost Installation Guide

<div align="center">
  <a href="README.md">⬅️ Back to Presentation</a> | 
  <b>🇬🇧 English</b> | 
  <a href="LOCALHOST.ru.md">🇷🇺 Русский</a>
</div>

---

### Prerequisites
*   Python 3.8+ installed.
*   `pip` (Python package manager).

### Step-by-Step Installation

1.  **Clone or download** the repository.
2.  **Navigate to the project folder:**
    ```bash
    cd path/to/project
    ```
3.  **Create a virtual environment:**
    ```bash
    # Linux/Mac
    python3 -m venv venv
    source venv/bin/activate

    # Windows
    python -m venv venv
    venv\Scripts\activate
    ```
4.  **Install dependencies:**
    ```bash
    pip install flask flask-socketio eventlet
    ```
5.  **Run the server:**
    ```bash
    python app.py
    ```
6.  **Open in browser:**
    Go to `http://127.0.0.1:5000`

### ⚠️ Security Warning
**DO NOT HOST THIS PUBLICLY.**
This application executes arbitrary code on your machine. If you host this on a public IP, anyone can delete your files or run malicious commands. Use it only on `localhost` (127.0.0.1).