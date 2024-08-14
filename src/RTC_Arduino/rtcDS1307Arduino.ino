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
