import gpiod
import socket
import ast

# Setup GPIO
chip = gpiod.Chip("0")
chip2 = gpiod.Chip("1")

line_1 = chip.get_line(5)
line_2 = chip.get_line(4)
line_3 = chip.get_line(9)

lineChip2_1 = chip2.get_line(91)
lineChip2_2 = chip2.get_line(92)
lineChip2_3 = chip2.get_line(93)

line_1.request(consumer='gpio_control', type=gpiod.LINE_REQ_DIR_OUT)
line_2.request(consumer='gpio_control', type=gpiod.LINE_REQ_DIR_OUT)
line_3.request(consumer='gpio_control', type=gpiod.LINE_REQ_DIR_OUT)

lineChip2_1.request(consumer='gpio_control', type=gpiod.LINE_REQ_DIR_OUT)
lineChip2_2.request(consumer='gpio_control', type=gpiod.LINE_REQ_DIR_OUT)
lineChip2_3.request(consumer='gpio_control', type=gpiod.LINE_REQ_DIR_OUT)

# Set default states: pins 5, 4, and 9 high; pins 91, 92, and 93 low
line_1.set_value(1)
line_2.set_value(1)
line_3.set_value(1)

lineChip2_1.set_value(0)
lineChip2_2.set_value(0)
lineChip2_3.set_value(0)

# Setup socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 65432))
server_socket.listen(1)

while True:
    conn, addr = server_socket.accept()
    data = conn.recv(1024).decode()
    pin_states = ast.literal_eval(data)
    
    # Set the states of pins 5, 4, and 9
    line_1.set_value(1 if pin_states['pin1'] else 0)
    line_2.set_value(1 if pin_states['pin2'] else 0)
    line_3.set_value(1 if pin_states['pin3'] else 0)
    
    # Set the states of pins 91, 92, and 93 based on binary values
    lineChip2_1.set_value(1 if pin_states['bin0'] else 0)     
    lineChip2_2.set_value(1 if pin_states['bin1'] else 0)
    lineChip2_3.set_value(1 if pin_states['bin2'] else 0)
    
    print("GPIO pins set according to received states.")
    conn.close()

