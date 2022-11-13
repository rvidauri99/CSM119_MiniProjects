#include <ArduinoBLE.h>
#include <Arduino_LSM6DS3.h>

BLEService IMUService("1101");

// BLEFloatCharacteristic AX("13012F01-F8C3-4F4A-A8F4-15CD926DA146", BLERead | BLENotify);
BLEFloatCharacteristic AX("2101", BLERead | BLENotify);
// BLEFloatCharacteristic AY("2102", BLERead | BLENotify);
// BLEFloatCharacteristic AZ("2103", BLERead | BLENotify);
// BLEFloatCharacteristic GX("2104", BLERead | BLENotify);
// BLEFloatCharacteristic GY("2105", BLERead | BLENotify);
// BLEFloatCharacteristic GZ("2106", BLERead | BLENotify);

float ax, ay, az, gx, gy, gz;

void setup() {
  // LED to indicate if connected(on) or disconnected(off)
  pinMode(LED_BUILTIN, OUTPUT);

  Serial.begin(9600);
  while (!Serial);

  // begin initialization
  if (!BLE.begin()) {
    Serial.println("starting Bluetooth® Low Energy failed!");
    while (1);
  }
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
  
  Serial.print("Accelerometer sample rate = ");
  Serial.print(IMU.accelerationSampleRate());
  Serial.println("Hz");

  // set advertised local name and service UUID:
  BLE.setDeviceName("Rod Nano 33 IoT");
  BLE.setLocalName("Rod Nano 33 IoT");
  BLE.setAdvertisedService(IMUService);

  // add the characteristic to the service
  IMUService.addCharacteristic(AX);
  // IMUService.addCharacteristic(AY);
  // IMUService.addCharacteristic(AZ);
  // IMUService.addCharacteristic(GX);
  // IMUService.addCharacteristic(GY);
  // IMUService.addCharacteristic(GZ);

  // add service
  BLE.addService(IMUService);

  // write initial values
  AX.writeValue(0);
  // AY.writeValue(0);
  // AZ.writeValue(0);
  // GX.writeValue(0);
  // GY.writeValue(0);
  // GZ.writeValue(0);

  // start advertising
  BLE.advertise();

  Serial.println("BLE IMU Peripheral");
}


void loop() {
  // listen for BLE peripherals to connect:
  BLEDevice central = BLE.central();

  // if a central is connected to peripheral:
  if (central) {
    // turn led on
    digitalWrite(LED_BUILTIN, HIGH);

    Serial.print("Connected to central: ");
    // print the central's MAC address:
    Serial.println(central.address());

    // while the central is still connected to peripheral:
    while (central.connected()) {
      if (IMU.accelerationAvailable()) {
        IMU.readAcceleration(ax, ay, az);
        AX.writeValue(ax);
        // AY.writeValue(ay);
        // AZ.writeValue(az);
      }
      // if (IMU.gyroscopeAvailable()) {
      //   IMU.readGyroscope(gx, gy, gz);
      //   GX.writeValue(gx);
      //   GY.writeValue(gy);
      //   GZ.writeValue(gz);
      // }
    }

    // when the central disconnects, print it out:
    digitalWrite(LED_BUILTIN, LOW);
    Serial.print(F("Disconnected from central: "));
    Serial.println(central.address());
  }
}