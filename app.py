import eventlet
eventlet.monkey_patch() # <--- ОЧЕНЬ ВАЖНО: Делает сервер асинхронным

import sys
import subprocess
import threading
import queue
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
# Разрешаем асинхронность
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Глобальная переменная процесса
process = None
process_lock = threading.Lock()

def output_reader(proc, out_queue):
    """Читает вывод процесса (stdout)"""
    try:
        for line in iter(proc.stdout.readline, b''):
            out_queue.put(('stdout', line.decode(errors='replace')))
    except Exception:
        pass

def error_reader(proc, out_queue):
    """Читает ошибки процесса (stderr)"""
    try:
        for line in iter(proc.stderr.readline, b''):
            out_queue.put(('stderr', line.decode(errors='replace')))
    except Exception:
        pass

@app.route('/')
def index():
    return render_template('index.html')

def background_execution(code):
    """Эта функция работает в фоне и не блокирует сервер"""
    global process
    
    with process_lock:
        # Убиваем старый процесс, если есть
        if process and process.poll() is None:
            process.kill()

        try:
            process = subprocess.Popen(
                [sys.executable, '-u', '-c', code], # -u = unbuffered
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=0
            )
        except Exception as e:
            socketio.emit('terminal_output', {'text': f'Ошибка запуска: {e}\n'})
            return

    # Очередь для сбора данных от потоков
    q = queue.Queue()
    
    # Запускаем потоки чтения (они не блокируют eventlet)
    t1 = threading.Thread(target=output_reader, args=(process, q))
    t2 = threading.Thread(target=error_reader, args=(process, q))
    t1.daemon = True
    t2.daemon = True
    t1.start()
    t2.start()

    # Главный цикл чтения очереди
    while True:
        # Если процесс умер и очередь пуста — выходим
        if process.poll() is not None and q.empty():
            break
        
        try:
            # Читаем из очереди (ждем немного, чтобы не грузить ЦП)
            msg_type, line = q.get(timeout=0.05)
            socketio.emit('terminal_output', {'text': line})
        except queue.Empty:
            socketio.sleep(0.01) # Важно! Даем серверу "подышать" для обработки input
            continue
    
    socketio.emit('terminal_output', {'text': '\n--- Программа завершена ---\n'})


@socketio.on('run_code')
def run_code(data):
    """Обработчик кнопки RUN"""
    code = data.get('code')
    # Запускаем выполнение в ФОНЕ, чтобы сервер мог принимать input
    socketio.start_background_task(target=background_execution, code=code)

@socketio.on('send_input')
def send_input(data):
    """Обработчик ввода пользователя"""
    global process
    user_input = data.get('input') + '\n'
    
    if process and process.poll() is None:
        try:
            process.stdin.write(user_input.encode())
            process.stdin.flush() # Проталкиваем данные
        except Exception as e:
            socketio.emit('terminal_output', {'text': f'Ошибка ввода: {e}\n'})

@socketio.on('stop_code')
def stop_code():
    global process
    if process and process.poll() is None:
        process.kill()
        socketio.emit('terminal_output', {'text': '\n--- Остановлено пользователем ---\n'})

if __name__ == '__main__':
    print("Сервер перезапущен. Порт 5000.")
    # Используем socketio.run вместо app.run
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)