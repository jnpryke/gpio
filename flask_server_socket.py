from flask import Flask, render_template_string, request
import socket

app = Flask(__name__)

# HTML template with buttons and dark theme
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>GPIO Control</title>
    <style>
        body {
            background-color: #121212;
            color: #ffffff;
            font-family: Arial, sans-serif;
        }
        h1 {
            text-align: center;
        }
        form {
            display: flex;
            justify-content: center;
            gap: 20px;
        }
        button {
            background-color: #1f1f1f;
            color: #ffffff;
            border: 1px solid #ffffff;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
        }
        button:hover {
            background-color: #333333;
        }
    </style>
</head>
<body>
    <h1>GPIO Control</h1>
    <form method="POST" action="/control">
        <button name="action" value="on" type="submit">Turn On</button>
        <button name="action" value="off" type="submit">Turn Off</button>
    </form>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/control', methods=['POST'])
def control():
    action = request.form['action']
    send_command(action)
    return render_template_string(html_template)

def send_command(command):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 65432))
    client_socket.send(command.encode())
    client_socket.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
