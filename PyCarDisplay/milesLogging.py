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
        clean_csv_files()
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

def clean_csv_files() -> None:
    with open('combined.csv', mode='w') as combined_csv:
        combined_writer = csv.writer(combined_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        combined_writer.writerow(['Date', 'Mileage', 'Elapsed Time'])

        # get files in current directory
        files = os.listdir()
        # check if the log file exists
        # get all the files containing .csv in the name
        csv_files = [i for i in files if ".csv" in i]
        if len(csv_files) == 0:
            return
        
        # combine the csv files and remove NUL bytes
        for csv_file in csv_files:
            with open(csv_file, mode='r') as mileage_log:
                # remove NUL bytes from the csv file upon reading it
                mileage_reader = csv.reader((line.replace('\0','') for line in mileage_log), delimiter=",", quoting=csv.QUOTE_MINIMAL)
                mileage_list = list(mileage_reader)
                for row in mileage_list:
                    # do not write the column headers to the combined csv file
                    if row != ['Date', 'Mileage', 'Elapsed Time']:
                        combined_writer.writerow(row)

    # move all the old csv files to a backup folder
    backup_folder = "backup"
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)

    for csv_file in csv_files:
        # exclude the combined.csv file from being moved to the backup folder
        if csv_file != "combined.csv":
            os.rename(csv_file, backup_folder + "/" + csv_file)

    # rename the combined csv file to the original csv file name
    os.rename("combined.csv", MILEAGE_LOG_FILE)
    
    print("CSV log files cleaned")


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
    # get files in current directory
    files = os.listdir()
    # check if the log file exists
    # get all the files containing .csv in the name
    csv_files = [i for i in files if ".csv" in i]
    if len(csv_files) == 0:
        print("ERROR: Cannot rename log file, no csv files found!")
        return
    if len(csv_files) == 1:
        # if there are no csv files, rename the log file to include "(1)" at the end
        os.rename(MILEAGE_LOG_FILE, MILEAGE_LOG_FILE[:-4] + "(1).csv")
        return
    print("Renaming the log file...")
    # get the highest number in the list of files before the .csv extension
    highest_number = max([int(i[-6]) for i in csv_files if i[-6].isdigit()])
    if highest_number+1 < 10:
        # rename the log file with +1 to the highest number
        os.rename(MILEAGE_LOG_FILE, MILEAGE_LOG_FILE[:-4] + "(" + str(highest_number + 1) + ").csv")
    if highest_number == 9:
        # we have too many log file backups, so we will not rename the log file
        print("WARNING: Maximum number of log files reached!")
        return


def create_new_log() -> None:
    # rename the old log file and create a new one
    rename_log()
    init_log()
