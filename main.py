import threading
from flask import Flask
# (Import your gpio_server and Flask logic)

def run_flask():
    from toggle_html.py import app  # Assuming you saved your Flask app in flask_app.py
    app.run(host='0.0.0.0', port=5000)

def run_gpio_server():
    from toggle_pins.py import main  # Assuming you saved the GPIO server in gpio_server.py
    main()

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    gpio_thread = threading.Thread(target=run_gpio_server)

    flask_thread.start()
    gpio_thread.start()

    flask_thread.join()
    gpio_thread.join()
