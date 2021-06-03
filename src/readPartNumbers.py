import sys
import os
import query_part_picker_db


def find_my_parts(arduino_addresses, path_to_client=None):
    """Given a nodes static IP, find all part numbers assigned to it in the master spreadsheet
        Returns list [(part number, part name, line #), ..., (part number n, part name n, line # n)]"""
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

        for row in query_part_picker_db.query_db():
            part_ip_row = row[3].split('/')
            for ip in part_ip_row:
                if ip_byte_four == ip:
                    parts[arduino_ip].append((row[0], row[1], row[2], row[4]))

    return parts


if __name__ == "__main__":
    # print(find_my_parts(_primitives.get_local_ip()))
    pass
