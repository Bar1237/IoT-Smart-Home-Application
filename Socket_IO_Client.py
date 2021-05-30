import socketio
from timeit import default_timer as timer
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

start = timer()
while 1:
    @sio.on('relay1')
    def handle_state(data):
        print("Update to Relay 1 from client {}: {} ".format(sio.sid, data))

        relay1_state = int(data['state'])  # data comes in as a str.
        if relay1_state == 0:
            relay1.off()
        else:
            relay1.on()
        logger.info("Relay 1 is " + str(relay1.value))


    @sio.on('relay2')
    def handle_state(data):
        print("Update on Relay 2 from client {}: {} ".format(sio.sid, data))

        relay2_state = int(data['state'])  # data comes as a str.
        if relay2_state == 0:
            relay2.off()
        else:
            relay2.on()
        logger.info("Relay 2 is " + str(relay2.value))

    end = timer()
    if int(end - start) != 0 and int(end - start) % 2 == 0:
        start = end
        result = dht_sensor.read()
        sio.emit('dht', {"state": result.temperature})