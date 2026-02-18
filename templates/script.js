const socket = io();
const terminal = document.getElementById('terminal');
const termInput = document.getElementById('term-input');
const codeEditor = document.getElementById('code');

// ==========================================
// TAB AND INDENT LOGIC (MOST IMPORTANT)
// ==========================================
codeEditor.addEventListener('keydown', function(e) {
    // 1. Handle TAB key
    if (e.key === 'Tab') {
        e.preventDefault(); // Cancel focus loss
        const start = this.selectionStart;
        const end = this.selectionEnd;

        // Insert 4 spaces
        this.value = this.value.substring(0, start) + "    " + this.value.substring(end);

        // Return cursor to position (after spaces)
        this.selectionStart = this.selectionEnd = start + 4;
    }

    // 2. Handle ENTER key (Auto-indent)
    if (e.key === 'Enter') {
        e.preventDefault();
        const start = this.selectionStart;
        const end = this.selectionEnd;
        const value = this.value;

        // Find current line start
        const lastNewLine = value.lastIndexOf('\n', start - 1);
        const currentLineStart = lastNewLine + 1;
        // Get current line text before cursor
        const currentLine = value.substring(currentLineStart, start);

        // Count current spaces at line start (indent)
        const match = currentLine.match(/^(\s*)/);
        const currentIndent = match && match[1] ? match[1] : '';

        // Check if line ends with colon (ignoring trailing spaces)
        let newIndent = currentIndent;
        if (currentLine.trimEnd().endsWith(':')) {
            newIndent += "    "; // Add 4 more spaces
        }

        // Insert new line + indent
        const insert = "\n" + newIndent;
        this.value = value.substring(0, start) + insert + value.substring(end);

        // Place cursor at end of indent
        this.selectionStart = this.selectionEnd = start + insert.length;
        
        // Scroll to cursor if needed
        this.blur();
        this.focus();
    }
});

// ==========================================
// SERVER LOGIC
// ==========================================

socket.on('terminal_output', function(msg) {
    terminal.innerText += msg.text;
    terminal.scrollTop = terminal.scrollHeight;
});

function runCode() {
    const code = codeEditor.value;
    terminal.innerText = "=== Running ===";
    socket.emit('run_code', {code: code});
    termInput.focus();
}

function stopCode() {
    socket.emit('stop_code');
}

termInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        const text = termInput.value;
        terminal.innerText += text + "\n";
        socket.emit('send_input', {input: text});
        termInput.value = '';
    }
});

// Hotkey Ctrl+Enter to run
document.addEventListener('keydown', function(e) {
    if (e.ctrlKey && e.key === 'Enter') {
        runCode();
    }
});