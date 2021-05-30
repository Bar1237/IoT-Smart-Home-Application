import socketio
import logging
import gpiozero
from gpiozero import Device
from gpiozero.pins.pigpio import PiGPIOFactory
import dht11
import RPi.GPIO as GPIO

# standard Python
sio = socketio.Client()

# Initialize Logging
logging.basicConfig(level=logging.WARNING)  # Global logging configuration
logger = logging.getLogger('main')
logger.setLevel(logging.INFO)
sio.connect('http://192.168.31.235:5000')

# Initialize Relays and Sensor
relay1 = gpiozero.OutputDevice(20, active_high=True, initial_value=False)
relay2 = gpiozero.OutputDevice(21, active_high=True, initial_value=False)
dht_sensor = dht11.DHT11(pin=26)

while 1:
    @sio.on('relay1')
    def handle_state(data):
        logger.info("Update to Relay 1 from client {}: {} ".format(sio.sid, data))

        if 'state' in data and data['state'].isdigit():
            relay1_state = int(data['state'])  # data comes in as a str.
            if relay1_state == 0:
                relay1.off()
            else:
                relay1.on()
            logger.info("Relay 1 is " + str(relay1.value))

        # Broadcast new state to *every* connected connected (so they remain in sync).
        sio.emit("relay1", relay1.value)


    @sio.on('relay2')
    def handle_state(data):
        logger.info("Update on Relay 2 from client {}: {} ".format(sio.sid, data))

        if 'state' in data and data['state'].isdigit():
            relay2_state = int(data['state'])  # data comes as a str.
            if relay2_state == 0:
                relay2.off()
            else:
                relay2.on()
            logger.info("Relay 2 is " + str(relay2.value))

        # Broadcast new state to *every* connected connected (so they remain in sync).
        sio.emit("relay2", relay2.value)