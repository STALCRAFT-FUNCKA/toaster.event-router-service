"""Module "events"."""


class Event(object):
    """DOCSTRING"""

    event_id: str = None
    event_type: str = None

    def __init__(self, raw_event: dict, event_type: str = "Undefined"):
        self.event_type = event_type
        self.event_id = raw_event.get("event_id")

    def __str__(self):
        return f"<-- class Event <type: {self.event_type}> | <id: {self.event_id}> -->"

    def __repr__(self):
        return self.__str__()

    def as_dict(self):
        dict_repr = {}
        for attr, value in vars(self).items():
            if not callable(value) and not attr.startswith("__"):
                if isinstance(value, tuple):
                    dict_repr[attr] = value._asdict()
                    # Inside unpacking for reply and forward messages
                    if attr == "mesage":
                        reply = dict_repr[attr]["reply"]
                        forward = dict_repr[attr]["forward"]
                        dict_repr[attr]["reply"] = reply.as_dict() if reply else None
                        dict_repr[attr]["forward"] = [fwd.as_dict() for fwd in forward]
                else:
                    dict_repr[attr] = value

        return dict_repr
