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
        except:  # Add error exception, maybe index error, list out of range
            pass
        leds = {}
        update_leds = []
        add_leds = []
        parts = line_number.split("/")
        current_leds = partpicker_database.query_database("leds")
        for item in parts:
            for key in my_part_list:
                for i, data in enumerate(my_part_list[key]):
                    if int(item) == my_part_list[key][i][1]:
                        print("We found part", item)
                        print("location", my_part_list[key][i][0], key)
                        my_part_list[key][i][0] = my_part_list[key][i][0].split('/')
                        for led in current_leds:
                            r, g, b = led[1].split('/')
                            location = led[0]
                            for part_location in my_part_list[key][i][0]:
                                if location in part_location:
                                    print(location, "is in", part_location)
                                    if int(r) != 0 or int(g) != 0 or int(b) != 0:
                                        # TODO update the timeout or that led
                                        pass
                                    else:
                                        if bool(leds.get(key)):
                                            print("Adding", location, "to leds")
                                            leds[key].append([color,
                                                              location])  # TODO fix this... not all values are being
                                            # updated in the database... could have to fo with the any statement
                                            update_leds.append([color, location])
                                        else:
                                            print("Adding", location, "to leds")
                                            leds[key] = [[color, location]]
                                            update_leds.append([color, location])
                        for part_location in my_part_list[key][i][0]:
                            if any(part_location in x for x in current_leds):
                                print(part_location + " is in current leds")
                                break
                            else:
                                if bool(leds.get(key)):
                                    leds[key].append([color, part_location])
                                    print("Adding", location, "to leds")
                                    print(leds[key])
                                    add_leds.append([color, part_location])

                                    # locations equal
                                else:
                                    print("Adding", location, "to leds")
                                    leds[key] = [[color, location]]
                                    add_leds.append([color, part_location])

        print("LEDS", leds)
        print("UPDATE LEDS", update_leds)
        print("ADD LEDS", add_leds)
        if update_leds:
            print("Updating leds")
            partpicker_database.write_to_table("leds", update_leds, False)
        if add_leds:
            print("Adding Leds")
            partpicker_database.write_to_table("leds", add_leds, True)

        for key in leds:
            for i, item in enumerate(leds[key]):
                location_index = item[1].split('-')[1]
                leds[key][i][1] = location_index
        send_msg(leds)

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


def send_msg(msg):  # This connects to the arduino and separates the color from the rack index with a '-' and each
    # color/index combo is separated by '|'
    print("Sending ", msg, " to arduino....")
    for key in msg:
        for i, item in enumerate(msg[key]):
            msg[key][i] = '-'.join(item)
        msg[key] = '|'.join(msg[key])
    for key in msg:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            out = (msg[key] + '!').encode('utf-8')  # Add -!- to message to signify end of message for arduino
            try:
                s.settimeout(5)
                s.connect((key, 3706))  # change to address of arduino
                s.settimeout(None)
                print("Connected to " + key)
                s.sendall(out)
                s.shutdown(0)
                s.close()
            except socket.timeout as error:
                print("Could not connect to " + key, "(" + str(error) + ")")
