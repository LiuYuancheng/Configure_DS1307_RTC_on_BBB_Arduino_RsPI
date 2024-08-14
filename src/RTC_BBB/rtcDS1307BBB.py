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