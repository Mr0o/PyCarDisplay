from rpi_lcd import LCD
from time import sleep

lcdSmall = LCD(0x27)
lcdBig = LCD(0x26)

lcdSmall.clear()
engine_temp = 90
while(1):
    engine_temp += 5
    #engine_temp = engine_temp * 1.8 + 32.00 #convert celsius to fahrenheit
    temp_bar = ""
    if engine_temp < 120: #less than 120 degrees, consider it a cold engine
        temp_bar = "_______  C"
    if engine_temp >= 120:
        temp_bar = "_______"
    if engine_temp >= 160:
        temp_bar = chr(255) + "______"
    if engine_temp >= 175:
        temp_bar = chr(255) + chr(255) + "_____"
    if engine_temp >= 185:
        temp_bar = chr(255) + chr(255) + chr(255) + "____"
    if engine_temp >= 195:
        temp_bar = chr(255) + chr(255) + chr(255) + chr(255) + "___"
    if engine_temp >= 217:
        temp_bar = chr(255) + chr(255) + chr(255) + chr(255) + chr(255) +"__"
    if engine_temp >= 222:
        temp_bar = chr(255) + chr(255) + chr(255) + chr(255) + chr(255) + chr(255) + "_"
    if engine_temp >= 227:
        temp_bar = chr(255) + chr(255) + chr(255) + chr(255) + chr(255) + chr(255) + chr(255)
    if engine_temp >= 233:
        temp_bar = chr(255) + chr(255) + chr(255) + chr(255) + chr(255) + chr(255) + chr(255) + "  H"
        
    lcdSmall.text("Outside: 78"+chr(223)+"F", 1)
    lcdSmall.text("Eng: " + temp_bar, 2)
    lcdBig.text("MPG: 26  Fuel: 0.8", 1)
    lcdBig.text("Avg MPG: 31.4", 2)
    lcdBig.text("test", 3)
    lcdBig.text("test", 4)

    if engine_temp > 250: engine_temp = 90 #reset
    sleep(0.25)
    
        
        
    
