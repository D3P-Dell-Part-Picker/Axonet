import os
import sys
import time
import primitives
import client
import readPartNumbers
import partpicker_database
import socket

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

    if message.startswith("find"):
        line_number = arguments[0]
        try:
            color = arguments[1]
        except:
            pass
        leds = {}
        update_leds = [];
        parts = line_number.split("/")
        current_leds = partpicker_database.query_database("leds")
        colors_in_use = []
        for item in parts:
            for key in my_part_list:
                for i, data in enumerate(my_part_list[key]):
                    if int(item) == my_part_list[key][i][1]:
                        print("We found part", item)
                        print("location", my_part_list[key][i][0], key)
                        # TODO Fix logic here.. manually typing flags updates database but web interface does not
                        for led in current_leds:
                            r, g, b = led[1].split('/')
                            location = led[0]
                            if location == my_part_list[key][i][0]:
                                if int(r) != 0 or int(g) != 0 or int(b) != 0:
                                    # TODO update the timeout or that led
                                    pass
                                else:
                                    # light_neopixel(color, location_index)
                                    if bool(leds.get(key)):
                                        leds[key].append([color, location])  # TODO fix this appending
                                        # locations equal
                                    else:
                                        leds[key] = [[color, location]]
                                    # to 0/0/0
                                    # several times
                        # leds.insert(0, key)
        for key in leds:
            for item in leds[key]:
                update_leds.append([item[0], item[1]])
        print(update_leds)
        # partpicker_database.write_to_table("leds", update_leds)
        # importlib.reload(sys.modules['simpleInjector'])
        for key in leds:
            for i, item in enumerate(leds[key]):
                location_index = item[1].split('-')[1]
                leds[key][i][1] = location_index
        send_msg(leds)  # TODO send a message to each arduino with the corresponding colors and led section
        # simpleInjector.run(msg=location_index)
        """Called by the client's listener_thread when it received a [name]: flag"""

        # find shelf for item num
        return

    if message.startswith("reset"):
        line_number = arguments[0]
        parts = line_number.split("/")
        for item in parts:
            for key in my_part_list:
                for i, data in enumerate(my_part_list[key]):
                    if int(item) == my_part_list[key][i][1]:
                        location = my_part_list[key][i][0].split('-')
                        location = location[1]
                        clear_display(location)


def light_neopixel(color, location):  # This code is for the raspberry pi if raspberry pis are used to light neopixels
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
        pass
        # pixels[i] = (red_val, green_val, blue_val)


def clear_display(location):
    section = {'0': [0, 1, 2],
               '1': [3, 4, 5],
               '2': [6, 7, 8],
               '3': [9, 10, 11],
               '4': [12, 13, 14]}
    for i in section[location]:
        pixels[i] = (0, 0, 0)


def send_msg(msg): # This connects to the arduino and seperates the color from the rack index with a '-' and each
    # color/index combo is seperated by '|'
    for key in msg:
        for i, item in enumerate(msg[key]):
            msg[key][i] = '-'.join(item)
        msg[key] = '|'.join(msg[key])
    for key in msg:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print(msg[key])
            out = (msg[key] + '!').encode('utf-8') # Add -!- to message to signify end of message for arduino
            s.bind(('0.0.0.0', 3706))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print("Connected with", addr, key)
                if addr[0] == key:
                    print(conn.send(out))
                conn.close()
                # TODO close connection
        # connection = socket.socket()
        pass
