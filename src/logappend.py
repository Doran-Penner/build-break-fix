#!/usr/bin/env python3
import sys
import argparse
import shlex
import re
from loadsave import load_all, save_all, Event

#takes a list of arguments to parse
#returns either a dictionary of parsed arguments (single command)
#or a list of dictionaries of parsed arguments (batch command)
def parse_args(args = None):
    # setup parser
    parser = argparse.ArgumentParser(
        prog="logread",
        description="queries the gallery log"
    )
    # Batch mode has highest precedence
    parser.add_argument('-B', dest='batch_file', metavar='file',
                        help='Specifies a batch file of commands')
    
    # Arguments for single command mode
    single_command_group = parser.add_argument_group('single command arguments')
    single_command_group.add_argument('-T', dest='timestamp', metavar='timestamp',
                                     help='Time the event is recorded (non-negative integer)')
    single_command_group.add_argument('-K', dest='token', metavar='token',
                                     help='Token used to authenticate the log (alphanumeric)')
    
    # Person specification (mutually exclusive)
    person_group = single_command_group.add_mutually_exclusive_group()
    person_group.add_argument('-E', dest='employee', metavar='employee-name',
                             help='Name of employee (alphabetic, no spaces)')
    person_group.add_argument('-G', dest='guest', metavar='guest-name',
                             help='Name of guest (alphabetic, no spaces)')
    
     # Action specification (mutually exclusive)
    action_group = single_command_group.add_mutually_exclusive_group()
    action_group.add_argument('-A', dest='action', action='store_const', const='arrive',
                             help='Specify arrival event')
    action_group.add_argument('-L', dest='action', action='store_const', const='leave',
                             help='Specify departure event')
    
    # Room specification
    single_command_group.add_argument('-R', dest='room', metavar='room-id',
                                    help='Room ID corresponding to an event (non-negative integer)')
    # Log file path specification
    single_command_group.add_argument('log', nargs='?', default=None,
                                    help='Path to the file containing the event log')
    
    parsed_args = parser.parse_args(args)

    # batch mode
    if parsed_args.batch_file is not None:
        try:
            with open(parsed_args.batch_file, 'r') as f:
                batch_commands = [line.strip() for line in f if line.strip()]
        except IOError:
            print("invalid", file=sys.stdout)
            sys.exit(255)
        
        batch_results = []
        for cmd in batch_commands:
            try:
                # Recursively parse each command in the batch file
                cmd_args = shlex.split(cmd)
                result = parse_args(cmd_args)
                batch_results.append(result)
            except SystemExit:
                # Continue processing other commands even if one fails
                continue
        
        return batch_results

    # Validate single command mode
    errors = []
    
    # Required arguments
    if not parsed_args.timestamp:
        errors.append("Missing required argument: -T timestamp")
    if not parsed_args.token:
        errors.append("Missing required argument: -K token")
    if not parsed_args.log:
        errors.append("Missing required argument: log file path")
    
    # Person specification
    if not (parsed_args.employee or parsed_args.guest):
        errors.append("Must specify either -E employee or -G guest")
    
    # Action specification
    if not parsed_args.action:
        errors.append("Must specify either -A (arrive) or -L (leave)")
    
    # Validate formats
    if parsed_args.timestamp and not re.fullmatch(r'0|[1-9]\d*', parsed_args.timestamp):
        errors.append("Timestamp must be a non-negative integer")
    elif parsed_args.timestamp:
        try:
            ts = int(parsed_args.timestamp)
            if ts < 0 or ts > 1073741823:
                errors.append("Timestamp must be between 0 and 1,073,741,823")
        except ValueError:
            errors.append("Timestamp must be a valid integer")
    
    if parsed_args.token and not re.fullmatch(r'[a-zA-Z0-9]+', parsed_args.token):
        errors.append("Token must be alphanumeric")
    
    if parsed_args.employee and not re.fullmatch(r'[a-zA-Z]+', parsed_args.employee):
        errors.append("Employee name must contain only alphabetic characters")
    
    if parsed_args.guest and not re.fullmatch(r'[a-zA-Z]+', parsed_args.guest):
        errors.append("Guest name must contain only alphabetic characters")
    
    if parsed_args.room:
        if not re.fullmatch(r'0|[1-9]\d*', parsed_args.room):
            errors.append("Room ID must be a non-negative integer")
        else:
            try:
                room_id = int(parsed_args.room)
                if room_id < 0 or room_id > 1073741823:
                    errors.append("Room ID must be between 0 and 1,073,741,823")
            except ValueError:
                errors.append("Room ID must be a valid integer")
    
    if errors:
        print("invalid", file=sys.stdout)
        sys.exit(255)

    result = {
        'time': int(parsed_args.timestamp),
        'key': parsed_args.token,
        'employee': True if parsed_args.employee else False,
        'name': parsed_args.employee or parsed_args.guest,
        'arrive': True if parsed_args.action=='arrive' else False,
        'room': int(parsed_args.room) if parsed_args.room else None,
        'log': parsed_args.log
    }
    
    return result



def append(new_event, log_file, key):
    #get the log and check against the new event
    log, salt = load_all(key, log_file)

    if len(log) != 0:
        #trying to add an event before/at the same time as an existing one
        if log[-1].time >= new_event.time:
            raise ValueError("Invalid")
            
        #check the most recent event including the person in the new event
        for event in reversed(log):
                #checking against each event including the person in new_event
                if event.name == new_event.name and event.employee == new_event.employee:
                    #checks that new arrivals aren't already there
                    if new_event.arrive == True and event.arrive != False:
                        if new_event.room != None and event.room == None:
                            break
                        else:
                            raise ValueError("Invalid")
                    #check that they haven't already left
                    if event.arrive==False and event.arrive==False:
                        raise ValueError("Invalid")
                    #need to fix this so that leaving follows arrival in the same room, and the arriving follows departing a room
                break

    #add the new event now that we know it's valid
    log.append(new_event)
    save_all(log, salt, key, log_file)

def main():
    try:
        args = sys.argv[1:]
        parsed_args = parse_args(args)

        #batch file case
        if isinstance(parsed_args, list):
            for result in parsed_args:
                new_event = Event(result['time'], result['employee'], result['name'], result['arrive'], result['room'])
                append(new_event, result['log'], result['key'])
                

        else:
            new_event = Event(parsed_args['time'], parsed_args['employee'], parsed_args['name'], parsed_args['arrive'], parsed_args['room'])
            append(new_event, parsed_args['log'], parsed_args['key'])


    except:
        print("invalid")
        sys.exit(255)


if __name__ == '__main__':
    main()
