import rp2
from rp2 import PIO
from machine import Pin
from time import sleep
import urandom

@rp2.asm_pio(out_init=[PIO.OUT_LOW]*8, sideset_init=[PIO.OUT_LOW]*4)
def sevseg():
    wrap_target()
    label("0")
    pull(noblock)           .side(0)      # 0
    mov(x, osr)             .side(0)      # 1
    out(pins, 8)            .side(1)      # 2
    out(pins, 8)            .side(2)      # 3
    out(pins, 8)            .side(4)      # 4
    out(pins, 8)            .side(8)      # 5
    jmp("0")                .side(0)      # 6
    wrap()
  
sm = rp2.StateMachine(0, sevseg, freq=2000, out_base=Pin(2), sideset_base=Pin(10))
sm.active(1)

digits = [
  0b11000000, # 0
  0b11111001, # 1
  0b10100100, # 2 
  0b10110000, # 3
  0b10011001, # 4
  0b10010010, # 5
  0b10000010, # 6
  0b11111000, # 7
  0b10000000, # 8
  0b10011000, # 9
]

def segmentize(num):
  return (
    digits[num % 10] | digits[num // 10 % 10] << 8
    | digits[num // 100 % 10] << 16 
    | digits[num // 1000 % 10] << 24 
  )

counter = 10
while counter >= 0:
  sm.put(segmentize(counter));
  counter -= 1
  sleep(1)

print('Lift Off')
