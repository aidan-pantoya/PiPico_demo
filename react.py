from machine import Pin
import time
import urandom

led = Pin(15, Pin.OUT)
button = Pin(16, Pin.IN)

timer_start_tick = 0

def button_pressed(pin):
    global timer_start_tick
    if led.value() == 1:
        timer_reaction = time.ticks_diff(time.ticks_ms(), timer_start_tick)
        print(f"Your reaction time was: {timer_reaction/1000} seconds")
        led.value(0)

button.irq(trigger=Pin.IRQ_RISING, handler=button_pressed)

while True:
    time.sleep(urandom.uniform(1, 5))
    timer_start_tick = time.ticks_ms()
    led.value(1)
    while led.value() == 1:
        time.sleep(0.1) 
