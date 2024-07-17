import gpiod
import socket
import time
import json

def setup_gpio():
    chip = gpiod.Chip("0")
    chip2 = gpiod.Chip("1")

    # Define all pins
    pins = {
        5: chip.get_line(5),
        4: chip.get_line(4),
        9: chip.get_line(9),
        91: chip2.get_line(91),
        92: chip2.get_line(92),
        93: chip2.get_line(93),
        87: chip.get_line(87),
        88: chip.get_line(88)
    }

    for pin in pins.values():
        pin.request(consumer='gpio_control', type=gpiod.LINE_REQ_DIR_OUT)

    return pins

def set_pin_states(pins, pin_states):
    for pin, state in pin_states.items():
        if state == "high":
            pins[int(pin)].set_value(1)
        else:
            pins[int(pin)].set_value(0)

if __name__ == "__main__":
    pins = setup_gpio()

    # Create a socket to listen for inputs
    server_address = ("localhost", 65432)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(server_address)
        s.listen()

        while True:
            print("Waiting for a connection...")
            connection, client_address = s.accept()
            try:
                print(f"Connection from {client_address}")
                while True:
                    data = connection.recv(1024)
                    if data:
                        pin_states = json.loads(data.decode())
                        print(f"Received pin states: {pin_states}")  # Debug statement
                        set_pin_states(pins, pin_states)
                    else:
                        break
            finally:
                connection.close()
