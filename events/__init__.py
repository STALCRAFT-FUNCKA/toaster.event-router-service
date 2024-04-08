"""Module "events".
About:
    Provides custom VK events. Convenient form,
    additional data, nothing superfluous.
"""

from .base import BaseEvent
from .event import MessageEvent, ButtonEvent

__all__ = ("BaseEvent", "MessageEvent", "ButtonEvent")
