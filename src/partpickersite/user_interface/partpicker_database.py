import mysql.connector
from mysql.connector import errorcode

"""The plan is to call the write _to_table function in the mission_runner.py and the call.py python files when the 
activities such as a delivery or a call happen. 

Depending on the type of activity the data will be written to a specific table such as deliveries or calls.
"""


# set database to robot_db
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


def query_database(table):
    if table == "racks":
        part_picker_db = init_db()
        cursor = part_picker_db.cursor()
        query = "SELECT * FROM racks"
        data = None
        data_list = []
        cursor.execute(query, data)

        for item in cursor:
            # print(item)

            data_list.append(item)
        cursor.close()
        part_picker_db.close()
        return data_list
    elif table == "leds":
        part_picker_db = init_db()
        cursor = part_picker_db.cursor()
        query = "SELECT * FROM leds"
        data = None
        data_list = []
        cursor.execute(query, data)
        for item in cursor:
            # print(item)

            data_list.append(item)  # Add each row of items from the database to a list
        cursor.close()
        part_picker_db.close()
        return data_list


def write_to_table(table, data):
    if table == "racks":
        command = "INSERT INTO racks (part_number, description, location, ip) VALUES (%s ,%s, %s, %s)"
        write_data(command, data)
    elif table == "leds":
        command = "INSERT INTO leds (color, location) VALUES (%s ,%s)"
        write_data(command, data)


# writes to the partpicker database
def write_data(command, value):
    part_picker_db = init_db()
    cursor = part_picker_db.cursor()
    cursor.executemany(command, value)
    part_picker_db.commit()
    cursor.close()
    part_picker_db.close()

# data = ['051-020-011', 'Left mtg ear', 'GL Cube', '01']
# write_to_table("racks", data)
