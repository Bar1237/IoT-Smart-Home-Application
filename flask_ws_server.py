"""
Template that is used as a base to this code is taken from:
https://github.com/PacktPublishing/Practical-Python-Programming-for-IoT/tree/master/chapter03
"""
import logging
from flask import Flask, request, render_template
from flask_socketio import SocketIO, send, emit                                     
from gpiozero import LED, Device
from gpiozero.pins.pigpio import PiGPIOFactory


# Initialize Logging
logging.basicConfig(level=logging.WARNING)  # Global logging configuration
logger = logging.getLogger('main')  # Logger for this module
logger.setLevel(logging.INFO) # Debugging for this file.


# Initialize GPIO
Device.pin_factory = PiGPIOFactory() #set gpiozero to use pigpio by default.


# Flask & Flask Restful Global Variables.
app = Flask(__name__) # Core Flask app.
socketio = SocketIO(app) # Flask-SocketIO extension wrapper.                         


# Global variables
LED_GPIO_PIN = 21
led1 = None
led2 = None
state1 = {
    'level': 50 
}
state2 = {
    'level': 50 
}


"""
GPIO Related Functions
"""
def init_led1():
    """Create and initialise PWMLED Object"""
    global led1
    led1 = state1['level'] / 100
    led1 =  LED(20)
    led1.value = state1['level'] / 100

def init_led2():
    """Create and initialise PWMLED Object"""
    global led2
    led2 = state2['level'] / 100
    led2 =  LED(21)
    led2.value = state2['level'] / 100


"""
Flask & Flask-SocketIO Related Functions
"""
# @app.route apply to the raw Flask instance.
# Here we are serving a simple web page.
@app.route('/', methods=['GET'])
def index():
    """index_ws_client.html file needs to be in the templates folder
    relative to this Python file."""
    return render_template('index_ws_client.html', pin=LED_GPIO_PIN)                 

# Flask-SocketIO Callback Handlers
@socketio.on('connect')                                                              
def handle_connect():
    """Called when a remote web socket client connects to this server"""
    logger.info("Client {} connected.".format(request.sid))                          

    # Send initialising data to newly connected client.
    emit("led1", state1)                                                             
    emit("led2", state2)

@socketio.on('disconnect')                                                           
def handle_disconnect():
    """Called with a client disconnects from this server"""
    logger.info("Client {} disconnected.".format(request.sid))

@socketio.on('led1')                                                                  
def handle_state(data):                                                              
    """Handle 'led' messages to control the LED."""
    global state
    logger.info("Update LED1 from client {}: {} ".format(request.sid, data))

    if 'level' in data and data['level'].isdigit():                                  
        new_level = int(data['level']) # data comes in as str.
        if new_level == 0:
            led1.off()
        else:
            led1.on()

        logger.info("LED1 brightness level is " + str(new_level))

        state1['level'] = new_level

    # Broadcast new state to *every* connected connected (so they remain in sync).
    emit("led1", state1, broadcast=True)                                               

@socketio.on('led2')                                                                  
def handle_state(data):                                                              
    """Handle 'led' messages to control the LED."""
    global state
    logger.info("Update LED2 from client {}: {} ".format(request.sid, data))

    if 'level' in data and data['level'].isdigit():                                  
        new_level = int(data['level']) # data comes in as str.
        if new_level == 0:
            led2.off()
        else:
            led2.on()

        logger.info("LED2 brightness level is " + str(new_level))

        state2['level'] = new_level

    # Broadcast new state to *every* connected connected (so they remain in sync).
    emit("led2", state2, broadcast=True)                                               


# Initialise Module
init_led2()
init_led1()


if __name__ == '__main__':

    socketio.run(app, host='0.0.0.0', debug=True)