import gpiod
import socket
import ast
import time

def setup_gpio():
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

    return line_1, line_2, line_3, lineChip2_1, lineChip2_2, lineChip2_3

def set_default_state(lines):
    line_1, line_2, line_3, lineChip2_1, lineChip2_2, lineChip2_3 = lines
    try:
        line_1.set_value(1)
        line_2.set_value(1)
        line_3.set_value(1)
        lineChip2_1.set_value(0)
        lineChip2_2.set_value(0)
        lineChip2_3.set_value(0)
        print("Restored default state: all enable pins high (false), input pins low (true)")
    except Exception as e:
        print(f"Error setting default state: {e}")

def set_gpio_state(pin_states, lines):
    line_1, line_2, line_3, lineChip2_1, lineChip2_2, lineChip2_3 = lines
    try:
        # Set the states of pins 5, 4, and 9
        line_1.set_value(0 if pin_states.get('pin1', False) else 1)
        line_2.set_value(0 if pin_states.get('pin2', False) else 1)
        line_3.set_value(0 if pin_states.get('pin3', False) else 1)
        print(f"Set enable pins: pin5={'LOW' if pin_states.get('pin1', False) else 'HIGH'}, pin4={'LOW' if pin_states.get('pin2', False) else 'HIGH'}, pin9={'LOW' if pin_states.get('pin3', False) else 'HIGH'}")
        
        # Set the states of pins 91, 92, and 93 based on binary values
        lineChip2_1.set_value(1 if pin_states.get('bin0', False) else 0)
        lineChip2_2.set_value(1 if pin_states.get('bin1', False) else 0)
        lineChip2_3.set_value(1 if pin_states.get('bin2', False) else 0)
        print(f"Set input pins: pin91={'HIGH' if pin_states.get('bin0', False) else 'LOW'}, pin92={'HIGH' if pin_states.get('bin1', False) else 'LOW'}, pin93={'HIGH' if pin_states.get('bin2', False) else 'LOW'}")
    except Exception as e:
        print(f"Error setting GPIO state: {e}")

def main():
    lines = setup_gpio()
    set_default_state(lines)

    # Setup socket server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 65432))
    server_socket.listen(1)
    print("Server started, waiting for connections...")

    while True:
        try:
            conn, addr = server_socket.accept()
            print(f"Accepted connection from {addr}")
            data = conn.recv(1024).decode()
            print(f"Received data: {data}")
            pin_states = ast.literal_eval(data)
            print(f"Parsed pin states: {pin_states}")
            
            set_gpio_state(pin_states, lines)
            conn.close()
            
            # Wait half a second before restoring default state
            time.sleep(0.5)
            set_default_state(lines)
            time.sleep(0.5)
        except Exception as e:
            print(f"Error handling connection: {e}")

if __name__ == "__main__":
    main()
