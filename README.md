### Smart Coffee Capsules Dispenser 
CS-LAB group 4

João Passos 1210646 & Pedro Vicente 1180558

---
# Project Specification:
This project is about the design and development of a ***Smart Coffee Capsules Dispenser***. 
The machine shall be able to give coffee capsules selected by the user. When a user identifies himself with his card, the system shall show the variety of coffee flavours available.

![System Design](/wiki/assets/Desenho.jpeg)

The system consists of 4 subsystems: authentication, storage, dispenser, and user interface. 
- The authentication subsystem is responsible for the entire process of verification and validation of the user's identity, from card reading to processing and communication with the server that will give the authorization. If a card is not recognize or a password is not valid, the subsystem shall notify the user.
- The storage subsystem shall detect and count the number of capsules present on a section. In addition to dispensing all capsules in a section, the subsystem should be able to activate a low stock state. It is also expected to report to the operator when this state is activated or when the storage is replenished.
- The dispenser subsystem shall give the pretended capsules to the user and update the user usage. When request by an admin, all capsules shall be dispensed. When a capsule is chosen, if the storage can't be rotated or the capsule doesn't reach the user the subsystem shall call the operator.
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
7. Dispenser subsystem rotates de sections for the pretended choice;
8. The coffee capsule is dispensed.

---
## Systems Architecture

![Architecture](/wiki/assets/DiagramaBlocos.png)

