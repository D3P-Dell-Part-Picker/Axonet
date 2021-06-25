import datetime
import importlib
import os
import socket
import struct
import sys
from hashlib import sha3_224


def inject(parts, color):
    r = color[0]
    g = color[1]
    b = color[2]
    rgb = str(r) + '/' + str(g) + '/' + str(b)
    msg = parse_msg((parts, rgb))
    out = msg.encode('utf-8')
    with socket.socket() as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # out = msg.encode('utf-8')  # Add -!- to message to signify end of message for arduino
        s.connect(('10.12.33.231', 3705))
        s.sendall(out)
        s.close()

    return [(r, g, b)]


def reset_led(parts,
              key):  # TODO try to reset LED # session key appears to be the same at different times so utilize it
    temp = []
    for item in parts:
        if item not in temp:
            temp.append(item)
    parts = temp
    print("Attempting to reset", parts, "for", key)
    command = "reset:"
    for index, part in enumerate(parts):
        if part != parts[len(parts) - 1]:
            command += part + '/'
        else:
            command += part
    command += ":0/0/0"
    out = command.encode('utf-8')
    with socket.socket() as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # out = msg.encode('utf-8')  # Add -!- to message to signify end of message for arduino
        s.connect(('10.12.33.231', 3705))
        s.sendall(out)
        s.close()


def parse_msg(message):
    # take all of the parts and create individual messages to inject into the network
    if type(message) != str:
        part_list = []
        command = "find:"  # add the find flag to the beginning of the message
        for i, part in enumerate(message[0]):
            print(i, part)
            rgb = message[1]
            part_list.insert(i, part[4])
        for i, item in enumerate(part_list):
            if i + 1 == len(part_list):  # if the part is the last in the list do not add a slash at the end
                command = command + str(item)
            else:  # the part is not the last in the list so a slash delimiter must be added to seperate from the
                # next part
                command = command + str(item) + '/'

        command = command + ":" + rgb # separate the parts from the color with the ":" delimiter
        return command
    else:
        command = 'reset:'
        message = message.strip('"')
        command += message
        print(command)
        return command


def prepare(message):
    """ Assign unique hashes to messages ready for transport.
        Returns (new hashed message) -> str """

    # Sign the message
    # timestamp = str(datetime.datetime.utcnow())
    # hash_input = timestamp + message
    # sig = sha3_224(hash_input.encode()).hexdigest()[:16]

    # out = sig + ":" + message

    # Prepend message length
    # message = message + '!'
    out = message.encode('utf-8')
    # out_with_padding = struct.pack(">I", len(out)) + out
    # print(out)
    # out = bytearray(out_with_padding)

    return out
