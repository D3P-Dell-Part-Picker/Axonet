import board
import neopixel
import busio
import digitalio
import time
from adafruit_wiznet5k.adafruit_wiznet5k import WIZNET5K
import adafruit_wiznet5k.adafruit_wiznet5k_socket as s

def led_separator(led, separator):
    sections = []
    for i in range(int(led / separator)):
        sections.insert(i, [])
        for e in range(separator):
            sections[i].insert(e, i * separator + e)
    return sections

num_pixels = 15
pixels_per_section = 3
separator = led_separator(num_pixels, pixels_per_section)
pixels = neopixel.NeoPixel(board.GP0, num_pixels)
pixels.brightness = 0.2
def light_pixel(msg):
    msg = msg.split("|")
    for half in msg:
        print(half)
        half = half.split('-')
        lights = separator[int(half[1])]
        half[0] = half[0].split('/')
        for light in lights:
            pixels[light] = (int(half[0][0]), int(half[0][1]), int(half[0][2]))

SPI1_SCK = board.GP10
SPI1_TX = board.GP11
SPI1_RX = board.GP12
SPI1_CSn = board.GP13
W5500_RSTn = board.GP15

MY_MAC = (0x0A, 0x0B, 0x03, 0x03, 0x01, 0x07)
IP_ADDRESS = (10, 12, 32, 107)
SUBNET_MASK = (255, 255, 254, 0)
GATEWAY_ADDRESS = (10, 12, 32, 1)
DNS_SERVER = (10, 254, 174, 10)
port = 3706

led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT
ethernetRst = digitalio.DigitalInOut(W5500_RSTn)
ethernetRst.direction = digitalio.Direction.OUTPUT


cs = digitalio.DigitalInOut(SPI1_CSn)

spi_bus = busio.SPI(SPI1_SCK, MOSI=SPI1_TX, MISO=SPI1_RX)

ethernetRst.value = False
time.sleep(1)
ethernetRst.value = True

eth = WIZNET5K(spi_bus, cs, is_dhcp=False, mac=MY_MAC)

eth.ifconfig = (IP_ADDRESS, SUBNET_MASK, GATEWAY_ADDRESS, DNS_SERVER)
s.set_interface(eth)
sock = s.socket()
sock.bind(('10.12.32.107',port))
time.sleep(1)
sock.listen()
while True:
    conn, addr = sock.accept()
    with conn:
        conn.settimeout(2)
        #print(conn)
        led.value = True
        conn.send(b'Connected')
        data = conn.recv(conn.available()).decode('utf-8')
        #print(data)
        conn.close()
        light_pixel(data)
        led.value = False

