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
        .toggle-btn {
            width: 60px;
            padding: 10px;
            color: white;
            cursor: pointer;
            text-align: center;
            border: none;
            border-radius: 4px;
        }
        .high {
            background-color: red;
        }
        .low {
            background-color: grey;
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
        function togglePinState(button, pin) {
            if (button.classList.contains('high')) {
                button.classList.remove('high');
                button.classList.add('low');
                button.innerText = 'Low';
                document.getElementById('pin_' + pin).value = 'low';
            } else {
                button.classList.remove('low');
                button.classList.add('high');
                button.innerText = 'High';
                document.getElementById('pin_' + pin).value = 'high';
            }
        }

        function setDefault() {
            document.querySelectorAll('.toggle-btn').forEach(button => {
                const pin = button.getAttribute('data-pin');
                if ([91, 92, 93].includes(parseInt(pin))) {
                    button.classList.remove('high');
                    button.classList.add('low');
                    button.innerText = 'Low';
                    document.getElementById('pin_' + pin).value = 'low';
                } else {
                    button.classList.remove('low');
                    button.classList.add('high');
                    button.innerText = 'High';
                    document.getElementById('pin_' + pin).value = 'high';
                }
            });

            // Submit the form after setting default states
            document.getElementById('pinForm').submit();
        }

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
            <!-- Separate section for pins 91, 92, 93 -->
            <tr><th colspan="2">Input Pins</th></tr>
            {% for pin in pins if pin in [91, 92, 93] %}
            <tr>
                <td>{{ pin }}</td>
                <td>
                    <button type="button" class="toggle-btn {% if pin in [91, 92, 93] %}low{% else %}high{% endif %}" data-pin="{{ pin }}" onclick="togglePinState(this, {{ pin }})">
                        {% if pin in [91, 92, 93] %}Low{% else %}High{% endif %}
                    </button>
                    <input type="hidden" id="pin_{{ pin }}" name="pin_{{ pin }}" value="{% if pin in [91, 92, 93] %}low{% else %}high{% endif %}">
                </td>
            </tr>
            {% endfor %}
            <!-- Separate section for the rest of the pins -->
            <tr><th colspan="2">Enable Pins</th></tr>
            {% for pin in pins if pin not in [91, 92, 93] %}
            <tr>
                <td>{{ pin }}</td>
                <td>
                    <button type="button" class="toggle-btn {% if pin in [91, 92, 93] %}low{% else %}high{% endif %}" data-pin="{{ pin }}" onclick="togglePinState(this, {{ pin }})">
                        {% if pin in [91, 92, 93] %}Low{% else %}High{% endif %}
                    </button>
                    <input type="hidden" id="pin_{{ pin }}" name="pin_{{ pin }}" value="{% if pin in [91, 92, 93] %}low{% else %}high{% endif %}">
                </td>
            </tr>
            {% endfor %}
        </table>
        <input type="submit" value="Set Pin States">
        <button type="button" onclick="setDefault()">Set Default</button>
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
