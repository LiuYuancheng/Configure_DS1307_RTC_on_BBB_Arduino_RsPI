# BeagleBone-Black--RTC-Config

**Program Design Purpose**: We want to add a Real-Time Clock unit to BBB it so the programs we run on the BBB will have real time info even the BBB is not connected to the internet. 

[TOC]

### Introduction

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

   ![](doc/img/readme1.png)

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



we force the RTC to communicate at 3.3V instead of 5V, which is better for the BBB. The resistor needs to be unsoldered is shown below: 
