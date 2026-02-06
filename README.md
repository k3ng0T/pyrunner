# 🐍 Python Web Terminal / Compiler

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-SocketIO-lightgrey.svg)](https://flask-socketio.readthedocs.io/)

<!-- Language Switcher -->
<div align="center">
  <a href="#english">🇬🇧 English</a> | <a href="#russian">🇷🇺 Русский</a>
</div>

---

<a name="english"></a>
## 🇬🇧 English Description

A fully functional web-based Python IDE that acts as a real terminal. Unlike client-side compilers (like Pyodide), this project runs code on your **backend server**, allowing full access to the file system, network, and Python standard libraries.

It uses **Flask** and **Socket.IO** to stream stdout/stderr in real-time and handle user input (`input()`) without freezing the browser.

### ✨ Features
*   **Real-time Output:** See `print()` results immediately as they happen (good for loops with `time.sleep`).
*   **Interactive Input:** Full support for `input()` function. The server waits for browser input.
*   **Smart Editor:**
    *   **Tab:** Inserts 4 spaces.
    *   **Enter:** Auto-indents based on the previous line.
    *   **Colons (`:`):** Automatically adds extra indentation after a colon.
*   **Process Control:** Stop/Kill button to terminate infinite loops.

### 🚀 Installation & Run

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

---
<div align="center">
  <a href="#english">⬆️ Back to Top</a>
</div>
---

<a name="russian"></a>
## 🇷🇺 Описание на Русском

Полноценная веб-IDE для Python, которая работает как настоящий терминал. В отличие от браузерных компиляторов, этот проект запускает код на **вашем сервере**, что дает полный доступ к файловой системе и библиотекам.

Использует **Flask** и **Socket.IO** для потоковой передачи вывода в реальном времени и обработки пользовательского ввода (`input()`) без зависания страницы.

### ✨ Возможности
*   **Живой вывод:** Результат `print()` появляется мгновенно (работает с `time.sleep`).
*   **Интерактивный ввод:** Полная поддержка функции `input()`. Сервер ждет, пока вы введете данные в браузере.
*   **Умный редактор:**
    *   **Tab:** Вставляет 4 пробела.
    *   **Enter:** Сохраняет отступ предыдущей строки.
    *   **Двоеточие (`:`):** Автоматически добавляет отступ на новой строке после двоеточия.
*   **Управление:** Кнопка "Stop" для экстренной остановки скрипта.

### 🚀 Установка и Запуск

1.  **Скачайте проект** и откройте папку в терминале.
2.  **Перейдите в папку проекта:**
    ```bash
    cd путь/к/папке
    ```
3.  **Создайте виртуальное окружение (обязательно):**
    ```bash
    # Linux/Mac
    python3 -m venv venv
    source venv/bin/activate

    # Windows
    python -m venv venv
    venv\Scripts\activate
    ```
4.  **Установите библиотеки:**
    ```bash
    pip install flask flask-socketio eventlet
    ```
5.  **Запустите сервер:**
    ```bash
    python app.py
    ```
6.  **Откройте в браузере:**
    Перейдите по адресу `http://127.0.0.1:5000`

### 🔧 Решение проблем
*   **TemplateNotFound: index.html**: Убедитесь, что файл `index.html` лежит внутри папки `templates`.
*   **Address already in use**: Порт 5000 занят. Остановите старый процесс или убейте его командой `fuser -k 5000/tcp` (Linux).

### ⚠️ Предупреждение о безопасности
**НЕ ЗАПУСКАЙТЕ ЭТОТ САЙТ В ОБЩЕМ ИНТЕРНЕТЕ.**
Приложение выполняет любой код на вашем компьютере. Если открыть доступ извне, любой пользователь сможет удалить ваши файлы. Используйте только локально (`localhost`).

<div align="center">
  <a href="#russian">⬆️ Наверх</a>
</div>