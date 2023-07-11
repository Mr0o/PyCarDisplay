from time import sleep

from PyCarDisplay.display import lcdBig, lcdSmall

import sys
# debug flag, pass -d or --debug to the script to enable debug mode
if "-d" in sys.argv or "--debug" in sys.argv:
    debug = True
else:
    debug = False

if debug == False:
    import obd
else:
    # if the obd module is not installed, then use the test module for non-Raspberry Pi systems
    import PyCarDisplay.obd_test as obd

### USER DEFINED VARIABLE ###
MPG_CALIBRATE = 0.000 # this is to be a percentage that can be used to adjust the mpg value to be more accurate (set to 0 to ignore)
MPH_CALIBRATE = 0.075 # this is to be a percentage that can be used to adjust the mph value to be more accurate (set to 0 to ignore)

def connectOBD():
    #connect, will keep trying to connect until it is succesfull
    # using Async() rather than OBD() for improved performance
    c = obd.Async() # auto-connects to USB or RF port
    trys = 0
    while (c.status() == "Not Connected"):
        c = obd.Async() # auto-connects to USB or RF port
        trys += 1
        if trys == 5: # only clear the screen on the fifth attempt
            lcdBig.clear()
            lcdSmall.clear()
        if trys > 6: # seems to be taking a while (6 attempts)
            lcdSmall.text("Connecting..." + str(trys) , 1) # so let the user know whats happening
        if trys == 15: # more than 15 attempts, likely never going to connect
            lcdBig.text("No connection!", 1) # let the user know something is wrong
            lcdBig.text("Check obd...", 2) # offer a solution
        sleep (0.8)
    
    sleep(0.5)
    # all pids to watch (required for the asynchronous usage of python-obd)
    c.watch(obd.commands.RPM) # keep track of the RPM
    c.watch(obd.commands.SPEED)
    c.watch(obd.commands.MAF)
    c.watch(obd.commands.COMMANDED_EQUIV_RATIO)
    c.watch(obd.commands.AMBIANT_AIR_TEMP)
    c.watch(obd.commands.COOLANT_TEMP)
    c.watch(obd.commands.DISTANCE_SINCE_DTC_CLEAR)
    c.watch(obd.commands.RELATIVE_THROTTLE_POS)
    c.watch(obd.commands.RUN_TIME)

    c.start() # start the async update loop
        
    return c


def get_DISTANCE_SINCE_DTC_CLEAR(command: obd.Async):
    cmd = command.query(obd.commands.DISTANCE_SINCE_DTC_CLEAR) # send the command, and parse the response
    if not cmd.is_null():
        miles_elapsed = cmd.value.magnitude
        miles_elapsed = miles_elapsed * 0.62137 #convert kilometers to miles
    else:
        miles_elapsed = 0
        print("DISTANCE_SINCE_DTC_CLEAR is null")

    return miles_elapsed 


def get_AMBIANT_AIR_TEMP(command: obd.Async):
    #ambient air temperature
    cmd = command.query(obd.commands.AMBIANT_AIR_TEMP) # send the command, and parse the response
    if not cmd.is_null():
        air_temp = cmd.value.magnitude
        air_temp = round(air_temp * 1.8 + 32.00) #convert celsius to fahrenheit
    else:
        air_temp = "--"
        print ("AMBIANT_AIR_TEMP is null")
    
    return air_temp


def get_COOLANT_TEMP(command: obd.Async):
    #coolant temperature
    cmd = command.query(obd.commands.COOLANT_TEMP) # send the command, and parse the response
    if not cmd.is_null():
        engine_temp = cmd.value.magnitude
        engine_temp = engine_temp * 1.8 + 32.00 #convert celsius to fahrenheit
    else:
        engine_temp = 140
        print ("COOLANT_TEMP is null")

    return engine_temp


def get_RELATIVE_THROTTLE_POS(command: obd.Async):
    # throttle position
    cmd = command.query(obd.commands.RELATIVE_THROTTLE_POS) # send the command, and parse the response
    if not cmd.is_null():
        pedal = cmd.value.magnitude
    else:
        pedal = 100

    return pedal


def get_RUN_TIME(command: obd.Async):
    # run time
    seconds = None
    cmd = command.query(obd.commands.RUN_TIME) # send the command, and parse the response
    if not cmd.is_null():
        time_elapsed = cmd.value.magnitude
        seconds = time_elapsed
        hours = 0
        minutes = 0
        if seconds > 3600:
            hours = seconds // 3600
        if seconds > 60:
            seconds %= 3600
            minutes = seconds // 60
        time_elapsed = "%d:%02d" % (hours, minutes)
    else:
        if seconds:
            if minutes > 0 or hours > 0:
                time_elapsed = "%d:%02d" % (hours, minutes)
        else:
            time_elapsed = "-:--"

    return time_elapsed


def get_MPG_GPH_INSTANTANEOUS(command: obd.Async, pedal: int):
    maf = command.query(obd.commands.MAF) # send the command, and parse the response
    kph = command.query(obd.commands.SPEED) # send the command, and parse the response
    rpm = command.query(obd.commands.RPM) # send the command, and parse the response
    cer = command.query(obd.commands.COMMANDED_EQUIV_RATIO)

    # using the commanded equivelent ratio, we can get the actual af ratio that is being requested by the ECU 
    #   rather than assuming it will always be a perfect 14.7 af ratio (because in the real world, it isnt)
    if not cer.is_null():
        cer = cer.value.magnitude
    else:
        cer = 1 # if it cant get the commanded equiv ratio, then just set it as 1 to ignore this from the equation (less accurate)

    if not rpm.is_null():
        rpm = rpm.value.magnitude
    else:
        rpm = 1200 # if for some reason it cannot get the rpm, set it to something higher than 1100 to prevent issues

    if not maf.is_null():
        maf = maf.value.magnitude 
        maf_lbs = (maf / (14.7 / cer)) / 454 # convert g/s to lb/s in fuel from AF ratio
        gps = maf_lbs / 6.701 # convert lb/s to gallons per second
        gph = gps * 3600
        
        if rpm < 100.0: 
            gph = 0.0 # if the car is not running, then the fuel consumption is 0
    else:
        # it is possible to calculate mpg using data from the MAP in cases where the MAF is unavailable, but it has not been implemented 
        gph = 0.001 # in case we cannot get the MAF (this will not work, meaning we will not get the MPG)
        print ("MAF is null")
        
    if not kph.is_null():
        value = kph.value.magnitude
        mph = value * 0.62137 #convert kilometers to miles
        mph = mph + (mph * MPH_CALIBRATE) #adjust for mph calibration
    else:
        mph = 0 # in case for some reason we cannot get the speed
        print ("Speed is null")
    
    # if foot is off the pedal and speed is over 15, then it means we are coasting, so the fuel consupmtion is much lower, 
    # but only if the engine is over 1100rpm, because at some point the engine will need to use fuel to keep the engine idle
    if pedal < 1 and rpm > 950 and mph > 1:
            gph = 0.014 # magic number
    if pedal < 1 and rpm > 1100 and mph > 1:
            gph = 0.004 # magic number
    
    # mpg is 0 if the speed is 0 mph
    if mph < 1: # this prevents a divide by zero error
        mpg = 0.0
    else:
        mpg = mph / gph # get miles per gallon
    
    if mpg > 99: # max mpg is 99
        mpg = 99

    return mpg, gph