#include <Arduino.h>
#include <ESP32Servo.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <string.h>
#include <stdlib.h>

#define SERVO_SECTION 32
#define SERVO_DISPENSE 33
#define IRSENSOR 35
 
Servo sectionServo, dispenserServo;  // create servo object to control a servo
const char *ssid = "estudantes"; // name of your WiFi network
const char *password = "estudantes"; // password of the WiFi network
const char *ID = "Controller"; // Device Name
static unsigned long ts = 0; // TimeStamp in ms
WiFiClient wclient; // WiFi Client Object
PubSubClient client(wclient); // Setup MQTT client
IPAddress broker(192, 168, 1, 94); // SET the IP address of the MQTT broker
const char* mqtt_username = "user"; //type your mosquitto mqtt username
const char* mqtt_password = "lol123"; //type your mosquitto mqtt password
short int state = 0; // initial state
int selection[6] = {0,0,0,0,0,0}; // espresso, latte, mocha, cappucino, black, ristretto
char *espresso; 
char *latte;
char *mocha;
char *cappuccino;
char *black;
char *ristretto;
int irSensorDeviceDriver();
void dispenseCapsule();

//////////////////////////////////////////////////////////////////////////////
// Handle incomming messages from the broker
//////////////////////////////////////////////////////////////////////////////
void MQTT_callback(char* topic, byte* payload, unsigned int length) {
  String response;
  for (int i = 0; i < length; i++) {
    response += (char)payload[i];
  }
  Serial.print("MQTT Message Arrived [");
  Serial.print(topic);
  Serial.print("] ");
  Serial.println(response);
  if(strcmp(topic,"capsules/dispenser")==0)
  {
    // Receives "0 0 1 0 1 0 " for example
    selection[0] = (response.substring(0,1)).toInt();
    selection[1] = (response.substring(2,3)).toInt();
    selection[2] = (response.substring(4,5)).toInt();
    selection[3] = (response.substring(6,7)).toInt();
    selection[4] = (response.substring(8,9)).toInt();
    selection[5] = (response.substring(10,11)).toInt();
    state = 1;
  }
  if(strcmp(topic,"capsules/stockReq")==0) state = 2;
}

void reconnect2MQTTbroker() {
  while (!client.connected()) { // Loop until we're reconnected
    Serial.print("Connecting to MQTT broker…\n");
    if (client.connect(ID, mqtt_username, mqtt_password)) { // Attempt to connect
      client.subscribe("capsules/dispenser");
      client.subscribe("capsules/stockReq");
      Serial.println("Connected!");
      Serial.println("Topics subscribed.");
    }
    else {
      Serial.println("Try again in 5 seconds");
      delay(5000); // Wait 5 seconds before retrying
    }
  }
}
 
void setup() {
  Serial.begin(115200);
  sectionServo.setPeriodHertz(50); 
  sectionServo.attach(SERVO_SECTION);
  dispenserServo.setPeriodHertz(50); 
  dispenserServo.attach(SERVO_DISPENSE);

  // Connect to WiFi
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password); // Connects to WiFi Network
  while (WiFi.status() != WL_CONNECTED) { // Waits for WiFi connection
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("ESP connected to WiFi with IP address: ");
  Serial.println(WiFi.localIP());
  ///////////////////////////////////////////////////////
  // Set MQTT Broker and Callback Function
  ///////////////////////////////////////////////////////
  client.setServer(broker, 1883); // Sets IP+PORT for the MQTT broker (PORT=1883)
  client.setCallback(MQTT_callback);     // Initialize the callback routine
  ts = millis(); // ts = TimeStamp
}
 
void loop() {
  int num = 0;
  int angle = 0;
  ///////////////////////////////////////////////////////
  // Reconnect to MQTT Server if connection is lost
  ///////////////////////////////////////////////////////
  if (!client.connected())
    reconnect2MQTTbroker();
  client.loop();

  switch (state)
  {
    case 1: // Dispense capsules and publish individually
      if (!client.connected())
        reconnect2MQTTbroker();
      client.publish("capsules/espresso",String(selection[0]).c_str());
      client.publish("capsules/latte",String(selection[1]).c_str());
      client.publish("capsules/mocha",String(selection[2]).c_str());
      client.publish("capsules/cappuccino",String(selection[3]).c_str());
      client.publish("capsules/black",String(selection[4]).c_str());
      client.publish("capsules/ristretto",String(selection[5]).c_str());

      for (int i = 0; i < 6; i++)
      {
        if (selection[i] != 0)        // if more than one then there is capsules chosen in section 'i'
        {
          angle = 15+30*i;            // calculate the angle for the pretended section
          sectionServo.write(angle);  // move o servo para a secção pretendida
          delay(1500);
          while (selection[i] != 0)     // ultil dispenses all the capsules chosen from a section
          {
            Serial.print(selection[i]);
            Serial.print(" ");
            dispenserServo.write(0);    // rotates to align with section
            delay(1000);
            dispenserServo.write(180);  // rotates do move capsule to exit
            delay(1000);  
            selection[i]--;
          }
        }
      }
      if (!client.connected())
        reconnect2MQTTbroker();
      client.publish("capsules/result","done");
      state = 0;
      break;

    case 2: //Stock request
      num = irSensorDeviceDriver();
      if (!client.connected())
        reconnect2MQTTbroker();
      client.publish("capsules/stock", String(num).c_str());
      state = 0;
      break;
    
    case 0: // do nothing
      break;
  }
}

/** Infrared Sensor device driver
 * Reads analog value and maps it to value between
   Input: nothing
   Output: Infrared sensor values
*/
int irSensorDeviceDriver() {
  int valorAnalog = analogRead(IRSENSOR);  // reads analog value of LDR sensor
  int values = map(valorAnalog, 300, 3300, 5, 0); // maps analog value into PWM
  return values;
}