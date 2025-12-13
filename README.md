# PyCarDisplay

# Image
![PyCarDisplay Demo Image](https://github.com/Mr0o/PyCarDisplay/blob/master/demo.jpg)

This is a simple car display for the Raspberry Pi. It uses 2 i2c LCD displays connected to a Raspberry Pi.

Data from the car is read from the OBD2 port using a USB to OBD2 cable. It is possible to use a Bluetooth OBD2 adapter, but USB is more reliable.

Here is the list of data that is currently displayed:

    - Outside temperature (F)
    - Engine temperature (coolant)
    - Instantaneous fuel consumption (Traditional MPG)
    - Instantaneous fuel consumption (Gallons per hour)
    - Miles traveled since start (Trip)
    - Time since engine start (Trip)