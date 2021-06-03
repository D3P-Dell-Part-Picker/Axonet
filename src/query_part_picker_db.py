import partpicker_database


def query_db():
    racks_data = partpicker_database.query_database("racks")

    return racks_data
