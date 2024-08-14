# Set RTC Unit for OT/IoT Device

### Configure DS1307 RTC on BeagleBone-Black Arduino or Raspberry PI



**Program Design Purpose**: Real time clock (RTC) module are widely used for System Clocks, Data Logging and Alarm Systems. Some times we need to set the module for some OT device such as a ship NEMA 0183 data recorder which record the ship engineer, rudder data. or set RTU for some IoT device which operating offline which can not connect to network time server. We will show how to integrate a simple DS1307 RTC unit in some wildly used micro controller used in OT and IoT  such as BeagleBone-Black, Arduino or Raspberry PI. 

```
# Created:     2024/08/11
# Version:     v_0.1.2
# Copyright:   Copyright (c) 2024 LiuYuancheng
# License:     MIT License
```

[TOC]

------

### Introduction

A Real-Time Clock (RTC) is a specialized computer clock that keeps track of the current time even when the main power is turned off. It is typically used in computers, embedded systems, and various electronics where accurate timekeeping is necessaries will show how to integrate a simple DS1307 RTC unit in some wildly used micro controller used in OT and IoT  such as BeagleBone-Black, Arduino or Raspberry PI. For each example, the explanation includes 3 part: 

- **Physical wire connection**: Show how to connect the DS1307 to the micro controller's GPIO pin and power on the data transmission. 

- **Library or driver configuration**:  Show how to install or config the I2C (a two-wire serial communication) lib or driver on the micro controller or your program. 
- **RTC time read and write**: Show how to setup the time to the DS1307 and read the time from it with your program.

#### Background Knowledge Introduction

In this section we will give a short introduction and the detail reference link about the hardware we used and the protocol for RTC data IO, if you are familiar about the DS1307 RTC, BBB, Arduino and Raspberry PI, you can skip this section. 

##### I2C DS1307 RTC

The DS1307 is a widely used RTC module that communicates via I2C and is commonly used in projects requiring basic timekeeping functionalities. RTC I2C DS1307 Module Including Coin Cell Battery is shown below:

![](doc/img/readme1.png)

Key Features of RTC:

- **Battery Backup**: RTC modules are often equipped with a small battery that allows them to keep time even when the main system is powered off.
- **I2C/SPI Interface**: RTCs commonly use communication protocols like I2C or SPI to interface with microcontrollers or processors.
- **Time and Date**: They maintain time (hours, minutes, seconds) and date (day, month, year) information.
- **Low Power Consumption**: Designed to consume minimal power, ensuring long battery life.

DS1307 RTC Detailed document link: https://www.analog.com/media/en/technical-documentation/data-sheets/ds1307.pdf

##### I2C Communication Protocol

I2C is **a two-wire serial communication protocol using a serial data line (SDA) and a serial clock line (SCL)**. The protocol supports multiple target devices on a communication bus and can also support multiple controllers that send and receive commands and data. Detail link: https://www.ti.com/lit/an/sbaa565/sbaa565.pdf?ts=1723523827811&ref_url=https%253A%252F%252Fwww.google.com%252F#:~:text=I2C%20is%20a%20two%2Dwire,and%20receive%20commands%20and%20data.

##### Micro Controller Introduction

- BeagleBone-Black: https://docs.beagleboard.org/latest/boards/beaglebone/black/ch04.html

- Arduino: https://www.arduino.cc/

- Raspberry PI: https://www.raspberrypi.com/

  

------

### Setup and Usage DS1307 RTC on BeagleBone-Black

This section will show how to connect the DS1307 RTC BeagleBone-Black. 

##### Wire Connection

1. Connect **VCC** on the RTC I2C DS1307 to the **P9_5** (VCC 5V) or **P9_7** (SYS 5V) pin on the BBB. NOTE: The **P9_5** VCC 5V pin will only be powered if a 5V adapter is plugged in to the barrel jack. If powering over USB use the **P9_7** (SYS 5V) pin instead! 
2. Connect GND on the breakout board to the **P9_1** (GND) pin on the BBB. 
3. Connect SDA on the breakout board to the **P9_20** pin of the BBB 
4. Connect SCL on the breakout board to the **P9_19** pin of the BBB

![](doc/img/rm_05.png)

heck if the DS1307 is properly connected and recognized by the BeagleBone Black by running the command `i2cdetect -y -r 1`. You should see the address `0x68`, which corresponds to the DS1307 module.

##### Library or driver configuration

Follow below steps to setup the DS1307 module

**Step1: Synchronize RTC Time with internet** 

After finished wired the RTC chip module wired up and verified that we can see the module with i2cdetect, we can set up the module. Now, execute the following to add the RTC chip to new device list:

```
echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device
```

After hooked the address to the BBB new device list, we can run the program to check the current time of the DS1307 module: 

```
hwclock -r -f /dev/rtc1
```

If this is the first time the module has been used it will report back Jan 1 2000, so we will need to set the time. The quickest way to set the time on the BeagleBone Black is to execute the following (The BBB need to connect to the internet):

```
/usr/bin/ntpdate -b -s -u pool.ntp.org
```

Now that the system time is set correctly, we can execute the following to write the system time to the DS1307:

```
hwclock -w -f /dev/rtc1
```

We can also verify whether it was set correctly by executing the following command to read the date and time from the DS1307 RTC:

```
hwclock -r -f /dev/rtc1
```

**Step 2: Create service that will run each time when BBB boot up (optional)** 

To start, create a directory and script that will be executed: `mkdir /usr/share/rtc_ds1307`

Copy `clock_init.sh` and `rtc-ds1307.service` in to the folder 

After copied the file, we'll need to actually enable the service so it starts each time as the system boots:

```
systemctl enable rtc-ds1307.service
```

The way to manually start and stop the service: 

```
systemctl start rtc-ds1307.service
systemctl stop rtc-ds1307.service
```

After reboot the BBB, the RTC I2C DS1307 Module can work normally now your program can use the system time lib.

**Step 3: Install the lib**

If your don't want to use the service in step 2, for your python program which to enable I2C1 (usually used for communication), you can use cmd: 

```
echo BB-I2C1 > /sys/devices/platform/bone_capemgr/slots
```

Install required library

```
sudo apt-get update
sudo apt-get install python3-pip
sudo pip3 install Adafruit_BBIO smbus2
```

##### Python Program to get the RTC data

After finished the config, you can use the below example to read the time data from the RTC

```python
import smbus2
import time

# Define the I2C bus and address of the DS1307 RTC
bus = smbus2.SMBus(1)  # Use '1' for I2C1 on BeagleBone Black
DS1307_ADDRESS = 0x68

# Function to convert BCD to decimal
def bcd_to_dec(bcd):
    return (bcd // 16 * 10) + (bcd % 16)

# Function to read the time from the DS1307 RTC
def read_time():
    # Read the time registers from the DS1307
    second = bus.read_byte_data(DS1307_ADDRESS, 0x00)
    minute = bus.read_byte_data(DS1307_ADDRESS, 0x01)
    hour = bus.read_byte_data(DS1307_ADDRESS, 0x02)
    day = bus.read_byte_data(DS1307_ADDRESS, 0x04)
    month = bus.read_byte_data(DS1307_ADDRESS, 0x05)
    year = bus.read_byte_data(DS1307_ADDRESS, 0x06)

    # Convert the BCD values to decimal
    second = bcd_to_dec(second)
    minute = bcd_to_dec(minute)
    hour = bcd_to_dec(hour)
    day = bcd_to_dec(day)
    month = bcd_to_dec(month)
    year = bcd_to_dec(year) + 2000  # The DS1307 only gives the last two digits of the year

    return (year, month, day, hour, minute, second)

# Main loop to print the time every second
while True:
    time_data = read_time()
    print("Date: {:02d}/{:02d}/{:04d} Time: {:02d}:{:02d}:{:02d}".format(
        time_data[2], time_data[1], time_data[0], time_data[3], time_data[4], time_data[5]))
    
    time.sleep(1)
```







The BeagleBone-Black doesn't have a embedded Real-Time Clock module, so if we powered off it and reboot it, if it is not connected to the internet, its time will be reset. We want to add a RTC unit to it so the program we run on the BBB will have RTC. 

We follow this tutorial link to do the RTC config: 

https://learn.adafruit.com/adding-a-real-time-clock-to-beaglebone-black



------

### Program Setup

###### Development Environment : BBB-Debian-V3, Shell

###### Additional Lib/Software Need: N.A

###### Hardware Needed

1. **BeagleBone-Black**:  https://beagleboard.org/black

2. **Tiny RTC I2C DS1307**: https://www.elecrow.com/wiki/index.php?title=Tiny_RTC

   We use RTC I2C DS1307 Module Including Coin Cell Battery to provide time to BBB. This is the description of RTC I2C DS1307 Module:

   

   RTC I2C DS1307 Module Features: 

   ```
   - The DS1307 I2C Real Time Clock chips (RTC) 
   - I2C EEPROM memory 24C32 32K 
   - To adopt LIR2032 rechargeable lithium battery, and with the charging circuit 
   - Solve the problem DS1307 with battery backup cannot read and write.
   - Fully charged, can provide the DS1307 timing. 
   - Compact design, 27mm * 28mm * 8.4mm 
   - Leads to the DS1307 clock pin for the MCU to provide the clock signal.
   ```

3. -

###### Program Files List 

version: v0.1

| Program File           | Execution Env | Description                                                  |
| ---------------------- | ------------- | ------------------------------------------------------------ |
| src/clock_init.sh      | shell         | Time data fetch program to get the real time from RTC        |
| src/rtc-ds1307.service | shell         | Service program to auto run the time fetch program when the BBB rebooted. |



------

### Program Usage

Follow below steps to set the program working for BBB: 

##### Step 1: Changed RTC I2C DS1307 Module for BBB

As the RTC I2C DS1307 Module was designed for the Arduino instead of BBB, when building the kit, we need to remove the pull up resistors (R2 and R3 which in the red box shown in the circuit diagram as shown below). 

![](doc/img/readme2.png)



We force the RTC to communicate at 3.3V instead of 5V, which is better for the BBB. The resistor needs to be unsoldered is shown below: 

![](doc/img/readme3.png)



##### Step 2: Connect the RTC to BBB for verification

After removed the pull up resistor of the RTC chip, the next step is connect to BBB for detection. The wiring work is simple: 

1. Connect **VCC** on the RTC I2C DS1307 to the **P9_5** (VCC 5V) or **P9_7** (SYS 5V) pin on the BBB. NOTE: The **P9_5** VCC 5V pin will only be powered if a 5V adapter is plugged in to the barrel jack. If powering over USB use the **P9_7** (SYS 5V) pin instead! 
2. Connect GND on the breakout board to the **P9_1** (GND) pin on the BBB. 
3. Connect SDA on the breakout board to the **P9_20** pin of the BBB 
4. Connect SCL on the breakout board to the **P9_19** pin of the BBB

The wire connection is shown below: 

<img src="doc/img/readme4.png" style="zoom: 67%;" />

Verify the wiring by running `i2cdetect -y -r 1` at the command line: If the ID 68 show up, the RTC is ready. As shown below: 

![](doc/img/readme5.png)

##### Step 3: Synchronize RTC Time with

After finished wired the RTC chip module wired up and verified that we can see the module with i2cdetect, we can set up the module. Now, execute the following to add the RTC chip to new device list:

```
echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device
```

After hooked the address to the BBB new device list, we can run the program to check the current time of the DS1307 module: 

```
hwclock -r -f /dev/rtc1
```

If this is the first time the module has been used it will report back Jan 1 2000, so we will need to set the time. The quickest way to set the time on the BeagleBone Black is to execute the following (The BBB need to connect to the internet):

```
/usr/bin/ntpdate -b -s -u pool.ntp.org
```

Now that the system time is set correctly, we can execute the following to write the system time to the DS1307:

```
hwclock -w -f /dev/rtc1
```

We can also verify whether it was set correctly by executing the following command to read the date and time from the DS1307 RTC:

```
hwclock -r -f /dev/rtc1
```







------

### Problem and Solution

###### 

**OS Platform** : na

**Error Message**: na

**Type**: na

**Solution**: na

**Related Reference**:  na



------

### Reference 

- https://learn.adafruit.com/adding-a-real-time-clock-to-beaglebone-black



------

> Last edit by LiuYuancheng(liu_yuan_cheng@hotmail.com) at 02/12/2020

