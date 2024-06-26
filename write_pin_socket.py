import gpiod
import socket

# Setup GPIO
# chip = gpiod.Chip('gpiochip1')  # Adjust as needed
chip = gpiod.Chip("0")  # Make sure the chip name is correct
chip2 = gpiod.Chip("1")  # Make sure the chip name is correct

line_1 = chip.get_line(5)  # Replace 16 with your actual GPIO pin number
line_2 = chip.get_line(4)  # Replace 16 with your actual GPIO pin number
line_3 = chip.get_line(9)  # Replace 16 with your actual GPIO pin number

lineChip2_1 = chip2.get_line(91)  # Chip 2 line
lineChip2_2 = chip2.get_line(92)  # Replace 16 with your actual GPIO pin number
lineChip2_3 = chip2.get_line(93)  # Replace 16 with your actual GPIO pin numbe

line_1.request(consumer='gpio_control', type=gpiod.LINE_REQ_DIR_OUT)
line_2.request(consumer='gpio_control', type=gpiod.LINE_REQ_DIR_OUT)
line_3.request(consumer='gpio_control', type=gpiod.LINE_REQ_DIR_OUT)

lineChip2_1.request(consumer='gpio_control', type=gpiod.LINE_REQ_DIR_OUT)
lineChip2_2.request(consumer='gpio_control', type=gpiod.LINE_REQ_DIR_OUT)
lineChip2_3.request(consumer='gpio_control', type=gpiod.LINE_REQ_DIR_OUT)

# Setup socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 65432))
server_socket.listen(1)

while True:
    conn, addr = server_socket.accept()
    data = conn.recv(1024).decode()
    if data == 'on':
        line_1.set_value(1)
        line_2.set_value(1)
        line_3.set_value(1)
        
        lineChip2_1.set_value(1)
        lineChip2_2.set_value(1)
        lineChip2_3.set_value(1)
        print("GPIO pin 5,4,8 set to high.")
    elif data == 'off':
        line_1.set_value(0)
        line_2.set_value(0)
        line_3.set_value(0)
        
        lineChip2_1.set_value(0)
        lineChip2_2.set_value(0)
        lineChip2_3.set_value(0)        
        print("GPIO pin 5,4,8 set to low.")
    conn.close()

