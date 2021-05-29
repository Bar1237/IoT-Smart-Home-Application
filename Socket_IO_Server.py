
import logging
from flask import Flask, request, render_template
from flask_socketio import SocketIO, send, emit    
import gpiozero                                 
from gpiozero import  Device
from gpiozero.pins.pigpio import PiGPIOFactory


# Initialize Logging
logging.basicConfig(level=logging.WARNING)  # Global logging configuration
logger = logging.getLogger('main') 
logger.setLevel(logging.INFO) 


# Initialize GPIO
Device.pin_factory = PiGPIOFactory() #set gpiozero to use pigpio by default.

# Initilize Relays
relay1 = gpiozero.OutputDevice(20, active_high=True, initial_value=False)
relay2 = gpiozero.OutputDevice(21, active_high=True, initial_value=False)

# Flask 
app = Flask(__name__) 
socketio = SocketIO(app)                         

"""
Flask & Flask-SocketIO Related Functions
"""
# @app.route apply to the raw Flask instance.
# Here we are serving a simple web page.
@app.route('/', methods=['GET'])
def index():
    return render_template('index_ws_client.html')                 

# Flask-SocketIO Callback Handlers
@socketio.on('connect')                                                              
def handle_connect():
    """Called when a remote web socket client connects to this server"""
    logger.info("Client {} connected.".format(request.sid)) 
    logger.info(relay1.value)                         
    logger.info(relay2.value) 
    emit("relay1", value_to_int(relay1.value))                                                             
    emit("relay2", value_to_int(relay2.value))

# Send Feedback when a client disconnects
@socketio.on('disconnect')                                                           
def handle_disconnect():
    """Called with a client disconnects from this server"""
    logger.info("Client {} disconnected.".format(request.sid))

# LED1 Handler
@socketio.on('relay1')                                                                  
def handle_state(data):                                                              
    logger.info("Update to Relay 1 from client {}: {} ".format(request.sid, data))

    if 'state' in data and data['state'].isdigit():                                  
        new_state = int(data['state']) # data comes in as a str.
        if new_state == 0:
            relay1.off()
        else:
            relay1.on()

        logger.info("Relay 1 is " + relay1.value )

        relay1_state = new_state

    # Broadcast new state to *every* connected connected (so they remain in sync).
    emit("relay1", relay1_state, broadcast=True)                                               

# LED2 Handler
@socketio.on('relay2')                                                                  
def handle_state(data):                                                              
    logger.info("Update on Relay 2 from client {}: {} ".format(request.sid, data))

    if 'relay_state' in data and data['relay_state'].isdigit():                                  
        new_state = int(data['state']) # data comes as a str.
        if new_state == 0:
            relay2.off()
        else:
            relay2.on()

        logger.info("Relay 2 is " + relay2.value )

        relay2_state = new_state

    # Broadcast new state to *every* connected connected (so they remain in sync).
    emit("relay2", relay2_state, broadcast=True)                                               

def value_to_int(self, value):
    if value:
        return 1
    else:
        return 0


if __name__ == '__main__':

    socketio.run(app, host='0.0.0.0', debug=False)