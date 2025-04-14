#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <arpa/inet.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <wordexp.h>

#include <openssl/ssl.h>
#include <openssl/bio.h>
#include <openssl/err.h>
#include <openssl/rand.h>

#include "data.h"

typedef struct _CmdLineResult {
  //TODO probably put more things here
  int     good;
} CmdLineResult;

int do_batch(char *);

CmdLineResult parse_cmdline(int argc, char *argv[], int is_batch) {
  CmdLineResult R = { 0 };
  int opt,r = -1;

  R.good = -1;

  //argument data
  Record  Rec = {0};

  //pick up the switches
  while ((opt = getopt(argc, argv, "T:K:E:G:ALR:B:")) != -1) {
    int     br = 0;
    size_t  len;
    
    //TODO Code this
    
    switch(opt) {
      case 'B':
        //batch file
	break;  

      case 'T':
	//timestamp
        break;

      case 'K':
	//secret token
        break;

      case 'A':
        //arrival
        break; 
      
      case 'L':
        //departure
        break;

      case 'E':
        //employee name
        break;

      case 'G':
        //guest name
	break;

      case 'R':
        //room ID
        break;

      default:
        //unknown option, leave
        break;
    }

    if(br) {
      break;
    }
  }
  
  //TODO Code this
  
  //pick up the positional argument for log path
  if(optind < argc) {
    logpath = argv[optind];
  }
  
  //TODO do stuff
  if(batchfile != NULL) {
    R.good = do_batch(batchfile);
  } else {
    //TODO do stuff
    R.good = 0;
  }

  return R;
}

int do_batch(char *filepath) {
  //read in data from filepath
  char  *data = NULL;
  int   fd = open(filepath, O_RDONLY);

  if(fd <= 0) {
    return -1;
  }

  //TODO Code this

  close(fd);

  return 0;
}

int main(int argc, char *argv[]) {
  int r;
  CmdLineResult R;
  
  R = parse_cmdline(argc, argv, 0);

  if(R.good == 0) {
    Buffer  B = read_from_path(/** stuff **/);

    //TODO do things here.
    
    //write the result back out to the file
    write_to_path(/** stuff **/);
  }

  return r;
}
