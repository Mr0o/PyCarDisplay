### LCD ADDRESSES ###
LCD_SMALL_ADDR = 0x27 # I2C address of small LCD (16x2)
LCD_BIG_ADDR   = 0x26 # I2C address of big LCD (20x4)

# UNITS
USE_METRIC = False
# note: this will not apply to the values recorded in the log

# Size of tank for MPG AVG calculation
FUEL_TANK_SIZE_GALLONS = 18.0 # size of fuel tank in gallons

### USER DEFINED CALIBRATION OFFSET ###
# adjustment goes like this: actual
MPG_CALIBRATE = 0.000 # this is to be a value that can be used to adjust the mpg value to be more accurate (set to 0 to ignore)
MPH_CALIBRATE = 0.000 # this is to be a value that can be used to adjust the mph value to be more accurate (set to 0 to ignore)

### RANGE OF VALUES FOR TEMPERATURE GAUGE ###
# UNITS IN DEGREES FAHRENHEIT #
# These values are configured for my particular vehicle (2.0L 4-cylinder), your car may run at different temps
# Adjust these values as needed to better fit your vehicle's temperature range
COLD_ENGINE_MAX  = 125 # if temp is below this value, consider it a cold engine
TEMP_LEVEL_ZERO  = 120
TEMP_LEVEL_ONE   = 146
TEMP_LEVEL_TWO   = 157
TEMP_LEVEL_THREE = 168
TEMP_LEVEL_FOUR  = 177
TEMP_LEVEL_FIVE  = 205
TEMP_LEVEL_SIX   = 217
TEMP_LEVEL_SEVEN = 224
HOT_ENGINE_MIN   = 230 # if temp is above this value, consider it a hot engine
