import time
import datetime
import mysql.connector
import finder
from partpicker_database import query_database
from mysql.connector import errorcode


def init_db():
    try:
        part_picker_db = mysql.connector.connect(user='pi', password='Welcome00', host='10.12.33.231',
                                                 database='partpicker')
        return part_picker_db
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Credential Error")
        else:
            print(err)
    else:
        part_picker_db.close


def check_timeout():
    # TODO potentially send message to server for logging
    data_list = []
    rows = []
    table = query_database("leds")
    for item in table:
        try:
            if item[3] < datetime.datetime.now():
                rows.append(item)
        except TypeError:
            pass
    if rows:
        for row in rows:
            data = ["None", None, None, ""]
            data[3] = row[0]
            data_list.append(data)
        db = init_db()
        cursor = db.cursor()
        command = "UPDATE leds SET color = %s, timeout = %s, session_keys = %s WHERE location = %s"
        cursor.executemany(command, data_list)
        db.commit()
        cursor.close()
        db.close()
        parts = []
        table = query_database("racks")
        for item in table:  # find the part number from the location to reset it
            for x in item[2].split('/'):
                for y in data_list:
                    if x == y[3]:
                        if item[4] not in parts:
                            parts.append(item[4])
        command = "reset:"
        for part in parts:
            if part != parts[-1]:
                command += str(part) + '/'
            else:
                command += str(part) + ':0/0/0'
        finder.respond_start(command)


if __name__ == "__main__":
    while True:
        check_timeout()
        time.sleep(30)
