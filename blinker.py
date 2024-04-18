import time
from machine import Pin

led = Pin(15, Pin.OUT)

print("Hello, Pi Pico!")

while True:
  led.toggle()
  time.sleep(1) 