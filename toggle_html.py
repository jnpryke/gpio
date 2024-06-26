from flask import Flask, render_template_string, request
import socket

app = Flask(__name__)

# HTML template with toggles for each GPIO pin and a submit button
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
            flex-direction: column;
            align-items: center;
            gap: 10px;
        }
        .toggle {
            display: flex;
            align-items: center;
            gap: 10px;
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
        <div class="toggle">
            <label for="pin1">Pin 5:</label>
            <input type="checkbox" id="pin1" name="pin1">
        </div>
        <div class="toggle">
            <label for="pin2">Pin 4:</label>
            <input type="checkbox" id="pin2" name="pin2">
        </div>
        <div class="toggle">
            <label for="pin3">Pin 9:</label>
            <input type="checkbox" id="pin3" name="pin3">
        </div>
        <div class="toggle">
            <label for="pin4">Pin 91:</label>
            <input type="checkbox" id="pin4" name="pin4">
        </div>
        <div class="toggle">
            <label for="pin5">Pin 92:</label>
            <input type="checkbox" id="pin5" name="pin5">
        </div>
        <div class="toggle">
            <label for="pin6">Pin 93:</label>
            <input type="checkbox" id="pin6" name="pin6">
        </div>
        <button type="submit">Apply</button>
    </form>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/control', methods=['POST'])
def control():
    pin_states = {
        'pin1': request.form.get('pin1') == 'on',
        'pin2': request.form.get('pin2') == 'on',
        'pin3': request.form.get('pin3') == 'on',
        'pin4': request.form.get('pin4') == 'on',
        'pin5': request.form.get('pin5') == 'on',
        'pin6': request.form.get('pin6') == 'on'
    }
    send_command(pin_states)
    return render_template_string(html_template)

def send_command(pin_states):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 65432))
    client_socket.send(str(pin_states).encode())
    client_socket.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

