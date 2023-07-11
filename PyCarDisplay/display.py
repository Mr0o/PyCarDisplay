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

# connect to LCD displays, if it fails to connect, try again until it is succesfull
lcdSmall = None
lcdBig = None

failed = True
while(failed):
    try:
        lcdSmall = LCD(0x27) # address for the 16x2 display is 0x27
        lcdBig = LCD(0x26) # address for the 20x4 display is 0x26
        failed = False
    except Exception:
        print("ERROR: Failed to connect to the LCD Displays! Check the I2C connection!")
        sleep(1)

def getTempGauge(t: int) -> str:
    # check that the argument is an integer
    if type(t) != int:
        t = 125
    # create temperature bar guage
    temp_bar = ""
    if t < 125: #less than 125 degrees, consider it a cold engine
        temp_bar = "_______  C"
    if t >= 120:
        temp_bar = "_______"
    if t >= 146:
        temp_bar = chr(255) + "______"
    if t >= 157:
        temp_bar = "_" + chr(255) + "_____"
    if t >= 168:
        temp_bar = "__" + chr(255) + "____"
    if t >= 177:
        temp_bar = "___" + chr(255) + "___"
    if t >= 205:
        temp_bar = "____" + chr(255) +"__"
    if t >= 217:
        temp_bar = "_____" + chr(255) + "_"
    if t >= 227:
        temp_bar = "______" + chr(255)
    if t >= 237:
        temp_bar = "______" + chr(255) + "  H"

    return temp_bar

def LCD_Update(air_temp, engine_temp, mpg_display, gph, time_elapsed, miles_elapsed) -> str:
    ### print to LCD ###
    lcdSmall.text("Outside: "+ str(air_temp) +chr(223)+"F", 1)
    lcdSmall.text("Eng: " + getTempGauge(engine_temp), 2) 

    space = ""
    if round(mpg_display) < 10: 
        space = " " # improves formatting

    lcdBig.text("MPG: " +space+ str(round(mpg_display)) + "  GPH: " + str(round(gph, 2)), 1)
    lcdBig.text("Time: " + time_elapsed, 3)
    lcdBig.text("Miles: " + str(round(miles_elapsed)), 4)


def LCD_Clear():
    lcdSmall.clear()
    lcdBig.clear()


def LCD_Error_Msg(msg: str):
    lcdBig.text("ERROR: ", 1)
    lcdBig.text(str(msg), 2)

def LCD_Idle():
    # print blank values to the LCD while we wait a few seconds for the obd data to load (obd is asynchronous, it will run during the sleep command)
    lcdSmall.text("Outside: --" +chr(223)+"F", 1)
    lcdSmall.text("Eng: " + getTempGauge(130), 2)

    lcdBig.text("MPG: --  Gph: --", 1)
    #lcdBig.text("Avg MPG: --", 2)
    lcdBig.text("Time: -:--", 3)
    lcdBig.text("Miles: -", 4)
