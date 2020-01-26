#include <SD.h>
#include <BMP280_DEV.h> 
#include "I2Cdev.h"
#include "MPU6050.h"
#include "Wire.h" 
#include <Servo.h>
File logFile;
MPU6050 sensor;
Servo myservo;
float temperature, pressure, altitude;            // Create the temperature, pressure and altitude variables
BMP280_DEV bmp280;                                // Instantiate (create) a BMP280_DEV object and set-up for I2C operation
int ax, ay, az;
int gx, gy, gz;
int potpin = 0;  // analog pin used to connect the potentiometer
int val;
int pos=0;
float h, hmax;
 
void setup()
{
  Serial.begin(57600);
  Wire.begin(); 
  sensor.initialize();
  bmp280.begin(BMP280_I2C_ALT_ADDR);
  bmp280.startNormalConversion(); 
  myservo.attach(9);
  hmax=0;
  Serial.print(F("Iniciando SD ..."));
  if (!SD.begin(4))
  {
    Serial.println(F("Error al iniciar"));
    return;
  }
  Serial.println(F("Iniciado correctamente"));
}

 
void loop()
{
  // Abrir archivo y escribir valor
  
  if (bmp280.getMeasurements(temperature, pressure, altitude))    // Check if the measurement is complete
  {
    sensor.getAcceleration(&ax, &ay, &az);
    sensor.getRotation(&gx, &gy, &gz);
    float ax_m_s2 = (ax-460) * (9.81/16384.0);
    float ay_m_s2 = (ay-245) * (9.81/16384.0);
    float az_m_s2 = (az-306) * (9.81/16384.0);
    float gx_deg_s = (gx+776) * (250.0/32768.0);
    float gy_deg_s = (gy-618) * (250.0/32768.0);
    float gz_deg_s = (gz+121) * (250.0/32768.0);
    Serial.print(temperature);                    // Display the results    
    Serial.print(F("*C   "));
    Serial.print(pressure);    
    Serial.print(F("hPa   "));
    Serial.print(altitude);
    Serial.println(F("m  "));
    Serial.print("a[x y z](m/s2) g[x y z](deg/s):\t");
    Serial.print(ax); Serial.print("\t");
    Serial.print(ay); Serial.print("\t");
    Serial.print(az); Serial.print("\t");
    Serial.print(gx); Serial.print("\t");
    Serial.print(gy); Serial.print("\t");
    
    logFile = SD.open("datalog.txt", FILE_WRITE);
    if (logFile) { 
      logFile.print(temperature); logFile.print("\t");
      logFile.print(altitude); logFile.print("\t");
      logFile.print(pressure); logFile.print("\t");
      logFile.print(ax_m_s2); logFile.print("\t");
      logFile.print(ay_m_s2); logFile.print("\t");
      logFile.print(az_m_s2); logFile.print("\t");
      logFile.print(gx_deg_s); logFile.print("\t");
      logFile.print(gy_deg_s); logFile.print("\t");
      logFile.print(gz_deg_s); logFile.print("\t");
      logFile.print(F("\n"));
      logFile.close();
      if  ( altitude-hmax  >  0 )
      { 
        hmax=altitude ; 
      }
      if  ( altitude-hmax  <  -2 ) 
      { 
        for (pos = 0; pos <= 180; pos += 1){
          val = analogRead(potpin);
          val = map(val, 0, 1023, 0, 180);  
          myservo.write(val);    
          hmax=500000;
          delay(15);
        }
        for (pos = 180; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
          val = analogRead(potpin);              // tell servo to go to position in variable 'pos'
          val = map(val, 0, 1023, 0, 180);
          myservo.write(val);
          hmax=500000;
          delay(15);   
        }
      } 
  
    
  }
  }
}
