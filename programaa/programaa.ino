#include <SD.h>
#include <BMP280_DEV.h> 
#include "I2Cdev.h"
#include "MPU6050.h"
#include "Wire.h" 
File logFile;
MPU6050 sensor;
float temperature, pressure, altitude;            // Create the temperature, pressure and altitude variables
BMP280_DEV bmp280;                                // Instantiate (create) a BMP280_DEV object and set-up for I2C operation
int ax, ay, az;
int gx, gy, gz;
 
void setup()
{
  Serial.begin(57600);
  Wire.begin(); 
  sensor.initialize();
  bmp280.begin(BMP280_I2C_ALT_ADDR);
  bmp280.startNormalConversion(); 
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
      } 
  
    
  }
  
}
