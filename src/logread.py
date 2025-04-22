#!/usr/bin/env python3
import sys
import argparse

# setup parser
parser = argparse.ArgumentParser(
    prog="logread",
    description="queries the gallery log"
)

# custom error system thing
class invalidParser(argparse.ArgumentParser):
    def error(self, message):
        print("invalid")
        sys.exit(255)

def parse_args():
    p = invalidParser(prog="logread", add_help=False)

    # auth token arg
    p.add_argument("-K", dest="token", required=True, help="auth token")

    # only one mode (S, R, T) can be active at once
    modes = p.add_mutually_exclusive_group(required=True)
    modes.add_argument("-S", 
                       action="store_true", 
                       dest="print_state", 
                       help="print current gallery state"
                       )
    modes.add_argument("-R",
                       action="store_true", 
                       dest="list_rooms",
                       help="list gallery rooms"
                       )
    modes.add_argument("-T",
                       action="store_true", 
                       dest="total_time",
                       help="show total time spent in gallery"
                       )
    
    # only guest or employe mode at once
    person = p.add_mutually_exclusive_group()
    person.add_argument("-E",
                        dest="employee", 
                        help="employee name"
                        )
    person.add_argument("-G", 
                        dest="guest",
                        help="guest name"
                        )
    
    # log arg
    p.add_argument("log", 
                   help="path to log file"
                   )
    
    # TODO: make an actual help message here
    p.add_argument("-h",
                   "--help", 
                   action="help",
                   help="show this help msg and exit")

    args = p.parse_args()
    
    if (args.list_rooms or args.total_time) and not (args.employee or args.guest):
        p.error("-S cant be used with -G or -E")

    return args

# TODO: Add check for the log's token

class Person:
    def __init__(self, name, employee, ):
        pass

'''
dictionary of every person who's ever been to the gallery;
{name: employee?, current room (can be none), [rooms visited], time spent overall, previous action timestamp}

COULD USE CLASS LIKE STRUCT INSTEAD

dictionary of rooms??

main read function: reads through log entries 
for each person:
    
    haven't been seen before:
        set new dictionary entry (name, employee?, current room = NONE, rooms visited = [], overall time = 0, prev action = )

    check if already in gallery (room is not none): 
        yes: total time += (current timestamp - previous timestamp)
        
    previous timestamp = current timestamp
    
    are they leaving?
        current room = new room OR None





'''