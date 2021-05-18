import csv
import sys
import os
import urllib.request
import urllib.error
import query_part_picker_db

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


def find_my_parts(arduino_addresses, directory_server, path_to_client=None):
    """Given a nodes static IP, find all part numbers assigned to it in the master spreadsheet
        Returns list [(part number, part name, line #), ..., (part number n, part name n, line # n)]"""
    if path_to_client:
        try:
            os.chdir(path_to_client)
        except FileNotFoundError:
            print("Directory does't exist: " + str(path_to_client))
            return

    parts = {}
    for arduino_ip in arduino_addresses:
        parts[arduino_ip] = []
        ip_bytes = arduino_ip.split('.')
        ip_byte_four = ip_bytes[4 - 1]

        _primitives.log("Fetching part numbers for " + arduino_ip + "...", in_log_level="Debug")

        """try:
            racks_csv_text = _primitives.download_file(directory_server + "Racks.csv")
    
            if racks_csv_text != 1:
                open(os.path.abspath("./Racks.csv"), "w").write(racks_csv_text)
                part_number_assignments = open("./Racks.csv")
            else:
                raise urllib.error.URLError("Could not access Racks.csv. Directory server offline?")
    
        except urllib.error.URLError:
            print("ERROR: No internet connection detected; cannot download Racks file... Searching for local copy...")
    
            try:
                part_number_assignments = open(os.path.abspath("./Racks.csv"))
                print("Local Racks.csv found! Proceeding...")
    
            except FileNotFoundError:
                print("ERROR: No local Racks file found; cannot proceed; returning no parts")
                return []
    
        csv_reader = csv.reader(part_number_assignments, delimiter=',')
        """
        for row in query_part_picker_db.query_db():
            if ip_byte_four == row[3]:
                parts[arduino_ip].append((row[0], row[1], row[2], row[4]))

        _primitives.log("Found " + str(len(parts[arduino_ip])) + " parts assigned to " + arduino_ip + "...", in_log_level='Debug')

    return parts


if __name__ == "__main__":
    print(find_my_parts(_primitives.get_local_ip()))
"""
    for row in csv_reader:
        # TODO Search database
        if ip_byte_four in row[3]:
            our_parts.append((row[0], row[1], row[4]))

    _primitives.log("Found "+str(len(our_parts)) + " parts assigned to "+local_ip+"...", in_log_level='Debug')

    return our_parts
"""
