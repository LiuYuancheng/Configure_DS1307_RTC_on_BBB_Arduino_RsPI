# Set RTC Unit for OT/IoT Device

### Configure DS1307 RTC on BeagleBone-Black Arduino or Raspberry PI



**Program Design Purpose**: Real time clock (RTC) module are widely used for System Clocks, Data Logging and Alarm Systems. Some times we need to set the module for some OT device such as a ship NEMA 0183 data recorder which record the ship engineer, rudder data. or set RTU for some IoT device which operating offline which can not connect to network time server. We will show how to integrate a simple DS1307 RTC unit in some wildly used micro controller used in OT and IoT  such as BeagleBone-Black, Arduino or Raspberry PI. 

```
# Created:     2024/08/11
# Version:     v_0.1.2
# Copyright:   N.A
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

### Setup DS1307 RTC on 3.3 V OT device

Based on the DS1307 RTC document page 3/14, the MAX SDA, SCL = 5.0V, if your OT micro controller's signal voltage control is 3.3V, we can reduce the signal voltage by remove 2 pull-up resistors. 

As shown in the below circuit diagram, the SDA and SDL are connect to the VCC with the two 3.3K pull up register R2 and R3. 

![](doc/img/rm_03.png)

If we unsolder the 2 register, the output will be the DS1307 chips' out put voltage which is Max 3.5V, then for the OT device which use 3.3V voltage system  



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

For detailed code and program please refer to `src/rtcBBB` . 



------

### Setup and Usage DS1307 RTC on Arduino

##### Wire Connection

1. Connect VCC on the RTC I2C DS1307 to the Pin 17 (+5V )  on Arduino Uno/Nano. 
2. Connect GND on the breakout board to the Pin 19 (GND) pin on the Arduino Uno/Nano. 
3. Connect SDA on the breakout board to the Pin25 (A4/D18) pin on the Arduino Uno/Nano. 
4. Connect SCL on the breakout board to the Pin24 (A5/D19) on the Arduino Uno/Nano. 

![](doc/img/rm_06.png)

##### Library or driver configuration

To read time data from a DS1307 RTC module using I2C with an Arduino, you will need to use the `Wire.h` library to communicate with the module. 

Then from the lib Arduino IDE search RTClib to install the `RTClib.h` which can easily interact with DS1307 and other RTC modules. as shown below:

![](doc/img/rm_07.png)

##### C++ Program to get the RTC data

After finished the config, you can use the below example to read the time data from the RTC

```c++
#include <Wire.h>
#include <RTClib.h>  // You need to install the RTClib library in the Arduino IDE

RTC_DS1307 rtc;

void setup() {
  // Start the serial communication
  Serial.begin(9600);
  // Start the I2C communication
  Wire.begin();
  // Check if the RTC is connected properly
  if (!rtc.begin()) {
    Serial.println("Couldn't find RTC");
    while (1);
  }

  // Check if the RTC is running
  if (!rtc.isrunning()) {
    Serial.println("RTC is NOT running!");
    // Uncomment the following line to set the RTC time to the time the sketch was compiled
    // rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }
}

void loop() {
  // Get the current time from the RTC
  DateTime now = rtc.now();

  // Print the current date and time to the serial monitor
  Serial.print(now.year(), DEC);
  Serial.print('/');
  Serial.print(now.month(), DEC);
  Serial.print('/');
  Serial.print(now.day(), DEC);
  Serial.print(" ");
  Serial.print(now.hour(), DEC);
  Serial.print(':');
  Serial.print(now.minute(), DEC);
  Serial.print(':');
  Serial.print(now.second(), DEC);
  Serial.println();

  // Wait 1 second before repeating
  delay(1000);
}

```

For detailed code and program please refer to `src/rtcArduino` . 



------

### Setup and Usage DS1307 RTC on Raspberry PI

##### Wire Connection

1. Connect VCC on the RTC I2C DS1307 to the Pin 3 or Pin4 (+5V )  on Raspberry PI. 
2. Connect GND on the breakout board to the Pin 6 (GND) pin on Raspberry PI. 
3. Connect SDA on the breakout board to the Pin3 (GPIO2) pin on the Raspberry PI. 
4. Connect SCL on the breakout board to the Pin5 ((GPIO3) on the Raspberry PI. 

![](doc/img/rm_08.png)

Same as setting on BeagleBone-Black, ensure that the DS1307 RTC is working and connected correctly by running `i2cdetect -y 1` in the terminal. You should see `0x68` listed, which is the address of the DS1307.

##### Library or driver configuration

To read time data from a DS1307 RTC module using I2C on a Raspberry Pi, you can use the `smbus` or `smbus2` library in Python. Below is an example code to read the time from a DS1307 RTC module. We need to enable the GPIO I2C Interface first. 

Run `sudo raspi-config`. 

![](doc/img/rm_09.png)

Then navigate to `Interfacing Options` > `I2C` and enable it.

![](doc/img/rm_10.png)

Install necessary packages: `sudo apt-get install -y python-smbus i2c-tools`. For newer newer Raspberry Pi models Opens I2C bus 1 with `smbus.SMBus(1)`

##### Python Program to get the RTC data

```
import smbus
import time

# Define the I2C bus and address of the DS1307 RTC
bus = smbus.SMBus(1)  # Use '1' for I2C on newer Raspberry Pi models
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

For detailed code and program please refer to `src/rtcRspI` . 

------

### Reference 

- https://learn.adafruit.com/adding-a-real-time-clock-to-beaglebone-black



------

> Last edit by LiuYuancheng(liu_yuan_cheng@hotmail.com) at 14/08/2024
