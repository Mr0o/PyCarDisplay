# PyCarDisplay

### This is a simple car display for the Raspberry Pi. It uses 2 i2c LCD displays connected to a Raspberry Pi.

Data from the car is read from the OBD2 port using a USB to OBD2 cable. It is possible to use a Bluetooth OBD2 adapter, but USB is more reliable.

<img src="https://github.com/Mr0o/PyCarDisplay/blob/master/demo.jpg?raw=true" alt="PyCarDisplay Demo Image" width="50%" />

Here is the list of data that is currently displayed:

    - Outside temperature (F)
    - Engine temperature (coolant)
    - Instantaneous fuel consumption (Traditional MPG)
    - Instantaneous fuel consumption (Gallons per hour)
    - Miles traveled since start (Trip)
    - Time since engine start (Trip)

# How to Set Up (Instructions)

## Raspberry Pi Setup
1. Install [Raspberry Pi OS](https://www.raspberrypi.com/software/operating-systems/) on your Raspberry Pi.
2. Connect the two i2c LCD displays to the Raspberry Pi using the following connections:

   - **LCD 1**:
     - VCC to 5V
     - GND to GND
     - SDA to SDA (GPIO 2)
     - SCL to SCL (GPIO 3)

   - **LCD 2**:
     - VCC to 5V
     - GND to GND
     - SDA to SDA (GPIO 2)
     - SCL to SCL (GPIO 3)

   > Note: Both displays share the same I2C bus, so ensure they have different I2C addresses. This may require changing the address of one of the displays using jumpers or solder pads on the display module. The addresses used in this project are `0x27` for the smaller 16x2 display and `0x26` for the larger 20x4 display.

## Set up PyCarDisplay
1. Open a terminal on the Raspberry Pi.
   ```
    cd ~/Desktop
   ```
2. Clone this repository to your Desktop:
    ```
    git clone https://github.com/Mr0o/PyCarDisplay.git
    ```
3. Change to the PyCarDisplay directory:
    ```
    cd PyCarDisplay
   ```
4. Run the install script to set up the environment and install dependencies:
    ```
    bash install.sh
    ```
5. Reboot the Raspberry Pi to verify that it is working:
    ```
    sudo reboot
    ```
6. Done! Just make sure the LCDs are connected and the OBD2 cable is plugged in.
## Set up PyCarDisplay (Manually)

1. Open a terminal on the Raspberry Pi.
   ```
    cd ~/Desktop
   ```
2. Clone this repository to your Desktop:
   ```
    git clone https://github.com/Mr0o/PyCarDisplay.git
    ```
3. Change to the PyCarDisplay directory:
    ```
    cd PyCarDisplay
    ```
4. Create a Python virtual environment:
    ```
    python3 -m venv env
    ```
5. Activate the virtual environment:
    ```
    source env/bin/activate
    ```
6. Install the required Python packages:
    ```
    pip3 install -r requirements.txt
    ```
7. Make the run.sh script executable:
    ```
    chmod +x run.sh
    ```
8. Set up the script to run on startup by adding it to .bashrc:
    ```
    echo "bash /home/$USER/Desktop/PyCarDisplay/run.sh &" >> ~/.bashrc
    ```
     > <i>It should be noted that modifying .bashrc will cause the script to run every time a terminal is opened. If this is not desired, consider using other methods to run the script on startup, such as cron jobs or systemd services. </i>
9. Reboot the Raspberry Pi to test the setup:
    ```
    sudo reboot
    ```
10. After rebooting, the PyCarDisplay script should start automatically, and you should see data on the LCD displays once connected to the car's OBD2 port.