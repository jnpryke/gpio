import gpiod
import socket
import ast
import time

# Setup GPIO
chip = gpiod.Chip("0")
chip2 = gpiod.Chip("1")

line_5 = chip.get_line(5)
line_4 = chip.get_line(4)
line_9 = chip.get_line(9)

line_91 = chip2.get_line(91)
line_92 = chip2.get_line(92)
line_93 = chip2.get_line(93)

line_5.request(consumer='gpio_control', type=gpiod.LINE_REQ_DIR_OUT)
line_4.request(consumer='gpio_control', type=gpiod.LINE_REQ_DIR_OUT)
line_9.request(consumer='gpio_control', type=gpiod.LINE_REQ_DIR_OUT)

line_91.request(consumer='gpio_control', type=gpiod.LINE_REQ_DIR_OUT)
line_92.request(consumer='gpio_control', type=gpiod.LINE_REQ_DIR_OUT)
line_93.request(consumer='gpio_control', type=gpiod.LINE_REQ_DIR_OUT)

# Set default states: all enable pins high
line_5.set_value(1)
line_4.set_value(1)
line_9.set_value(1)
line_91.set_value(0)
line_92.set_value(0)
line_93.set_value(0)

print("Default state set: all enable pins high")

# Setup socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 65432))
server_socket.listen(1)

while True:
    conn, addr = server_socket.accept()
    data = conn.recv(1024).decode()
    command = ast.literal_eval(data)
    
    enable_pins = command["enable_pins"]
    input_pins = command["input_pins"]
    
    # Log conditions for enabling pins
    print(f"Condition to enable pin 5: {enable_pins['pin5']}")
    print(f"Condition to enable pin 4: {enable_pins['pin4']}")
    
    # Set enable pins
    line_5.set_value(1 if enable_pins["pin5"] else 0)
    line_4.set_value(1 if enable_pins["pin4"] else 0)
    print(f"Set enable pins: pin5={'HIGH' if enable_pins['pin5'] else 'LOW'}, pin4={'HIGH' if enable_pins['pin4'] else 'LOW'}")
    
    # Set input pins
    line_91.set_value(1 if input_pins[0] == '1' else 0)
    line_92.set_value(1 if input_pins[1] == '1' else 0)
    line_93.set_value(1 if input_pins[2] == '1' else 0)
    print(f"Set input pins: pin91={'HIGH' if input_pins[0] == '1' else 'LOW'}, pin92={'HIGH' if input_pins[1] == '1' else 'LOW'}, pin93={'HIGH' if input_pins[2] == '1' else 'LOW'}")
    
    conn.close()
    
    # Restore default states after each input
    line_5.set_value(1)
    line_4.set_value(1)
    line_9.set_value(1)
    line_91.set_value(0)
    line_92.set_value(0)
    line_93.set_value(0)
    print("Restored default state: all enable pins high")
    time.sleep(1)

