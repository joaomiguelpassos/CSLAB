#define _GNU_SOURCE
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include "sqlite3.h"
#include <mosquitto.h>
#include <wiringPi.h>

struct UserData
{
	int id;
	char username[15];
	char password[15];
   int capsules[6];
   int auth;
};

// User data is defined globally so that callbacks can access it
struct UserData user;
int state=0;                     // aux variable for state changing

/** SQLite3 Callback
 * Return records from DB */
static int callback(void *data, int argc, char **argv, char **azColName)
{
   int i;
   //fprintf(stderr, "%s: ", (const char*)data);
   
   for(i = 0; i<argc; i++){
      user.id = atoi(argv[0]);
      strcpy(user.username,argv[1]);
      strcpy(user.password,argv[2]);
   }
   return 0;
}
/* ************************************* */

/* MQTT Subscribe Callback */
void my_message_callback(struct mosquitto *mosq, void *userdata, const struct mosquitto_message *message)
{
   if(message->payloadlen){
      if(strcmp(message->topic,"login/id") == 0)
      {

         printf("%s %s\n", message->topic, message->payload);
         user.id = atoi(message->payload);
         state = 1;
      }

      if(strcmp(message->topic,"login/pin") == 0)
      {
         printf("%s %s\n", message->topic, message->payload);
         if (strcmp(message->payload,user.password) == 0)
         {
            state = 3;     // password matches
         }else{
            state = 2;     // password don't match
         }
      }
   }else{
      printf("%s (null)\n", message->topic);
   }
   fflush(stdout);
}

void my_connect_callback(struct mosquitto *mosq, void *userdata, int result)
{
   int i;
   if(!result){
      /* Subscribe to broker information topics on successful connect. */
      mosquitto_subscribe(mosq, NULL, "login/id/#", 2);
      mosquitto_subscribe(mosq, NULL, "login/pin/#", 2);
   }else{
      fprintf(stderr, "MQTT Connection failed\n");
   }
}

void my_subscribe_callback(struct mosquitto *mosq, void *userdata, int mid, int qos_count, const int *granted_qos)
{
   int i;

   printf("Subscribed (mid: %d): %d", mid, granted_qos[0]);
   for(i=1; i<qos_count; i++){
      printf(", %d", granted_qos[i]);
   }
   printf("\n");
}

void my_log_callback(struct mosquitto *mosq, void *userdata, int level, const char *str)
{
   // Pring all log messages regardless of level.
   printf("%s\n", str);
}

/* ************************************* */

int main(int argc, char* argv[]) 
{
   // DB variables
   sqlite3 *db;
   char *zErrMsg = 0, buf[35], *sql;;
   int rc, r;
   const char* data = "Callback function called";

   // MQTT variables
   char *host = "52.13.116.147";    // MQTT HQ free broker
   int port = 1883;
   int keepalive = 60;
   bool clean_session = true;
   struct mosquitto *mosq = NULL;
   user.auth=0;                    // System starts with no one authenticated

   mosquitto_lib_init();
   mosq = mosquitto_new(NULL, clean_session, NULL);
   if(!mosq){
      fprintf(stderr, "Error: Out of memory.\n");
      return 1;
   }
   mosquitto_log_callback_set(mosq, my_log_callback);
   mosquitto_connect_callback_set(mosq, my_connect_callback);
   mosquitto_message_callback_set(mosq, my_message_callback);
   mosquitto_subscribe_callback_set(mosq, my_subscribe_callback);

   while(1)
   {
      switch(state)
      {
         case 1:  // an ID was detected on RFID reader
            state = 0; // reset state

            /* Open database */
            rc = sqlite3_open("test.db", &db);

            if( rc ) 
            {
               fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
               //return(0);
            } else {
               fprintf(stderr, "Opened database successfully\n");
            }
            /* Create SQL statement */
            sql = "SELECT * from login WHERE id=";
            snprintf(buf, 31, "%s%d", sql, user.id);

            /* Execute SQL statement */
            rc = sqlite3_exec(db, buf, callback, (void*)data, &zErrMsg);
            
            if( rc != SQLITE_OK ) 
            {
               fprintf(stderr, "SQL error: %s\n", zErrMsg);
               mosquitto_publish(mosq, NULL, "login/idReply", 2, "-1", 0, true); // -1 tells python user id was not found
		printf("Teste");
               sqlite3_free(zErrMsg); // free memory
            }else{
               mosquitto_publish(mosq, NULL, "login/idReply", 2, "0", 0, true);  // 0 tells python that id exists
               sqlite3_close(db);     // close db connection
            }
            break;

         case 2:  // password didn't match, tell python
            mosquitto_publish(mosq, NULL, "login/pin", 2, "0", 0, true);
            state = 0;
            break;

         case 3:  // password matches and capsule selection starts
            mosquitto_publish(mosq, NULL, "login/pin", 2, "0", 0, true);
            user.auth = 1; // user is authenticated
            
            // TO DO - capsule selection and dispenser

            if (wiringPiSetup() == -1)
            {
               // when initialize wiring failed,print messageto screen
               printf("setup wiringPi failed !");
               return 1;
            }

            r=fork();   // creates a different process for hosting MQTT API
            if(r == 0)
               mosquitto_loop_forever(mosq, -1, 1);
            break;

         case 0:
            // does nothing
            break;
      }
   }
   mosquitto_destroy(mosq);
   mosquitto_lib_cleanup();
   return 0;
}
