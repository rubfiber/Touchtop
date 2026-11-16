#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

Adafruit_MPU6050 mpu;

float roll = 0.0;
float pitch = 0.0;
unsigned long lastTime = 0;

void setup() {
  Serial.begin(115200);
  while (!Serial) delay(10);

  if (!mpu.begin()) {
    Serial.println("no mpu found");
    while (1) delay(10);
  }

  mpu.setAccelerometerRange(MPU6050_RANGE_2_G);
  mpu.setGyroRange(MPU6050_RANGE_250_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

  lastTime = millis();
}

void loop() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  unsigned long currentTime = millis();
  float dt = (currentTime - lastTime) / 1000.0;
  lastTime = currentTime;

  float accelRoll  = atan2(a.acceleration.y, a.acceleration.z) * 180.0 / PI;
  float accelPitch = atan2(-a.acceleration.x, sqrt(a.acceleration.y * a.acceleration.y + a.acceleration.z * a.acceleration.z)) * 180.0 / PI;

  float gyroX = g.gyro.x * 180.0 / PI;
  float gyroY = g.gyro.y * 180.0 / PI;

  roll  = 0.96 * (roll + gyroX * dt) + 0.04 * accelRoll;
  pitch = 0.96 * (pitch + gyroY * dt) + 0.04 * accelPitch;

  Serial.print("Roll: ");
  Serial.print(roll, 1);
  Serial.print(" deg\tPitch: ");
  Serial.print(pitch, 1);
  Serial.println(" deg");

  delay(20);
}
