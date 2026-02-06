import eventlet
eventlet.monkey_patch() # <--- VERY IMPORTANT: Makes the server asynchronous

import sys
import subprocess
import threading
import queue
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
# Enable asynchronous mode
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Global process variable
process = None
process_lock = threading.Lock()

def output_reader(proc, out_queue):
    """Reads process output (stdout)"""
    try:
        for line in iter(proc.stdout.readline, b''):
            out_queue.put(('stdout', line.decode(errors='replace')))
    except Exception:
        pass

def error_reader(proc, out_queue):
    """Reads process errors (stderr)"""
    try:
        for line in iter(proc.stderr.readline, b''):
            out_queue.put(('stderr', line.decode(errors='replace')))
    except Exception:
        pass

@app.route('/')
def index():
    return render_template('index.html')

def background_execution(code):
    """This function runs in the background and doesn't block the server"""
    global process
    
    with process_lock:
        # Kill old process if exists
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
            socketio.emit('terminal_output', {'text': f'Execution error: {e}\n'})
            return

    # Queue for collecting data from threads
    q = queue.Queue()
    
    # Start reading threads (they don't block eventlet)
    t1 = threading.Thread(target=output_reader, args=(process, q))
    t2 = threading.Thread(target=error_reader, args=(process, q))
    t1.daemon = True
    t2.daemon = True
    t1.start()
    t2.start()

    # Main queue reading loop
    while True:
        # If process died and queue is empty - exit
        if process.poll() is not None and q.empty():
            break
        
        try:
            # Read from queue (wait a bit to not overload CPU)
            msg_type, line = q.get(timeout=0.05)
            socketio.emit('terminal_output', {'text': line})
        except queue.Empty:
            socketio.sleep(0.01) # Important! Give server time to process input
            continue
    
    socketio.emit('terminal_output', {'text': '\n--- Program finished ---\n'})


@socketio.on('run_code')
def run_code(data):
    """RUN button handler"""
    code = data.get('code')
    # Run in BACKGROUND so server can accept input
    socketio.start_background_task(target=background_execution, code=code)

@socketio.on('send_input')
def send_input(data):
    """User input handler"""
    global process
    user_input = data.get('input') + '\n'
    
    if process and process.poll() is None:
        try:
            process.stdin.write(user_input.encode())
            process.stdin.flush() # Push the data
        except Exception as e:
            socketio.emit('terminal_output', {'text': f'Input error: {e}\n'})

@socketio.on('stop_code')
def stop_code():
    global process
    if process and process.poll() is None:
        process.kill()
        socketio.emit('terminal_output', {'text': '\n--- Stopped by user ---\n'})

if __name__ == '__main__':
    print("Server restarted. Port 5000.")
    # Use socketio.run instead of app.run
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)