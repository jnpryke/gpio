from flask import Flask, render_template_string, request
import socket
import time

app = Flask(__name__)

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
            text-align: center;
            margin-top: 50px;
        }
        input[type="text"] {
            padding: 10px;
            font-size: 16px;
            margin-bottom: 20px;
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
    <h1>GPIO Character Sequence Control</h1>
    <form method="POST" action="/control">
        <input type="text" name="sequence" placeholder="Enter number sequence" required>
        <br>
        <button type="submit">Submit</button>
    </form>
</body>
</html>
"""

# Mappings for each pin
pin_5_map = {
    "0": "1",
    "1": "2",
    "2": "10",
    "3": "11",
    "4": "100",
    "5": "101",
    "6": "110",
    "7": "111",
    "8": "END"
}

pin_4_map = {
    "0": "NEXT",
    "1": "SLEEP",
    "2": "POWER",
    "3": "BLUETOOTH",
    "4": "F10",
    "5": "0",
    "6": "PRINT SCREEN",
    "7": "F5"
}

pin_9_map = {
    "0": "WINDOWS KEY",
    "1": "HANGUL",
    "2": "",
    "3": "",
    "4": "",
    "5": "",
    "6": "",
    "7": ""
}

def send_command(pin_states):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 65432))
    client_socket.send(str(pin_states).encode())
    client_socket.close()
    print(f"Sent command: {pin_states}")

def process_sequence(sequence):
    print(f"Processing sequence: {sequence}")
    for char in sequence:
        print(f"Processing character: {char}")
        if char in pin_5_map:
            binary_input = format(int(char), '03b')
            pin_states = {
                'pin1': True, 'pin2': False, 'pin3': False,
                'bin0': binary_input[2] == '1',
                'bin1': binary_input[1] == '1',
                'bin2': binary_input[0] == '1'
            }
            send_command(pin_states)
            time.sleep(0.5)
        elif char in pin_4_map:
            binary_input = format(int(char), '03b')
            pin_states = {
                'pin1': False, 'pin2': True, 'pin3': False,
                'bin0': binary_input[2] == '1',
                'bin1': binary_input[1] == '1',
                'bin2': binary_input[0] == '1'
            }
            send_command(pin_states)
            time.sleep(0.5)
        elif char in pin_9_map:
            binary_input = format(int(char), '03b')
            pin_states = {
                'pin1': False, 'pin2': False, 'pin3': True,
                'bin0': binary_input[2] == '1',
                'bin1': binary_input[1] == '1',
                'bin2': binary_input[0] == '1'
            }
            send_command(pin_states)
            time.sleep(0.5)

@app.route('/')
def index():
    print("Rendering index page")
    return render_template_string(html_template)

@app.route('/control', methods=['POST'])
def control():
    sequence = request.form['sequence']
    print(f"Received sequence: {sequence}")
    process_sequence(sequence)
    return render_template_string(html_template)

if __name__ == '__main__':
    print("Starting GPIO Control Server")
    app.run(host='0.0.0.0', port=5000)
