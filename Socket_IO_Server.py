import logging
import time
from flask import Flask, request, render_template
from flask_socketio import SocketIO, send, emit    

# Initialize Logging
logging.basicConfig(level=logging.WARNING)  # Global logging configuration
logger = logging.getLogger('main') 
logger.setLevel(logging.INFO) 

# Devices
relay1 = 0
relay2 = 0
dht11 = 0

# Flask 
app = Flask(__name__) 
socketio = SocketIO(app, cors_allowed_origins="*")

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
    emit("relay1", relay1)                                                            
    emit("relay2", relay2)

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
        relay1_state = int(data['state']) # data comes in as a str.
        if relay1_state == 0:
            relay1 = 0
        else:
            relay1 = 1
        logger.info("Relay 1 is " + str(relay1))

    # Broadcast new state to *every* connected connected (so they remain in sync).
    emit("relay1", str(relay1), broadcast=True)                                               

# LED2 Handler


@socketio.on('relay2')
def handle_state(data):                                                              
    logger.info("Update on Relay 2 from client {}: {} ".format(request.sid, data))

    if 'state' in data and data['state'].isdigit():                                  
        relay2_state = int(data['state']) # data comes as a str.
        if relay2_state == 0:
            relay2 = 0
        else:
            relay2 = 1
        logger.info("Relay 2 is " + str(relay2))

    # Broadcast new state to *every* connected connected (so they remain in sync).
    emit("relay2", str(relay2), broadcast=True)                                               


if __name__ == '__main__':

    socketio.run(app, host='0.0.0.0', debug=True)