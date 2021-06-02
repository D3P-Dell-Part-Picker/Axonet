import csv
import sys
import os
import urllib.request
import urllib.error
import partpicker_database.query_database as query_database

sys.path.insert(0, (os.path.abspath('../misc')))

import primitives
import os

_primitives = primitives.Primitives("Client", "Debug")


def download_racks_csv(url):
    response = urllib.request.urlopen(url)
    data = response.read()  # a `bytes` object
    text = data.decode('utf-8')  # a `str`; this step can't be used if data is binary
    racks_file = open("Racks.csv", "w")
    racks_file.write(text)


def find_my_parts(arduino_addresses, path_to_client=None):
    # Given a nodes static IP, find all part numbers assigned to it in the database

    if path_to_client:
        try:
            os.chdir(path_to_client)
        except FileNotFoundError:
            print("Directory doesn't exist: " + str(path_to_client))
            return

    parts = {}
    for arduino_ip in arduino_addresses:
        parts[arduino_ip] = []
        ip_bytes = arduino_ip.split('.')
        ip_byte_four = ip_bytes[4 - 1]

        _primitives.log("Fetching part numbers for " + arduino_ip + "...", in_log_level="Debug")

        for row in query_database("racks"):
            part_IPsrow = row[3].split('/')
            for ip in part_IPsrow:
                if ip_byte_four == ip:
                    parts[arduino_ip].append((row[0], row[1], row[2], row[4]))

        _primitives.log("Found " + str(len(parts[arduino_ip])) + " parts assigned to " + arduino_ip + "...",
                        in_log_level='Debug')

    return parts


if __name__ == "__main__":
    print(find_my_parts(_primitives.get_local_ip()))
