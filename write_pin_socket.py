import gpiod
import socket

# Setup GPIO
# chip = gpiod.Chip('gpiochip1')  # Adjust as needed
chip = gpiod.Chip("0")  # Make sure the chip name is correct

line = chip.get_line(5)  # Replace 16 with your actual GPIO pin number
line2 = chip.get_line(4)  # Replace 16 with your actual GPIO pin number
line3 = chip.get_line(9)  # Replace 16 with your actual GPIO pin number

line.request(consumer='gpio_control', type=gpiod.LINE_REQ_DIR_OUT)
line2.request(consumer='gpio_control', type=gpiod.LINE_REQ_DIR_OUT)
line3.request(consumer='gpio_control', type=gpiod.LINE_REQ_DIR_OUT)

# Setup socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 65432))
server_socket.listen(1)

while True:
    conn, addr = server_socket.accept()
    data = conn.recv(1024).decode()
    if data == 'on':
        line.set_value(1)
        line2.set_value(1)
        line3.set_value(1)
        print("GPIO pin 5,4,8 set to high.")
    elif data == 'off':
        line.set_value(0)
        line2.set_value(0)
        line3.set_value(0)
        print("GPIO pin 5,4,8 set to low.")
    conn.close()

