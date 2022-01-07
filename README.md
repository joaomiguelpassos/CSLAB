### Smart Coffee Capsules Dispenser 
CS-LAB group 4

João Passos 1210646 & Pedro Vicente 1180558

---
# Project Specification:
This project is about the design and development of a ***Smart Coffee Capsules Dispenser***. 
The machine shall be able to give coffee capsules selected by the user. When a user identifies himself with his card, the system shall show the variety of coffee flavours available.

![System Design](/wiki/assets/Desenho.jpeg)

The system consists of 4 subsystems: authentication, storage, dispenser, and user interface. 
- The authentication subsystem is responsible for the entire process of verification and validation of the user's identity, from card reading to processing and communication with the server that will give the authorization. If a card is not recognized or a password is not valid, the subsystem shall notify the user.
- The storage subsystem shall detect and count the number of capsules present in ecach section. In addition to dispensing all capsules in a section, the subsystem should be able to activate a low stock state. It is also expected to report to the operator when this state is achived or when the storage is replenished.
- The dispenser subsystem shall give the pretended capsules to the user and update the user consumption. When requested by an admin, all capsules shall be dispensed. When a capsule is chosen, if the storage can't be rotated or the capsule doesn't reach the user the subsystem shall call the operator.
- The user interface is where the interaction with the user is made. All the information will be displayed and the user can interact with the system by tapping the screen making his choices.

---
## Technologies

- Apache
- MySQL
- RFID
- SMTP
- MQTT
- Raspberry Pi 4 Model B and accessories

---
## Conceptual Model

![Conceptual model](/wiki/assets/ModeloConceptual.png)

The system's operation mode is shown in the above figure. We considered a trouble-free use.

1. An NFC/RFID tag is presented to the reader;
2. The authentication subsystem identifies the user;
3. A virtual keyboard is displayed;
4. The user inserts his password;
5. Authentication subsystem queries the server about the user;
6. User makes his choice from the flavours shown;
7. Dispenser subsystem rotates the sections for the pretended choice;
8. The coffee capsule is dispensed.

---
## Systems Architecture

![Architecture](/wiki/assets/DiagramaBlocos.png)

The system materials and their functionality are described below:
- 2 Servo motors DC:
The DC servo motors are able to control the rotor's angular position very accuratly through a PWM signal input.
The first motor will be responsable to rotate the storage unit so that the flavour of the coffee capsule select by the user is aligned with the capsules dropping plataform.
The second motor will be responsable to rotate de dropping plataform that ensures the dispensing of only one coffee capsule in each iteraction.
- 1 Touch screen:
The touch screen will be the main device for the user to interact with the system. This device will be the main input and output feature of the system.
- 1 RFID tag
- 1 RFID sensor
The RFID sensor will be responsable for identifying the user's id from the chip tag
- Infrared sensors:
The Infrared sensors will be placed in each section of the storage system allowing the main system to know the number of coffee capsules in each section.
- 1 RaspberryPi 4 model B:
The Raspberrypi will be the microprocessor of the hole system and will be responsible of the dispenser system and to host the web server, the database and the MQTT server.
- Cables to connect the system sensors and actuators to the raspberrypi.
