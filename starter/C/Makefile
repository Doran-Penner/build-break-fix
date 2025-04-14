all: logappend logread

CFLAGS=-g 
LFLAGS=-lssl -lcrypto 

logappend: logappend_skel.o data_skel.o
	$(CC) -g -o logappend logappend_skel.o data_skel.o $(LFLAGS)

logread: logread_skel.o data_skel.o
	$(CC) $(CFLAGS) -o logread logread_skel.o data_skel.o $(LFLAGS)

logappend_skel.o: logappend_skel.c
	$(CC) $(CFLAGS) -c -o logappend_skel.o logappend_skel.c

logread_skel.o: logread_skel.c
	$(CC) $(CFLAGS) -c -o logread_skel.o logread_skel.c

data_skel.o: data_skel.c
	$(CC) $(CFLAGS) -c -o data_skel.o data_skel.c

clean:
	rm -f *.o
	rm -rf logappend_skel logread_skel
