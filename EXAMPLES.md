Examples
========
Consider the following 4 invocations of `logappend`:

    $ ./logappend -T 1 -K secret -A -E Fred log1
    $ ./logappend -T 2 -K secret -A -G Jill log1
    $ ./logappend -T 3 -K secret -A -E Fred -R 1 log1
    $ ./logappend -T 4 -K secret -A -G Jill -R 1 log1

These commands have used the secret token (which in this example is creatively set to *secret*) to append 4 events to the log `log1`, recording the arrival of *Fred* and *Jill* in room *1* of the gallery. Suppose `log1` didn't exist prior to the first `logappend` command, and so the first command initialized `log1`. Then, if `logread` is then used to print the state of the gallery, the following should be printed: 

    $ ./logread -K secret -S log1
    Fred
    Jill
    1: Fred,Jill

If we continue using `log1` and record some movements, we can then use `logread` to get a list of the rooms entered by Fred.

    ./logappend -T 5 -K secret -L -E Fred -R 1 log1
    ./logappend -T 6 -K secret -A -E Fred -R 2 log1
    ./logappend -T 7 -K secret -L -E Fred -R 2 log1
    ./logappend -T 8 -K secret -A -E Fred -R 3 log1
    ./logappend -T 9 -K secret -L -E Fred -R 3 log1
    ./logappend -T 10 -K secret -A -E Fred -R 1 log1
    ./logread -K secret -R -E Fred log1
    1,2,3,1 

We can also use `logappend` in batch mode. Here is an example using the batch mode on a fresh log, `log2`:

    $ cat batch
    -K secret -T 0 -A -E John log2
    -K secret -T 1 -A -R 0 -E John log2
    -K secret -T 2 -A -G James log2
    -K secret -T 3 -A -R 0 -G James log2
    $ ./logappend -B batch
    invalid
    invalid
    $ echo $?
    0
    $ ./logread -K secret -S log2
    James
    0:James
    $ echo $?
    0

We can see from the output that the first two lines of the batch file are invalid:  the first line fails because 0 is an invalid time, and then the second line fails because John is not in the gallery. However, the 3rd and 4th are applied successfully, putting James in a room with room ID 0. (`$?` evaluates to the exit status of the previous command, so `echo $?` echoes the exit status of the previous command. Handy!)

If we ran the same batch file except with fixed time arguments (on a fresh log, `log3`), we should instead see the following: 

    $ cat batch
    -K secret -T 1 -A -E John log3
    -K secret -T 2 -A -R 0 -E John log3
    -K secret -T 3 -A -G James log3
    -K secret -T 4 -A -R 0 -G James log3
    $ ./logappend -B batch
    $ echo $?
    0
    $ ./logread -K secret -S log3
    John
    James
    0:James,John
    $ echo $?
    0
