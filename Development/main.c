#define _GNU_SOURCE
#include <stdio.h>
#include <unistd.h>
#include <pthread.h>
#include <sched.h>
#include <string.h>
#include <stdlib.h>
#include "sqlite3.h"
#include <mosquitto.h>
#include <wiringPi.h>

#define NUM_THREADS 2
#define MAIN_CORE 2
#define SECONDARY_CORE 3
#define CEILING     3

struct UserData
{
   int id;
   char username[15];
   char password[15];
   int capsules[6];
   int auth;
};

struct taskargs 
{
    int priority;
    int core;
    struct timespec period;
    struct timespec first_arrival;
};

// User data is defined globally so that callbacks can access it
struct UserData user;
int state=0, exist=0;                     // aux variable for state changing
pthread_mutex_t mutex;  // Global mutex
// MQTT variables
struct mosquitto *mosq = NULL;

int set_task_priority_FIFO(int priority)
{
    struct sched_param params;
    int retval;
    
    /* Set thread priority under SHED_FIFO scheduler. */
    params.sched_priority = priority;
    retval = pthread_setschedparam(pthread_self(), SCHED_FIFO, &params);
    
    return retval; /* 0 if success. */
}

int set_task_affinity(int core)
{
    cpu_set_t cores_mask;
    int retval;
    
    /* Set affinity of thread to cores -> {0, 1, 2, 3} */
    CPU_ZERO(&cores_mask);
    CPU_SET(core, &cores_mask);
    retval = pthread_setaffinity_np(pthread_self(), sizeof(cores_mask), &cores_mask);
    
    return retval; /* 0 if success. */
}


struct timespec next_arrival(struct timespec previous, struct timespec period)
{
    struct timespec next;
    
    next.tv_sec     = previous.tv_sec + period.tv_sec;   /* Seconds */
    next.tv_nsec    = previous.tv_nsec + period.tv_nsec; /* Nanoseconds*/
    
    if(next.tv_nsec > 1000000000L) {
        /* Nanoseconds can not exceed one second. */
        next.tv_nsec -= 1000000000L;
        next.tv_sec++;
    }
    
    return next;
}

/** SQLite3 Callback
 * Return records from DB */
static int callback(void *data, int argc, char **argv, char **azColName)
{
   int i;

   exist = 1;
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
         printf("UserID: %d\n", user.id);
         state = 1;
      }

      if(strcmp(message->topic,"login/pin") == 0)
      {
         printf("%s %s\n", message->topic, message->payload);
         if (strcmp(message->payload,user.password) == 0)
         {
            state = 3;     // password matches
            printf("Matched!\n");
         }else{
            state = 2;     // password don't match
            printf("Not matched...\n");
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

/* ************************************* */

void * t1_task(void *arg) 
{
    struct taskargs * targs;
    struct timespec next, period;

    char *host = "localhost";
    int port = 1883;
    int keepalive = 60;
    bool clean_session = true;
    
    /* Read parameters from arg. */
    targs = (struct taskargs *) arg;
    period  = targs->period;
    next    = targs->first_arrival;
    
    /* Set affinity of thread to cores -> {0, 1, 2, 3} */
    set_task_affinity(targs->core);
    
    /* Set thread priority under SHED_FIFO scheduler. */
    set_task_priority_FIFO(targs->priority);

    while(1){
        /* Sleep until the 'next' arrival time. */
        clock_nanosleep(CLOCK_MONOTONIC, TIMER_ABSTIME, &next, 0);
        
        mosquitto_lib_init();
        mosq = mosquitto_new(NULL, clean_session, NULL);
        if(!mosq){
           fprintf(stderr, "Error: Out of memory.\n");
           return 1;
        }

        // MQTT Callbacks
        mosquitto_connect_callback_set(mosq, my_connect_callback);
        mosquitto_message_callback_set(mosq, my_message_callback);

        if(mosquitto_connect(mosq, host, port, keepalive)){
           fprintf(stderr, "Unable to connect.\n");
           return 1;
        }

        mosquitto_loop_forever(mosq, -1, 1);

        /* Set timer for next activation. */
        next = next_arrival(next, period);
    }
    mosquitto_destroy(mosq);
    mosquitto_lib_cleanup();
}

int main(int argc, char* argv[]) 
{
   // DB variables
   sqlite3 *db;
   char *zErrMsg = 0, buf[35], buf_2[6], *sql;
   char* s = "temp";
   int rc, r;
   const char* data = "Callback function called";
   user.auth=0;                    // System starts with no one authenticated

   system("sudo rm /var/lib/mosquitto/mosquitto.db");

   struct taskargs targs[NUM_THREADS];
   pthread_t threads[NUM_THREADS];
   struct timespec first_arrival;
   pthread_mutexattr_t mutex_attr;

   /* Create and initialize the mutex. */
   pthread_mutexattr_init(&mutex_attr);
   pthread_mutexattr_setprotocol(&mutex_attr, PTHREAD_PRIO_PROTECT);
   pthread_mutexattr_setprioceiling(&mutex_attr, CEILING);
   pthread_mutex_init(&mutex, &mutex_attr);
   pthread_mutexattr_destroy(&mutex_attr);

   /* Set the time instant when tasks will arrive (in less than 2 seconds). */
   clock_gettime(CLOCK_MONOTONIC, &first_arrival);
   first_arrival.tv_nsec   += 100000000;
   first_arrival.tv_sec    += first_arrival.tv_nsec / 1000000000L;
   first_arrival.tv_nsec   = first_arrival.tv_nsec % 1000000000L;
   
   /* HIGH priority task. */
   // T1: Button Control
   targs[0].priority       = 4;
   targs[0].core           = MAIN_CORE;
   targs[0].period.tv_sec  = 0;
   targs[0].period.tv_nsec = 100000000; /* 20 ms */
   targs[0].first_arrival  = first_arrival;

   pthread_create(&threads[0], NULL, t1_task, &targs[0]);

   if (wiringPiSetup() == -1)
   {
      // when initialize wiring failed,print messageto screen
      printf("setup wiringPi failed !");
      return 1;
   }

   while(1)
   {
      switch(state)
      {
         case 1:     // received an ID from interface and verifies it. Returns to interface -1 if exists else -2
            state = 0; // reset state
            /* Open database */
            rc = sqlite3_open("teste.db", &db);

            if( rc ) 
            {
               fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
               //return(0);
            } else {
               fprintf(stderr, "Opened database successfully\n");
            }
                           
            /* Create SQL statement */
            sql = "SELECT * from login WHERE id=";
            snprintf(buf, 40, "%s%d", sql, user.id);

            /* Execute SQL statement */
            rc = sqlite3_exec(db, buf, callback, (void*)data, &zErrMsg);
            
            if( rc != SQLITE_OK ) 
            {
               fprintf(stderr, "SQL error: %s\n", zErrMsg);
               sqlite3_free(zErrMsg); // free memory
            }else{
               sqlite3_close(db);     // close db connection
            }
            delay(500);
            if(exist == 1)
            {
	            char* s = "-1";
	            snprintf(buf_2,10,"%s",s);
               mosquitto_publish(mosq, NULL, "login/idReply", 2, buf_2, 0, true);  // -1 tells python that id exists
               exist = 0;
            } else if (exist == 0){
	            char* s = "-2";
	            snprintf(buf_2,10,"%s",s);
               mosquitto_publish(mosq, NULL, "login/idReply", 2, buf_2, 0, true); // -2 tells python user id was not found
            }
            break;
         
         case 2:
            mosquitto_publish(mosq, NULL, "login/pinReply", 2, "-2", 0, true);   // -1 tells python that password didn't match
            state = 0;
            break;

         case 3:
            mosquitto_publish(mosq, NULL, "login/pinReply", 2, "-1", 0, true);   // -1 tells python that id exists

            // TODO motor code
            break;
      }
   }

   pthread_mutex_destroy(&mutex);
   return 0;
}
