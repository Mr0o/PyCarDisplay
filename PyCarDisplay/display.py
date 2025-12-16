from time import sleep

import sys
# debug flag, pass -d or --debug to the script to enable debug mode
if "-d" in sys.argv or "--debug" in sys.argv:
    debug = True
else:
    debug = False

if debug == False:
    from rpi_lcd import LCD
else:
    # if the rpi_lcd module is not installed, then use the test module for non-Raspberry Pi systems
    from PyCarDisplay.rpi_lcd_test import LCD

from PyCarDisplay.user_configs import USE_METRIC, LCD_SMALL_ADDR, LCD_BIG_ADDR
from PyCarDisplay.user_configs import COLD_ENGINE_MAX, HOT_ENGINE_MIN
from PyCarDisplay.user_configs import TEMP_LEVEL_ZERO, TEMP_LEVEL_ONE, TEMP_LEVEL_TWO, TEMP_LEVEL_THREE
from PyCarDisplay.user_configs import TEMP_LEVEL_FOUR, TEMP_LEVEL_FIVE, TEMP_LEVEL_SIX, TEMP_LEVEL_SEVEN

# connect to LCD displays, if it fails to connect, try again until it is succesfull
lcdSmall = None
lcdBig = None

failed = True
while(failed):
    try:
        lcdSmall = LCD(LCD_SMALL_ADDR) # address for the 16x2 display
        lcdBig = LCD(LCD_BIG_ADDR) # address for the 20x4 display
        failed = False
    except Exception:
        print("ERROR: Failed to connect to the LCD Displays! Check the I2C connection!")
        print("Check I2C address in user_configs.py and ensure I2C is enabled on the Raspberry Pi.\n")
        sleep(1)

def getTempGauge(t) -> str:
    # create temperature bar guage
    temp_bar = ""
    if t < COLD_ENGINE_MAX: # less than COLD_ENGINE_MAX, consider it a cold engine - "C"
        temp_bar = "_______  C"
    if t >= TEMP_LEVEL_ZERO:
        temp_bar = "_______"
    if t >= TEMP_LEVEL_ONE:
        temp_bar = chr(255) + "______"
    if t >= TEMP_LEVEL_TWO:
        temp_bar = "_" + chr(255) + "_____"
    if t >= TEMP_LEVEL_THREE:
        temp_bar = "__" + chr(255) + "____"
    if t >= TEMP_LEVEL_FOUR:
        temp_bar = "___" + chr(255) + "___"
    if t >= TEMP_LEVEL_FIVE:
        temp_bar = "____" + chr(255) + "__"
    if t >= TEMP_LEVEL_SIX:
        temp_bar = "_____" + chr(255) + "_"
    if t >= TEMP_LEVEL_SEVEN:
        temp_bar = "______" + chr(255)
    if t >= HOT_ENGINE_MIN: # greater than HOT_ENGINE_MIN, consider it a hot engine - "H"
        temp_bar = "______" + chr(255) + "  H"

    return temp_bar

def LCD_Update(air_temp, engine_temp, mpg_display, gph, time_elapsed, miles_elapsed) -> str:
    ### print to LCD ###
    if not USE_METRIC:
        lcdSmall.text("Outside: "+ str(air_temp) +chr(223)+"F", 1)
        lcdSmall.text("Eng: " + getTempGauge(engine_temp), 2) 

        space = ""
        if round(mpg_display) < 10: 
            space = " " # improves formatting

        lcdBig.text("MPG: " +space+ str(round(mpg_display)) + "  GPH: " + "{:.2f}".format(gph), 1)
        lcdBig.text("                    ", 2)
        lcdBig.text("Time: " + time_elapsed, 3)
        lcdBig.text("Miles: " + str(round(miles_elapsed)), 4)
    
    # METRIC
    else:
        # convert values to metric
        air_temp_c = round((air_temp - 32) * 5.0/9.0)
        km_elapsed = miles_elapsed * 1.609344
        lkm_display = 235.2145 / mpg_display if mpg_display != 0 else 0
        lph = gph * 0.264172
                           
        lcdSmall.text("Outside: "+ str(air_temp_c) +chr(223)+"C", 1)
        lcdSmall.text("Eng: " + getTempGauge(engine_temp), 2) 

        space = ""
        if round(lkm_display) < 10: 
            space = " " # improves formatting
        
        lcdBig.text("L/100km: " +space+ str(round(lkm_display)) + "  L/h: " + "{:.2f}".format(lph), 1)
        lcdBig.text("                    ", 2)
        lcdBig.text("Time: " + time_elapsed, 3)
        lcdBig.text("Km: " + str(round(km_elapsed)), 4)


def LCD_Clear():
    lcdSmall.clear()
    lcdBig.clear()


def LCD_Error_Msg(msg: str):
    lcdBig.text("ERROR: ", 1)
    lcdBig.text(str(msg), 2)

def LCD_Idle():
    if not USE_METRIC:
        # print blank values to the LCD while we wait a few seconds for the obd data to load (obd is asynchronous, it will run during the sleep command)
        lcdSmall.text("Outside: --" +chr(223)+"F", 1)
        lcdSmall.text("Eng: " + getTempGauge(130), 2)

        lcdBig.text("MPG: --  Gph: --", 1)
        lcdBig.text("                    ", 2)
        lcdBig.text("Time: -:--", 3)
        lcdBig.text("Miles: -", 4)
    
    # METRIC
    else:
        # print blank values to the LCD while we wait a few seconds for the obd data to load (obd is asynchronous, it will run during the sleep command)
        lcdSmall.text("Outside: --" +chr(223)+"C", 1)
        lcdSmall.text("Eng: " + getTempGauge(130), 2)

        lcdBig.text("L/100km: -- L/h: -- ", 1)
        lcdBig.text("                    ", 2)
        lcdBig.text("Time: -:--", 3)
        lcdBig.text("Km: -", 4)
