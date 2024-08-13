from flask import Flask, render_template, jsonify
import threading
import time, sys
import socket

app = Flask(__name__)

# Shared variable for counting
counter = 0
hostname = "not_assigned_yet"
IPAddr = "not_assigned_yet"
counter_lock = threading.Lock()


def infinite_counter():
    global counter
    while True:
        time.sleep(1)  # Sleep for 1 second
        print('\b'+str(counter), end="", flush=True)  # type: ignore
        # print(counter)
        with counter_lock:
            counter += 1

@app.route('/')
def get_counter():
    with counter_lock:
        return jsonify(
            {
                'counter': counter,
                'Your Computer Name is ' : hostname,
                "Your Computer IP Address is": IPAddr
            }
        )

if __name__ == '__main__':
    # Start the infinite counter in a separate thread
    counter_thread = threading.Thread(target=infinite_counter, daemon=True)
    counter_thread.start()

    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)

    print("Your Computer Name is:" + hostname)
    print()
    
    # Run the Flask app
    app.run(host='0.0.0.0')

