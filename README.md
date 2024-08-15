# Set RTC Unit for OT/IoT Device

### Configure DS1307 RTC on BeagleBone-Black Arduino or Raspberry PI

![](doc/img/title.png)

**Program Design Purpose**: Real-Time Clock (RTC) modules are essential for maintaining accurate timekeeping in various applications, including system clocks, data logging, and alarm systems. In scenarios where devices operate offline, such as a ship's NMEA 0183 data recorder that logs engine and rudder data, or an RTU (Remote Terminal Unit) which time state change configuration or IoT devices that cannot connect to a network time server, an RTC is crucial. This guide demonstrates how to integrate a DS1307 RTC module with commonly used microcontrollers in OT (Operational Technology) and IoT (Internet of Things) environments, such as the BeagleBone-Black, Arduino, and Raspberry Pi.

```
# Created:     2024/08/11
# Version:     v_0.1.2
# Copyright:   N.A
# License:     MIT License
```

**Table of Contents**

[TOC]

------

### Introduction

A Real-Time Clock (RTC) is a specialized clock that maintains accurate timekeeping even when the main power is turned off. RTCs are crucial in computers, embedded systems, and other electronics where continuous time tracking is necessary. This project will demonstrate how to integrate a DS1307 RTC module with popular microcontrollers used in Operational Technology (OT) and Internet of Things (IoT) applications, such as the BeagleBone-Black, Arduino, and Raspberry Pi. Each example will cover three key areas:

- **Physical Wiring Connection**: Instructions on connecting the DS1307 to the microcontroller's GPIO pins and powering the data transmission.
- **Library or Driver Configuration**: Guidance on installing or configuring the I2C (a two-wire serial communication protocol) library or driver on the microcontroller or in your program.
- **RTC Time Read and Write**: Steps to set the time on the DS1307 and read the time from it using your program.

#### Background Knowledge Introduction

This section provides an overview and reference links for the hardware and protocols used in this project. If you are already familiar with the DS1307 RTC, BeagleBone-Black, Arduino, and Raspberry Pi, you can skip this section.

##### I2C DS1307 RTC

The DS1307 is a widely-used RTC module that communicates via I2C and is suitable for basic timekeeping applications. It includes a coin cell battery, ensuring that it keeps time even when the main power is off. RTC I2C DS1307 Module Including Coin Cell Battery is shown below:

![](doc/img/readme1.png)

**Key Features of the DS1307 RTC:**

- **Battery Backup**: Ensures timekeeping continues even during power loss.
- **I2C Interface**: Allows communication with microcontrollers via the I2C protocol.
- **Time and Date Management**: Tracks hours, minutes, seconds, day, month, and year.
- **Low Power Consumption**: Designed to consume minimal power, extending battery life.

DS1307 RTC Detailed document link: https://www.analog.com/media/en/technical-documentation/data-sheets/ds1307.pdf

##### I2C Communication Protocol

I2C is **a two-wire serial communication protocol using a serial data line (SDA) and a serial clock line (SCL)**. The protocol supports multiple target devices on a communication bus and can also support multiple controllers that send and receive commands and data. Detail link: https://www.ti.com/lit/an/sbaa565/sbaa565.pdf?ts=1723523827811&ref_url=https%253A%252F%252Fwww.google.com%252F#:~:text=I2C%20is%20a%20two%2Dwire,and%20receive%20commands%20and%20data.

##### Micro Controller Introduction

- **BeagleBone-Black**: https://docs.beagleboard.org/latest/boards/beaglebone/black/ch04.html

- **Arduino:** https://www.arduino.cc/

- **Raspberry PI**: https://www.raspberrypi.com/




------

### Setting Up the DS1307 RTC for 3.3V OT Devices

According to the DS1307 RTC datasheet (page 3/14), the maximum voltage for the SDA and SCL lines is 5.0V. If your OT microcontroller operates at 3.3V signal levels, you can adapt the DS1307 module by removing the two pull-up resistors connected to the SDA and SCL lines before link it to your OT controller.

In the circuit diagram below, the SDA and SCL lines are connected to VCC through two 3.3kΩ pull-up resistors, R2 and R3.

![](doc/img/rm_03.png)

By unsoldering these two resistors, the output voltage will be directly from the DS1307 chip, which has a maximum output of 3.5V. This adjustment ensures compatibility with OT devices that operate on a 3.3V system.



------

### Setting Up and Using the DS1307 RTC on BeagleBone-Black

This section explains how to connect and configure the DS1307 RTC with the BeagleBone Black.

#### Wire Connection

1. **VCC Connection**: Connect the **VCC** pin on the DS1307 RTC to the **P9_5** (VCC 5V) or **P9_7** (SYS 5V) pin on the BeagleBone Black. **Note**: The **P9_5** VCC 5V pin will only be powered if a 5V adapter is plugged into the barrel jack. If powering the BeagleBone Black via USB, use the **P9_7** (SYS 5V) pin instead.
2. **GND Connection**: Connect the **GND** pin on the DS1307 RTC to the **P9_1** (GND) pin on the BeagleBone Black.
3. **SDA Connection**: Connect the **SDA** pin on the DS1307 RTC to the **P9_20** pin on the BeagleBone Black.
4. **SCL Connection**: Connect the **SCL** pin on the DS1307 RTC to the **P9_19** pin on the BeagleBone Black.

The connection detail is shown below:

![](doc/img/rm_05.png)

To check if the DS1307 is properly connected and recognized by the BeagleBone Black, run the command `i2cdetect -y -r 1`. The address `0x68` should appear, indicating that the DS1307 module is correctly connected.

#### **Library or driver configuration**

Follow below steps to setup the DS1307 module

**Step1: Synchronize RTC Time with internet** 

Once the DS1307 module is wired up and recognized, you can set up the module by adding it to the device list with below commands :

```
echo ds1307 0x68 > /sys/class/i2c-adapter/i2c-1/new_device
```

After adding the DS1307 to the BeagleBone Black’s device list, check the current time on the module with cmd:

```
hwclock -r -f /dev/rtc1
```

If this is the first time the module has been used, it may display the default date of `Jan 1, 2000`. To set the time, connect the BeagleBone Black to the internet and run to synchronize the time or use time cmd to setup the time directly:

```
/usr/bin/ntpdate -b -s -u pool.ntp.org
```

Once the system time is set correctly, write the system time to the DS1307:

```
hwclock -w -f /dev/rtc1
```

Verify the time has been set correctly by reading the date and time from the DS1307 RTC:

```
hwclock -r -f /dev/rtc1
```

**Step 2: Create a Time Correct Service to Run on Boot (Optional)**

To start, create a directory and script that will be executed: `mkdir /usr/share/rtc_ds1307`

Copy `clock_init.sh` and `rtc-ds1307.service` in to the folder 

Enable the service to start on boot:

```
systemctl enable rtc-ds1307.service
```

The way to manually start and stop the service: 

```
systemctl start rtc-ds1307.service
systemctl stop rtc-ds1307.service
```

After rebooting the BeagleBone Black, the DS1307 RTC module should function correctly, allowing your program to utilize the system time library.

**Step 3: Install the IC2 Library **

If your don't want to use the service in step 2, for your python program which to enable I2C1 (usually used for communication), you can use below cmd: 

```
echo BB-I2C1 > /sys/devices/platform/bone_capemgr/slots
```

Install required library

```
sudo apt-get update
sudo apt-get install python3-pip
sudo pip3 install Adafruit_BBIO smbus2
```

#### Python Program to Get the RTC Data

After finished the config, you can use the below example to read the time data from the RTC:

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

For detailed code and program please refer to the programs in folder  `src/rtcBBB` . 



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
