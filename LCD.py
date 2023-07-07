from rpi_lcd import LCD
import obd

import pickle # used for saving and loading data

from time import sleep

### USER DEFINED VARIABLE ###
MPG_CALIBRATE = 0.000 # this is to be a percentage that can be used to adjust the mpg value to be more accurate (set to 0 to ignore)
MPH_CALIBRATE = 0.075 # this is to be a percentage that can be used to adjust the mph value to be more accurate (set to 0 to ignore)

### load mpg data and calculate average mpg ###
path_to_pickle = '/home/pi/Desktop/mpg.pkl'


# connect to LCD displays, if it fails to connect, try again until it is succesfull
failed = True
while(failed):
    try:
        lcdSmall = LCD(0x27) # address for the 16x2 display is 0x27
        lcdBig = LCD(0x26) # address for the 20x4 display is 0x26
        failed = False
    except Exception:
        print("ERROR: Failed to connect to the LCD Displays! Check the I2C connection!")
        sleep(1)

lcdSmall.clear()
lcdBig.clear()

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
            lcdBig.text("Check odb...", 2) # offer a solution
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

def getTempGauge(t):
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

try:
    connection = connectOBD() # initial connection is made
except Exception as e:
    print("ERROR: " + str(e))
    lcdBig.text("ERROR: ", 1)
    lcdBig.text(str(e), 2)
    sleep(2)
    

# declaring variables with values of 0
avg_mpg = 0.0
mpg = 0
mph = 0
loops = 0

mpgData = []
try:
    # load average mpg data from file
    with open(path_to_pickle, 'rb') as f:
        mpgData = pickle.load(f)

    # calculate the average mpg
    mpg_sum = 0
    for i in mpgData:
        mpg_sum = mpg_sum + i
        avg_mpg =  mpg_sum / (len(mpgData) + 0.0001) # add a small number to prevent divide by zero
except Exception: # if the file does not exist, generate a new file
    mpgData = []
    print("Creating new file: 'mpg.pkl'")
    lcdSmall.clear()
    lcdBig.text("Creating new file", 1)
    lcdBig.text("'mpg.pkl'  ", 2)
    
    # generate a new pickle file with a blank array
    with open(path_to_pickle, 'wb') as f:
        pickle.dump(mpgData, f)
                
    sleep(3) # gives enough time for the user to see the message, otherwise it would just print and then instantly be cleared


# clear the displays
lcdSmall.clear()
lcdBig.clear()

# print blank values to the LCD while we wait a few seconds for the obd data to load (obd is asynchronous, it will run during the sleep command)
lcdSmall.text("Outside: --" +chr(223)+"F", 1)
lcdSmall.text("Eng: " + getTempGauge(130), 2)

lcdBig.text("MPG: --  Gph: --", 1)
#lcdBig.text("Avg MPG: --", 2)
lcdBig.text("Time: -:--", 3)
lcdBig.text("Miles: -", 4)

sleep(2) #give the obd connection a moment to gather the initial values

# gather the starting DTC mileage in order to calculate the trip distance
cmd = connection.query(obd.commands.DISTANCE_SINCE_DTC_CLEAR) # send the command, and parse the response
if not cmd.is_null():
    start_miles = cmd.value.magnitude
    start_miles = start_miles * 0.62137 #convert kilometers to miles
else:
    start_miles = 0


while(1): #loop forever
    sleep(0.25)
    try:
        if connection.status() == "Not Connected":
            connection = connectOBD() # reconnect if it is disconnected
        ### get obd data ###
        
        #ambient air temperature
        cmd = connection.query(obd.commands.AMBIANT_AIR_TEMP) # send the command, and parse the response
        if not cmd.is_null():
            air_temp = cmd.value.magnitude
            air_temp = round(air_temp * 1.8 + 32.00) #convert celsius to fahrenheit
        else:
            air_temp = "--"
            print ("Ambiant_Temp is null")
          
        #coolant temperature
        cmd = connection.query(obd.commands.COOLANT_TEMP) # send the command, and parse the response
        if not cmd.is_null():
            engine_temp = cmd.value.magnitude
            engine_temp = engine_temp * 1.8 + 32.00 #convert celsius to fahrenheit
        else:
            engine_temp = 140
            print ("Coolant_Temp is null")
        
        # throttle position
        cmd = connection.query(obd.commands.RELATIVE_THROTTLE_POS) # send the command, and parse the response
        if not cmd.is_null():
            pedal = cmd.value.magnitude
        else:
            pedal = 100

        # NOTE: if 'DISTANCE_SINCE_DTC_CLEAR' starts at a mileage such as '22,067.9' miles, the '.9' will be truncated
        # this can cause the miles elapsed to register as 1 mile even though you actually traveled 0.1 miles
        cmd = connection.query(obd.commands.DISTANCE_SINCE_DTC_CLEAR) # send the command, and parse the response
        if not cmd.is_null():
            current_miles = cmd.value.magnitude
            current_miles = current_miles * 0.62137 #convert kilometers to miles
            miles_elapsed = current_miles - start_miles
        else:
            miles_elapsed = 0

        
        cmd = connection.query(obd.commands.RUN_TIME) # send the command, and parse the response
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
            time_elapsed = str(0)

        ######## get mpg #########
        maf = connection.query(obd.commands.MAF) # send the command, and parse the response
        kph = connection.query(obd.commands.SPEED) # send the command, and parse the response
        rpm = connection.query(obd.commands.RPM) # send the command, and parse the response
        cer = connection.query(obd.commands.COMMANDED_EQUIV_RATIO)

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
            
        # average mpg
        if seconds > 1: # ignore mpg data if the car hasnt started yet (run time less than 1 second)
            if gph >= 0.01: 
                mpgData.append(mpg)
            else: # if there is no fuel being used (gph < 0.01) add 50% to the average mpg to increase the overall average
                  # this is to reflect the fuel economy of coasting in gear (uses no fuel, which means higher mpg)
                mpgData.append(avg_mpg + avg_mpg * 0.50) 
            ## find the average mpg ##
            mpg_sum = 0
            for i in mpgData:
                mpg_sum = mpg_sum + i
            avg_mpg =  mpg_sum / len(mpgData)
                
        # average mpg data should be limited to prevent an excessive amount of data being saved
        ## the mpg array will begin at a minimum of 25,000 and reset each time its size reaches 100,000
        if len(mpgData) > 100000: # limit the size of the mpg array to 100,000
            while(len(mpgData) > 25000): # set the size of the mpg array to 25,000
                mpgData.pop(0) # pop the first value until the size of the array is 25,000
        
        ### save average mpg data to file, only after every 100 loops ### 
        loops = loops + 1
        if loops > 100:
            loops = 0
            # save the data
            with open(path_to_pickle, 'wb') as f:
                pickle.dump(mpgData, f)
            
        
        ### print to LCD ###
        lcdSmall.text("Outside: "+ str(air_temp) +chr(223)+"F", 1)
        lcdSmall.text("Eng: " + getTempGauge(engine_temp), 2) 
        
        #calibrate MPG before displaying it
        mpg_display = round(mpg)
        if mpg == 99:
            mpg_display = 99 
        
        avg_display = round((avg_mpg - (avg_mpg*MPG_CALIBRATE)), 1)
        
        space = ""
        if round(mpg_display) < 10: space = " " # this fixes a spacing issue and makes it look nicer
        lcdBig.text("MPG: " +space+ str(mpg_display) + "  GPH: " + str(round(gph, 2)), 1)
        #lcdBig.text("Avg MPG: " + str(avg_display), 2)
        lcdBig.text("Time: " + time_elapsed, 3)
        lcdBig.text("Miles: " + str(round(miles_elapsed)), 4)
        #lcdBig.text("Miles: " + str(round(miles_elapsed)) + "  " + str(round(mph)) + "MPH:", 4) # for debugging ###REMOVE THIS###
        
        
    except Exception as e:
        """
        Catch any and all exceptions and print them out
        This is perhaps not the best idea, but it 
        will prevent the program from crashing
        and ensures the program keeps running
        """
        print("ERROR: " + str(e))
        lcdBig.clear()
        lcdBig.text("ERROR:", 1)
        lcdBig.text(str(e), 2)
        sleep(1)
 
