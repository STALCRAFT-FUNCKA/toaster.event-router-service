"""Submodule "events".
File:
    events.py

About:
    This file contains the implementation of the Event
    class, which is used to represent various types
    of events.The Event class provides methods for
    initializing an event, representing it as a string,
    and converting it to a dictionary.

Author:
    Oidaho (Ruslan Bashinsky)
    oidahomain@gmail.com
"""


class Event(object):
    """Class for representing an event.

    Attributes:
        event_id (str): Unique identifier for the event.
        event_type (str): Type of the event.
    """

    event_id: str = None
    event_type: str = None

    def __init__(self, raw_event: dict, event_type: str = "Undefined"):
        """Initializes an Event object.

        Args:
            raw_event (dict): Raw dictionary containing event data.
            event_type (str): Type of the event (default is "Undefined").
        """

        self.event_type = event_type
        self.event_id = raw_event.get("event_id")

    def __str__(self):
        string = (
            "<-- "
            f"class Event <type: {self.event_type}>"
            " | "
            f"<id: {self.event_id}>"
            " -->"
        )
        return string

    def __repr__(self):
        return self.__str__()

    def as_dict(self):
        """Converts the Event object to a dictionary.

        Description:
            This method is used only for logging
            purposes and is not intended for future
            data exchange.

        Returns:
            dict: Dictionary representation.
        """

        dict_repr = {}
        for attr, value in vars(self).items():
            if not callable(value) and not attr.startswith("__"):
                if isinstance(value, tuple):
                    dict_repr[attr] = value._asdict()
                else:
                    dict_repr[attr] = value

        return dict_repr
