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


def rename_log() -> None:
    # rename the old log file to keep as backup (if it is perhaps corrupted, but still has data contained within it)
    # check if a log file already exists
    # get files in current directory
    files = os.listdir()
    # check if the log file exists
    if MILEAGE_LOG_FILE[:-4] + "(1)" not in files:
        # if it is not found, rename the log file to include "(1)" at the end
        os.rename(MILEAGE_LOG_FILE, MILEAGE_LOG_FILE[:-4] + "(1)")
    else:
        # get all the files containing .csv in the name
        csv_files = [i for i in files if ".csv" in i]
        # get the highest number in the list of files before the .csv extension
        highest_number = max([int(i[-5]) for i in csv_files])
        # rename the log file with +1 to the highest number
        os.rename(MILEAGE_LOG_FILE, MILEAGE_LOG_FILE[:-5] + "(" + str(highest_number + 1) + ").csv")


def create_new_log() -> None:
    # rename the old log file and create a new one
    rename_log()
    init_log()
