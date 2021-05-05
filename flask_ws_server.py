"""
File: chapter03/flask_ws_server.py
A Flask based Web Sockets server to control an LED built using Flask-SocketIO.
Dependencies:
  pip3 install gpiozero pigpio flask-socketio
Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
import logging
from flask import Flask, request, render_template
from flask_socketio import SocketIO, send, emit                                      # (1)
# from gpiozero import PWMLED, Device
# from gpiozero.pins.pigpio import PiGPIOFactory


# Initialize Logging
logging.basicConfig(level=logging.WARNING)  # Global logging configuration
logger = logging.getLogger('main')  # Logger for this module
logger.setLevel(logging.INFO) # Debugging for this file.


# Initialize GPIO
# Device.pin_factory = PiGPIOFactory() #set gpiozero to use pigpio by default.


# Flask & Flask Restful Global Variables.
app = Flask(__name__) # Core Flask app.
socketio = SocketIO(app) # Flask-SocketIO extension wrapper.                         # (2)


# Global variables
LED_GPIO_PIN = 21
led1 = None # PWMLED Instance. See init_led()
led2 = None
state1 = {
    'level': 50 # 0..100 % brightless of LED.
}
state2 = {
    'level': 50 # 0..100 % brightless of LED.
}

"""
GPIO Related Functions
"""
def init_led1():
    """Create and initialise PWMLED Object"""
    global led1
    led1 = state1['level'] / 100
    # led =  PWMLED(LED_GPIO_PIN)
    # led.value = state['level'] / 100

def init_led2():
    """Create and initialise PWMLED Object"""
    global led2
    led2 = state2['level'] / 100
    # led =  PWMLED(LED_GPIO_PIN)
    # led.value = state['level'] / 100


"""
Flask & Flask-SocketIO Related Functions
"""

# @app.route apply to the raw Flask instance.
# Here we are serving a simple web page.
@app.route('/', methods=['GET'])
def index():
    """Make sure index_ws_client.html is in the templates folder
    relative to this Python file."""
    return render_template('index_ws_client.html', pin=LED_GPIO_PIN)                 # (3)


# Flask-SocketIO Callback Handlers
@socketio.on('connect')                                                              # (4)
def handle_connect():
    """Called when a remote web socket client connects to this server"""
    logger.info("Client {} connected.".format(request.sid))                          # (5)

    # Send initialising data to newly connected client.
    emit("led1", state1)                                                             # (6)
    emit("led2", state2)


@socketio.on('disconnect')                                                           # (7)
def handle_disconnect():
    """Called with a client disconnects from this server"""
    logger.info("Client {} disconnected.".format(request.sid))


@socketio.on('led1')                                                                  # (8)
def handle_state(data):                                                              # (9)
    """Handle 'led' messages to control the LED."""
    global state
    logger.info("Update LED1 from client {}: {} ".format(request.sid, data))

    if 'level' in data and data['level'].isdigit():                                  # (10)
        new_level = int(data['level']) # data comes in as str.

        # Range validation and bounding.
        if new_level < 0:                                                            # (11)
            new_level = 0
        elif new_level > 100:
            new_level = 100

        # Set PWM duty cycle to adjust brightness level.
        # We are mapping input value 0-100 to 0-1
        # led.value = new_level / 100                                                  # (12)
        logger.info("LED1 brightness level is " + str(new_level))

        state1['level'] = new_level

    # Broadcast new state to *every* connected connected (so they remain in sync).
    emit("led1", state1, broadcast=True)                                               # (13)


@socketio.on('led2')                                                                  # (8)
def handle_state(data):                                                              # (9)
    """Handle 'led' messages to control the LED."""
    global state
    logger.info("Update LED2 from client {}: {} ".format(request.sid, data))

    if 'level' in data and data['level'].isdigit():                                  # (10)
        new_level = int(data['level']) # data comes in as str.

        # Range validation and bounding.
        if new_level < 0:                                                            # (11)
            new_level = 0
        elif new_level > 100:
            new_level = 100

        # Set PWM duty cycle to adjust brightness level.
        # We are mapping input value 0-100 to 0-1
        # led.value = new_level / 100                                                  # (12)
        logger.info("LED2 brightness level is " + str(new_level))

        state2['level'] = new_level

    # Broadcast new state to *every* connected connected (so they remain in sync).
    emit("led2", state2, broadcast=True)                                               # (13)


# Initialise Module
init_led2()
init_led1()


if __name__ == '__main__':

    socketio.run(app, host='0.0.0.0', debug=True)