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

os.chdir(os.path.abspath('../../client/'))


def respond_start(message, sub_node, log_level, my_part_list=None):
    _primitives = primitives.Primitives(sub_node, log_level)
    arguments = _primitives.parse_cmd(message)

    if message.startswith("find"):
        line_number = arguments[0]
        try:
            color = arguments[1]
        except IndexError:
            print("No color was specified, or the command was not entered properly")  # Add error exception, maybe
            # index error, list out of range

        leds = {}
        update_leds = []
        add_leds = []
        led_dict = {
            'red': '255/0/0',
            'green': '0/255/0',
            'blue': '0/0/255',
            'white': '255/255/255',
            'yellow': '255/150/0',
            'purple': '200/0/255',
            'light_blue': '0/255/255',
            'orange': '255/50/0',
            'mint_green': '0/255/50',
            'pink': '255/75/125',
            'None': "0/0/0"
        }
        color_dict = {
            '255/0/0': 'red',
            '0/255/0': 'green',
            '0/0/255': 'blue',
            '255/255/255': 'white',
            '255/150/0': 'yellow',
            '200/0/255': 'purple',
            '0/255/255': 'light_blue',
            '255/50/0': 'orange',
            '0/255/50': 'mint_green',
            '255/75/125': 'pink',
            '0/0/0': 'None'
        }
        parts = line_number.split("/")
        current_leds = partpicker_database.query_database("leds")  # Get the currently lit leds from the database
        for item in parts:
            for key in my_part_list:
                for i, data in enumerate(my_part_list[key]):
                    if int(item) == my_part_list[key][i][1]:
                        print("We found part", item)
                        print("location", my_part_list[key][i][0], key)
                        my_part_list[key][i][0] = my_part_list[key][i][0].split('/')
                        for led in current_leds:

                            color_string = color_dict[color]
                            r, g, b = led_dict[led[1]].split('/')
                            location = led[0]
                            for part_location in my_part_list[key][i][0]:
                                if location in part_location:

                                    if int(r) != 0 or int(g) != 0 or int(b) != 0:
                                        # TODO update the timeout or that led
                                        pass
                                    else:
                                        # print(leds)
                                        if bool(leds.get(key)):
                                            leds[key].append([color,
                                                              location])  # TODO fix this... not all values are being
                                            # updated in the database... could have to fo with the any statement
                                            update_leds.append([color_string, location])
                                        else:
                                            leds[key] = [[color, location]]
                                            update_leds.append([color_string,
                                                                location])
                        for part_location in my_part_list[key][i][0]:
                            if any(part_location in x for x in current_leds):
                                break
                            else:
                                if bool(leds.get(key)):
                                    leds[key].append([color, part_location])
                                    print(leds[key])
                                    add_leds.append([color, part_location])

                                    # locations equal
                                else:
                                    leds[key] = [[color, location]]
                                    add_leds.append([color, part_location])

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
        parts = arguments[0].split("/")
        color = arguments[1]
        leds = {}
        for item in parts:
            for key in my_part_list:
                for i, data in enumerate(my_part_list[key]):
                    if int(item) == my_part_list[key][i][1]:
                        print("We found part", item)
                        print("location", my_part_list[key][i][0], key)
                        my_part_list[key][i][0] = my_part_list[key][i][0].split('/')
                        for location in my_part_list[key][i][0]:
                            temp = location.split('-')[1]
                            if bool(leds.get(key)):
                                leds[key].append([color,
                                                  temp])
                            else:
                                leds[key] = [[color, temp]]
        send_msg(leds)


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
                s.settimeout(2)
                s.connect((key, 3706))  # change to address of arduino
                s.settimeout(None)
                print("Connected to " + key)
                s.sendall(out)
                s.shutdown(0)
                s.close()
            except socket.timeout as error:
                print("Could not connect to " + key, "(" + str(error) + ")")
