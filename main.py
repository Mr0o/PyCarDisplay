from time import sleep
from PyCarDisplay.milesLogging import init_log, update_log, create_new_log
from PyCarDisplay.display import lcdBig, lcdSmall, LCD_Clear, LCD_Update, LCD_Error_Msg
from PyCarDisplay.obd_data import *

try:
    connection = connectOBD() # initial connection is made
except Exception as e:
    LCD_Error_Msg(str(e))
    sleep(2)

LCD_Clear()

init_log() # initialize the mileage log file

#give the obd connection a moment to gather the initial values
sleep(2) 

# gather the starting DTC mileage in order to calculate the trip distance
start_miles = get_DISTANCE_SINCE_DTC_CLEAR(connection)

previous_time_elapsed = "-:--"

#loop forever
while(True): 
    sleep(0.25)
    try:
        if connection.status() == "Not Connected":
            connection = connectOBD() # reconnect if it is disconnected

        ### get obd data ###
        air_temp = get_AMBIANT_AIR_TEMP(connection)
        engine_temp = get_AMBIANT_AIR_TEMP(connection)
        pedal = get_RELATIVE_THROTTLE_POS(connection)
        dtc_miles = get_DISTANCE_SINCE_DTC_CLEAR(connection)
        time_elapsed = get_RUN_TIME(connection)

        # get the elapsed miles this trip
        miles_elapsed = dtc_miles - start_miles
        # no negative miles
        if miles_elapsed < 0:
            miles_elapsed = 0

        ## get mpg ##
        mpg, gph = get_MPG_GPH_INSTANTANEOUS(connection, pedal)
        
        # check if the time elapsed has changed since the last loop
        time_elapsed_changed = False
        if time_elapsed != previous_time_elapsed:
            time_elapsed_changed = True
            previous_time_elapsed = time_elapsed

        # update the log, but only if the mileage is above 0 and the time elapsed has changed
        if miles_elapsed > 0 and time_elapsed != "-:--" and time_elapsed != "0:00" and time_elapsed_changed == True:
            try:
                update_log(miles_elapsed, time_elapsed) # update the mileage log file
            except Exception as e:
                # something has gone wrong, likely corrupted mileage log file
                # we will backup the old log file and create a new one
                print("ERROR: " + str(e))
                print("Creating a new mileage log file...")

                lcdBig.clear()
                lcdBig.text("ERROR: ", 1)
                lcdBig.text(str(e), 2)

                lcdSmall.clear()
                lcdSmall.text("Creating a new", 1)
                lcdSmall.text("log file...", 2)

                try:
                    create_new_log()
                except Exception as e:
                    print("ERROR: " + str(e))
                    LCD_Error_Msg(str(e))
                
                sleep(8)
        
        ## Update the LCD ##
        LCD_Update(air_temp, engine_temp, mpg, gph, time_elapsed, miles_elapsed)

    except Exception as e:
        """
        Catch any and all exceptions and print them out
        This is perhaps not the best idea, but it 
        will prevent the program from crashing
        and ensures the program keeps running
        """
        try:
            LCD_Error_Msg(str(e))
        except Exception:
            print("ERROR: " + str(e))

        sleep(1)
 
