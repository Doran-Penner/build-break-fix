#ifndef _BUFFR_H
#define _BUFFR_H

typedef struct _Buffer {
  unsigned char *Buf;
  unsigned long Length;
} Buffer;

typedef enum _GuestType {
  Employee,
  Guest
} GuestType;

typedef enum _ActionType {
  Arrived,
  Left
} ActionType;

typedef struct _Record {
  //put some things here
} Record;

Buffer read_from_path(char *path, unsigned char *key);
void write_to_path(char *path, Buffer *B, unsigned char *key);
Buffer concat_buffs(Buffer *A, Buffer *B);
Buffer print_record(Record *R);
void dump_record(Record *R);

int read_records_from_path(char *path, unsigned char *key, Record **, unsigned int *);

#endif
