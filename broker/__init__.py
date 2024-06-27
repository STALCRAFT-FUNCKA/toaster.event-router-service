"""Module "producer".
About:
    Provides a producer client that sends data
    to rabbit.queue-broker service. Using JSON.
"""

from .publisher import Publisher
from .subscriber import Subscriber


__all__ = ("Publisher", "Subscriber")
