from machine import Pin
import time
import urandom
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf, sys
import utime

pix_res_x = 128
pix_res_y = 64

def init_i2c(scl_pin, sda_pin):
    # Initialize I2C device
    i2c_dev = I2C(1, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=200000)
    i2c_addr = [hex(ii) for ii in i2c_dev.scan()]
    
    if not i2c_addr:
        print('No I2C Display Found')
        sys.exit()
    else:
        print("I2C Address      : {}".format(i2c_addr[0]))
        print("I2C Configuration: {}".format(i2c_dev))
    
    return i2c_dev

def display_logo(oled):
    # Display the Raspberry Pi logo on the OLED
    buffer = bytearray(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00|?\x00\x01\x86@\x80\x01\x01\x80\x80\x01\x11\x88\x80\x01\x05\xa0\x80\x00\x83\xc1\x00\x00C\xe3\x00\x00~\xfc\x00\x00L'\x00\x00\x9c\x11\x00\x00\xbf\xfd\x00\x00\xe1\x87\x00\x01\xc1\x83\x80\x02A\x82@\x02A\x82@\x02\xc1\xc2@\x02\xf6>\xc0\x01\xfc=\x80\x01\x18\x18\x80\x01\x88\x10\x80\x00\x8c!\x00\x00\x87\xf1\x00\x00\x7f\xf6\x00\x008\x1c\x00\x00\x0c \x00\x00\x03\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
    fb = framebuf.FrameBuffer(buffer, 32, 32, framebuf.MONO_HLSB)
    
    oled.fill(0)
    oled.blit(fb, 96, 0)
    oled.show()

def display_text(oled):
    oled.text("Raspberry Pi", 5, 5)
    oled.text("Pico", 5, 15)
    oled.show()

def display_anima(oled):
    
    start_time = utime.ticks_ms()
    
    led = Pin(15, Pin.OUT)
    button = Pin(16, Pin.IN)

    timer_start_tick = 0

    def button_pressed(pin):
        
        if led.value() == 1:
            timer_reaction = time.ticks_diff(time.ticks_ms(), timer_start_tick)
            led.value(0)
            print(f"Your reaction time was: {timer_reaction/1000} seconds")
            oled.fill_rect(5, 40, oled.width - 5, 8, 0)

            oled.text("Reaction: ", 5, 30)
            oled.text(str(timer_reaction/1000) + " sec", 5, 40)
            oled.show()
            utime.sleep_ms(1000)
            

    button.irq(trigger=Pin.IRQ_RISING, handler=button_pressed)

    while True:
        time.sleep(urandom.uniform(1, 5))
        timer_start_tick = time.ticks_ms()
        led.value(1)
        while led.value() == 1:
            time.sleep(0.1) 
        elapsed_time = (utime.ticks_diff(utime.ticks_ms(), start_time) // 1000) + 1

def main():
    i2c_dev = init_i2c(scl_pin=27, sda_pin=26)
    oled = SSD1306_I2C(pix_res_x, pix_res_y, i2c_dev)
    display_logo(oled)
    display_text(oled)
    display_anima(oled)
        

if __name__ == '__main__':
    main()
