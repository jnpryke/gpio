from flask import Flask, render_template_string, request, jsonify
import socket
import json

app = Flask(__name__)

html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>GPIO Pin Control</title>
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
        table {
            margin: 0 auto;
            border-collapse: collapse;
        }
        th, td {
            padding: 10px;
            border: 1px solid #ddd;
        }
        select {
            font-size: 16px;
            padding: 5px;
        }
        input[type="submit"], button {
            font-size: 20px;
            padding: 10px 20px;
            margin: 5px;
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
        }
        button {
            margin-left: 10px;
        }
    </style>
    <script>
        function sendPinStates() {
            var form = document.getElementById('pinForm');
            var formData = new FormData(form);
            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/send_pins', true);
            xhr.onload = function () {
                if (xhr.status === 200) {
                    console.log('Pin states set successfully!');
                } else {
                    console.log('An error occurred while setting pin states.');
                }
            };
            xhr.send(formData);
            return false;
        }
    </script>
</head>
<body>
    <h1>GPIO Pin Control</h1>
    <form id="pinForm" onsubmit="return sendPinStates();">
        <table>
            <tr>
                <th>Pin</th>
                <th>State</th>
            </tr>
            {% for pin in pins %}
            <tr>
                <td>{{ pin }}</td>
                <td>
                    <select name="pin_{{ pin }}">
                        <option value="high" {% if pin not in [91, 92, 93] %}selected{% endif %}>High</option>
                        <option value="low" {% if pin in [91, 92, 93] %}selected{% endif %}>Low</option>
                    </select>
                </td>
            </tr>
            {% endfor %}
        </table>
        <input type="submit" value="Set Pin States">
    </form>
</body>
</html>
"""

@app.route('/')
def index():
    pins = [5, 4, 9, 91, 92, 93, 87, 88]  # Including pins 87 and 88
    return render_template_string(html_template, pins=pins)

@app.route('/send_pins', methods=['POST'])
def send_pins():
    pin_states = {}
    for pin in request.form:
        pin_number = int(pin.split('_')[1])
        state = request.form[pin]
        pin_states[pin_number] = state
    send_pin_states_to_gpio(pin_states)
    return jsonify({"status": "success"})

def send_pin_states_to_gpio(pin_states):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", 65432))
        s.sendall(json.dumps(pin_states).encode())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
