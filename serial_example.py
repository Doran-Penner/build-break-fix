from typing import Optional
import pickle


class Event:
    def __init__(self, time, employee, name, arrive, room):
        # time the event happened
        self.time: int = time
        # if it's an employee (True) or a guest (False)
        self.employee: bool = employee
        # the person's name
        self.name: str = name
        # if they're arriving (True) or leaving (False)
        self.arrive: bool = arrive
        # the room, if None then they're entering/leaving the whole gallery
        self.room: Optional[int] = room

    # nicely-formatted printing
    def __str__(self):
        return (
            f"At time {self.time} "
            f"{'employee' if self.employee else 'guest'} "
            f"{self.name} "
            f"{'arrived in' if self.arrive else 'left'} "
            f"{f'room {self.room}' if self.room is not None else 'the gallery'}"
        )

    __repr__ = __str__


log = []
event = Event(1, True, "Bob", True, None)
another_event = Event(2, False, "Alice", True, 2)
log.append(event)
log.append(another_event)

log_binary = pickle.dumps(log)
log_str_again = pickle.loads(log_binary)
print(log_str_again)
