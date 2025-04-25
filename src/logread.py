#!/usr/bin/env python3
import sys
import argparse
from loadsave import *

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
    
    # only guest or employee mode at once
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

def load_log(token, log_file):
    try:
        # use load_all to get log
        log, _ = load_all(token, log_file)
        return log
    # if load all 
    except:
        print("integrity violation")
        sys.exit(255)


def print_state(log):
    # dict of people and their current room
    employees = {}
    guests = {}

    for event in log:

        '''
        line 1: comma-separated list of employees currently in the gallery.
        line 2: comma-separated list of guests currently in the gallery
        remaining lines: room-by-room information indicating which guest or employee is in which room:
            - room ID, printed as a decimal integer
            - ':'
            - ' '
            - comma-separated list of guests and employees
        '''

        # when someones entering a room: 
        if event.arrive:
            if event.employee:
                employees[event.name] = event.room
            else:
                guests[event.name] = event.room
        
        # when someones leaving a room:
        else:
            # if theyre leaving the gallery
            if event.room is None: 
                if event.employee:
                    employees.pop(event.name, None)
                else:
                    guests.pop(event.name, None)
            else: 
                # if theyre leaving a room (to gallery)
                if event.employee:
                    employees[event.name] = None
                else:
                    guests[event.name] = None

    # print comma separated employee / guest lists
    if employees:
        print(",".join(sorted(employees.keys())))
    if guests:
        print(",".join(sorted(guests.keys())))



    # update rooms and their occupants
    rooms_dict = {}

    for name, room in guests.items(): 
        # for each person and their room, if they're in one:
        if room is not None: 
            rooms_dict.setdefault(room, []).append(name)
        
    for name, room in employees.items(): 
        # for each person and their room, if they're in one:
        if room is not None: 
            rooms_dict.setdefault(room, []).append(name)

    for room in sorted(rooms_dict):
        occupants = sorted(rooms_dict[room])
        s = ",".join(occupants)
        print(f"{room}: {s}")
    
def list_rooms(log, is_employee, name):
    visited_rooms = []
    seen = False
    
    for event in log:
        # if we find the person and they're arriving in a room:
        if event.employee == is_employee and event.name == name:
            seen = True
            if event.arrive and event.room is not None:
                visited_rooms.append(str(event.room))
        
        # only print if the person has visited some room
    if seen:
        print(",".join(visited_rooms))

def total_time(log, is_employee, name):
    total = 0
    entry_time = None
    seen = False
    if log:
        last_time = log[-1].time
    else:
        0
    
    for event in log:
        if event.employee == is_employee and event.name == name:
            seen = True
            # if the person is entering the building:
            if event.arrive and event.room is None:
                entry_time = event.time

            # if the person is leaving: 
            elif not event.arrive and event.room is None and entry_time is not None:
                total += event.time - entry_time
                entry = None
    
    # only print if the person has been present in the building at some point
    if seen:
        # if they are currently in the building, add the remaining time 
        if entry is not None:
            total += last_time - entry_time
        print(total)


def main():
    args = parse_args()
    log = load_log(args.token, args.log)

    name = args.employee or args.guest
    is_employee = bool(args.employee)

    if args.print_state:
        print_state(log)

    elif args.list_rooms:
        list_rooms(log, is_employee, name)

    elif args.total_time:
        total_time(log, is_employee, name)
    


if __name__ == '__main__':
    main()