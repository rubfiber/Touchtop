#include "MPU9250.h"

MPU9250 mpu;

void setup() {
    Serial.begin(115200);
    Wire.begin();
    delay(2000);

    // Initialize sensor at default I2C address 0x68
    if (!mpu.setup(0x68)) {
        while (1) {
            Serial.println("MPU connection failed. Check your wiring!");
            delay(5000);
        }
    }

    // Improve yaw stability on slower boards like the Arduino Uno
    mpu.setFilterIterations(10);

    // --- CALIBRATION ---
    Serial.println("Keep sensor completely flat and still for Accel/Gyro calibration...");
    delay(3000);
    mpu.calibrateAccelGyro();

    Serial.println("Wave sensor in a figure-8 motion for Magnetometer calibration...");
    delay(2000);
    mpu.calibrateMag();

    Serial.println("Calibration complete!");
}

void loop() {
    // Update the sensor as fast as possible
    if (mpu.update()) {
        // Print every 50ms (20 times per second) without blocking the filter

        float yaw = mpu.getYaw();
        float pitch = mpu.getPitch();
        float roll = mpu.getRoll();
        static uint32_t prev_ms = millis();
        if (millis() > prev_ms + 50) {
            Serial.print(pitch, 2);
            Serial.print(",");
            Serial.print(roll, 2);
            Serial.print(",");
            Serial.println(yaw, 2);

            prev_ms = millis();
        }
    }
}
