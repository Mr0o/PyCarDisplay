import os
import datetime
import csv

MILEAGE_LOG_FILE = 'mileage_log.csv'

def init_log() -> None:
    # check if the mileage log file exists
    try:
        with open(MILEAGE_LOG_FILE, mode='r') as mileage_log:
            mileage_log.close()
        print("Opening mileage log file...")
    except FileNotFoundError:
        print("Creating mileage log file...")
        with open(MILEAGE_LOG_FILE, mode='w') as mileage_log:
            mileage_writer = csv.writer(mileage_log, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            mileage_writer.writerow(['Date', 'Mileage', 'Elapsed Time']) # write the column headers to the csv file

    # create a new row in the mileage log file
    with open(MILEAGE_LOG_FILE, mode='a') as mileage_log:
        # write a new row with the current date and -1 values for mileage and time
        mileage_writer = csv.writer(mileage_log, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        mileage_writer.writerow([datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S"), "NULL", "NULL"])


def update_log(miles_elapsed: int, time_elapsed: str) -> None:
     # edit the last row of the csv file to update the mileage and time elapsed with the current values
    with open(MILEAGE_LOG_FILE, mode='r') as mileage_log:
        mileage_reader = csv.reader(mileage_log, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        mileage_list = list(mileage_reader)
        mileage_list[-1][1] = round(miles_elapsed)
        mileage_list[-1][2] = time_elapsed
        mileage_log.close()

    # write the updated list to the csv file
    with open(MILEAGE_LOG_FILE, mode='w') as mileage_log:
        mileage_writer = csv.writer(mileage_log, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in mileage_list:
            mileage_writer.writerow(row)
        mileage_log.close()


def delete_log() -> None:
    # delete the mileage log file
    os.remove(MILEAGE_LOG_FILE)


def create_new_log() -> None:
    # delete the old log file and create a new one
    delete_log()
    init_log()
