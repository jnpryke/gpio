from flask import Flask, render_template_string, request
import socket

app = Flask(__name__)

# HTML template with updated functionality and better presentation
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
        .section {
            margin: 20px 0;
            padding: 20px;
            border: 1px solid #ffffff;
            border-radius: 10px;
        }
        .section-title {
            text-align: center;
            font-size: 24px;
            margin-bottom: 10px;
        }
        .toggle {
            display: flex;
            align-items: center;
            gap: 10px;
            justify-content: center;
            margin: 10px 0;
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
        .binary-display {
            text-align: center;
            font-size: 20px;
            margin: 10px 0;
        }
    </style>
    <script>
        function togglePin(id) {
            const pins = ['pin1', 'pin2', 'pin3'];
            const uncheckedPins = pins.filter(pin => !document.getElementById(pin).checked);
            if (uncheckedPins.length > 1) {
                document.getElementById(id).checked = true;
            }
        }

        function updateBinaryDisplay() {
            const bin0 = document.getElementById('bin0').checked ? 1 : 0;
            const bin1 = document.getElementById('bin1').checked ? 1 : 0;
            const bin2 = document.getElementById('bin2').checked ? 1 : 0;
            const binaryValue = (bin2 << 2) | (bin1 << 1) | bin0;
            document.getElementById('binaryValue').textContent = `Binary Value: ${binaryValue} ( ${bin2}${bin1}${bin0} )`;
        }

        function setDefault() {
            document.getElementById('pin1').checked = true;
            document.getElementById('pin2').checked = true;
            document.getElementById('pin3').checked = true;
            document.getElementById('bin0').checked = false;
            document.getElementById('bin1').checked = false;
            document.getElementById('bin2').checked = false;
            updateBinaryDisplay();
        }
    </script>
</head>
<body onload="setDefault()">
    <h1>GPIO Control</h1>
    <form method="POST" action="/control">
        <div class="section">
            <div class="section-title">Enabled Pins</div>
            <div class="toggle">
                <label for="pin1">Pin 5:</label>
                <input type="checkbox" id="pin1" name="pin1" onchange="togglePin('pin1')" checked>
            </div>
            <div class="toggle">
                <label for="pin2">Pin 4:</label>
                <input type="checkbox" id="pin2" name="pin2" onchange="togglePin('pin2')" checked>
            </div>
            <div class="toggle">
                <label for="pin3">Pin 9:</label>
                <input type="checkbox" id="pin3" name="pin3" onchange="togglePin('pin3')" checked>
            </div>
        </div>
        <div class="section">
            <div class="section-title">Input Selector Pins</div>
            <div class="toggle">
                <label for="bin0">Pin 91 (Lowest Bit):</label>
                <input type="checkbox" id="bin0" name="bin0" onchange="updateBinaryDisplay()">
            </div>
            <div class="toggle">
                <label for="bin1">Pin 92 (Middle Bit):</label>
                <input type="checkbox" id="bin1" name="bin1" onchange="updateBinaryDisplay()">
            </div>
            <div class="toggle">
                <label for="bin2">Pin 93 (Highest Bit):</label>
                <input type="checkbox" id="bin2" name="bin2" onchange="updateBinaryDisplay()">
            </div>
            <div class="binary-display" id="binaryValue">Binary Value: 0 ( 000 )</div>
        </div>
        <button type="submit">Apply</button>
        <button type="button" onclick="setDefault()">Default</button>
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
        'bin0': request.form.get('bin0') == 'on',
        'bin1': request.form.get('bin1') == 'on',
        'bin2': request.form.get('bin2') == 'on'
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

