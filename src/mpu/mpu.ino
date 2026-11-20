#include <Wire.h>
#include <MPU6050_light.h>

MPU6050 mpu(Wire);

uint32_t prev_ms = 0;

void setup() {
    Serial.begin(115200);
    Wire.begin();

    byte status = mpu.begin();
    Serial.print("MPU6050/6500 status: ");
    Serial.println(status);
    while (status != 0) {
        Serial.println("Connection failed. Check wiring!");
        delay(2000);
    }

    Serial.println("Keep sensor completely flat and still for calibration...");
    delay(1000);
    mpu.calcOffsets(); // Calibrates both gyro and accelerometer
    Serial.println("Calibration complete!");
}

void loop() {
    mpu.update();

    if (millis() - prev_ms >= 50) {
        float pitch = mpu.getAngleX();
        float roll  = mpu.getAngleY();
        float yaw   = mpu.getAngleZ();

        Serial.print(pitch, 2);
        Serial.print(",");
        Serial.print(roll, 2);
        Serial.print(",");
        Serial.println(yaw, 2);

        prev_ms = millis();
    }
}