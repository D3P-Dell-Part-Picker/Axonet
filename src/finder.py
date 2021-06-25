import os
import readPartNumbers
import partpicker_database
import socket

this_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(this_dir)


def respond_start(message):
    message = message.split(':')
    arguments = message[1:]
    if message[0] == "find" or message[0] == "reset":
        os.chdir(this_dir)
        pico_addresses = ["10.12.32.106", "10.12.32.107", "192.168.10.76", "192.168.10.4"]
        my_part_list = {}
        # TODO get part list for all arduino IP
        our_parts = readPartNumbers.find_my_parts(pico_addresses,
                                                  path_to_client=this_dir)
        for pico_address in our_parts:
            my_part_list[pico_address] = []
            for item in our_parts[pico_address]:
                line_num = item[3]
                part_location = item[2]
                my_part_list[pico_address].append([part_location, line_num])

        if message[0] == "find":
            line_number = arguments[0]
            try:
                color = arguments[1]
            except IndexError:
                print("No color was specified, or the command was not entered properly")
                return

            leds = {}
            update_leds = []
            add_leds = []
            update_timeout = []
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
                                            update_timeout.append([location])
                                        else:
                                            if bool(leds.get(key)):
                                                leds[key].append([color,
                                                                  location])
                                                update_leds.append([color_string, location])
                                            else:
                                                leds[key] = [[color, location]]
                                                update_leds.append([color_string,
                                                                    location])
                            # location isnt defined yet
                            for part_location in my_part_list[key][i][0]:
                                if any(part_location in x for x in current_leds):
                                    break
                                else:
                                    if bool(leds.get(key)):
                                        leds[key].append([color, part_location])
                                        add_leds.append([color, part_location])

                                        # locations equal
                                    else:
                                        leds[key] = [[color, part_location]]
                                        add_leds.append([color, part_location])
            if update_leds:
                print("Updating leds")
                partpicker_database.write_to_table("leds", update_leds, 0)
            if add_leds:
                print("Adding Leds")
                partpicker_database.write_to_table("leds", add_leds, 1)
            if update_timeout:
                print("Updating led timeout")
                partpicker_database.write_to_table("leds", update_timeout, 2)
            try:
                for key in leds:
                    for i, item in enumerate(leds[key]):
                        location_index = item[1].split('-')[1]
                        leds[key][i][1] = location_index
            except IndexError:
                print('Error in location naming')
            send_msg(leds)

        if message[0] == "reset":
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
        return


def send_msg(msg):  # This connects to the arduino and separates the color from the rack index with a '-' and each
    # color/index combo is separated by '|'
    print("Sending ", msg, " to Picos....")
    for key in msg:
        for i, item in enumerate(msg[key]):
            msg[key][i] = '-'.join(item)
        msg[key] = '|'.join(msg[key])
    for key in msg:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        out = msg[key].encode('utf-8')  # Add -!- to message to signify end of message for arduino
        try:
            s.settimeout(2)
            s.connect((key, 3706))  # change to address of arduino
            s.settimeout(None)
            print("Connected to " + key)
            s.sendall(out)
            s.settimeout(1)
            try:
                recieved = s.recv(1024).decode('utf-8')
                s.settimeout(None)
            except socket.timeout as error:
                # recieving timed out
                pass
            s.shutdown(0)
            s.close()

        except socket.timeout as error:
            print("Could not connect to " + key, "(" + str(error) + ")")
