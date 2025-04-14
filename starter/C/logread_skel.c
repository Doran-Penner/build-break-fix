#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <arpa/inet.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/queue.h>

#include <openssl/ssl.h>
#include <openssl/bio.h>
#include <openssl/err.h>
#include <openssl/rand.h>

#include "data.h"

int verbose = 0;

void print_records(Record *records, unsigned int num_records) {
  unsigned int i;

  for(i = 0; i < num_records; i++) {
    dump_record(&records[i]);
    printf("----------------\n");
  }

  return;
}

struct Person {
  //TODO put some other stuff here
  SLIST_ENTRY(Person)   link;
};

SLIST_HEAD(slisthead, Person);


void leave_action(struct slisthead *head, char *name, GuestType T, int roomPresent, unsigned long room) {
  //is this person already in the gallery? 
  struct Person *current; 
  int           found = 0; 
  
  //TODO Code this
  
  return;
}

void arrive_action(struct slisthead *head, char *name, GuestType T, int roomPresent, unsigned long room) {
  //is this person already in the gallery? 
  struct Person *current; 
  int           found = 0; 
 
  //TODO Code this

  return;
}

void execute_records(Record *Rarr, unsigned int num_records, struct slisthead *head) {
  int           i;
  int           firstTime = 0;
  unsigned long Seconds; 

  //TODO Code this

  return;
}

void print_time(Record *Rarr, unsigned int num_records, char *name) {
  unsigned long     start_time;
  unsigned long     elapsed_time = 0;
  int               st = 0;
  int               i;

  //TODO code this

  return;
}

void print_rooms(Record *Rarr, unsigned int num_records, char *name) {
  int           first = 1;
  int           make_newl = 0;
  int           i;


  //TODO code this

  return;
}

void print_summary(Record *Rarr, unsigned int num_records) {
  struct slisthead state = SLIST_HEAD_INITIALIZER(state);
  struct Person *current; 
  int           found = 0; 
  int           first = 1;

  execute_records(Rarr, num_records, &state);

  //TODO Code this

  return;
}

int main(int argc, char *argv[]) {
  int   opt,len;
  char  *logpath = NULL;
  
  //TODO Code this

  while ((opt = getopt(argc, argv, "K:PSRE:G:VT")) != -1) {
    switch(opt) {
      case 'T':
        break;

      case 'V':
        break;

      case 'P':
        break;

      case 'K':
        break;

      case 'S':
        break;

      case 'R':
        break;

      case 'E':

      case 'G':
        break;
    }
  }

  if(optind < argc) {
    logpath = argv[optind];
  }

}
