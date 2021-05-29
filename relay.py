import gpiozero
import time

RELAY_PIN = 20

# Triggered by the output pin going high: active_high=True
# Initially off: initial_value=False

relay = gpiozero.OutputDevice(RELAY_PIN, active_high=True, initial_value=False)

relay.off() # switch off

time.sleep(10)

relay.on() # switch on

print(relay.value) # see if on or off