import os
import sys
import time
import primitives
import client
import readPartNumbers

# Allow us to import the client
this_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(this_dir)
sys.path.insert(0, '../../../client/')
sys.path.insert(0, '../../../server/')
sys.path.insert(0, (os.path.abspath('../../inter/misc')))

try:
    import board
    import neopixel

    pixels = neopixel.NeoPixel(board.D18, 15)

except ImportError:
    print("Not a raspberry so cant import board")

os.chdir(os.path.abspath('../../client/'))


def respond_start(message, sub_node, log_level, my_part_list=None):
    _primitives = primitives.Primitives(sub_node, log_level)
    arguments = _primitives.parse_cmd(message)
    print(arguments)

    if message.startswith("find"):
        line_number = arguments[0]
        color = arguments[1]
        parts = line_number.split("/")
        for item in parts:
            print(my_part_list)
            for i, data in enumerate(my_part_list):
                if int(item) == my_part_list[i][1]:
                    print("We found it", item)
                    print("location", my_part_list[i][0])
                    print('location', my_part_list)
                    location = my_part_list[i][0].split('-')
                    location = location[1]
                    light_neopixel(color, location)

        """Called by the client's listener_thread when it received a [name]: flag"""

        # find shelf for item num
        return

    if message.startswith("reset"):
        line_number = arguments[0]
        parts = line_number.split("/")
        for item in parts:
            for i, data in enumerate(my_part_list):
                if int(item) == my_part_list[i][1]:
                    location = my_part_list[i][0].split('-')
                    location = location[1]
                    clear_display(location)


def light_neopixel(color, location):
    section = {'0': [0, 1, 2],
               '1': [3, 4, 5],
               '2': [6, 7, 8],
               '3': [9, 10, 11],
               '4': [12, 13, 14]}
    color = color.split('/')
    red_val = int(color[0])
    green_val = int(color[1])
    blue_val = int(color[2])

    for i in section[location]:
        pixels[i] = (red_val, green_val, blue_val)


def clear_display(location):
    section = {'0': [0, 1, 2],
               '1': [3, 4, 5],
               '2': [6, 7, 8],
               '3': [9, 10, 11],
               '4': [12, 13, 14]}
    for i in section[location]:
        pixels[i] = (0, 0, 0)
    # Create the LED segment class.
    # This creates a 7 segment 4 character display:
    # Clear the display.
