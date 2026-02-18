# ⚡ Python Remote Execution Environment (Web Terminal)

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-SocketIO-lightgrey.svg)](https://flask-socketio.readthedocs.io/)
[![Architecture](https://img.shields.io/badge/Architecture-Async%20Subprocess-orange.svg)]()

<!-- Language Switcher -->
<div align="center">
  <h3>
    🇬🇧 English | <a href="README.ru.md">🇷🇺 Русский</a>
  </h3>
</div>

---

## Concept & Architecture

This project is not just a syntax highlighter. It is a **fully asynchronous remote execution engine** that brings the power of a local terminal to the browser.

Most web-based Python runners fail at two things:
1.  **Blocking I/O:** They freeze when `time.sleep()` is called.
2.  **Interactivity:** They cannot handle `input()` requests without halting the entire server.

**This project solves both.** It creates a bridge between the Web Interface and the Server Kernel using WebSockets, allowing for real-time, bi-directional communication.

### 🛠 Under the Hood: How it Works

The magic lies in how the server manages processes. It doesn't just `eval()` code.

1.  **Process Isolation:** When you click "Run", the server spawns a completely separate OS subprocess (`subprocess.Popen`). This ensures the server remains responsive even if the user code crashes or loops infinitely.
2.  **Non-Blocking Streams:** Background threads monitor the `stdout` and `stderr` pipes of the subprocess.
3.  **Real-Time Transport:** As soon as the Python process outputs a line, it is pushed into a queue and immediately emitted to the frontend via **Socket.IO**.
4.  **Interactive Input:** When the Python process requests input, it pauses. The server stays alive. When you type in the browser, the data is sent via WebSocket and injected directly into the subprocess's `stdin`.

### 🚀 Capabilities

*   **True Interactivity:** Run scripts that require user input (`input()`) just like in a real console.
*   **Live Streaming:** Watch loops execute in real-time (perfect for scripts with delays or progress bars).
*   **Smart Editor:** A custom-built logic for the `textarea` that handles indentation (Tabs) and auto-formatting (Enter after `:`) similarly to VS Code.
*   **Process Control:** Full control over the lifecycle. You can kill/terminate running scripts instantly.

### 📥 Installation & Usage
To run this project on your local machine, please refer to the installation guide:

👉 **[READ INSTALLATION GUIDE (LOCALHOST.md)](LOCALHOST.md)**