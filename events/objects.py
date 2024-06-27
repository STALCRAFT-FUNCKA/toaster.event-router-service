"""Module "events"."""

from __future__ import annotations
from typing import NamedTuple, List, Optional


# TODO: Think about "cmid" duplication
class Button(NamedTuple):
    cmid: int  # conversation message id
    beid: str  # button event(press) id
    payload: dict  # button payload


class Message(NamedTuple):
    cmid: int  # conversation message id
    text: str  # message text
    reply: Optional[Message]  # replied message
    forward: Optional[List[Message]]  # forwarded messages
    attachments: List[str]  # message attachments


class User(NamedTuple):
    uuid: int  # user unique id
    name: str  # full user name
    firstname: str  # first name
    surname: str  # surname
    nick: str  # tag/nick/url


class Peer(NamedTuple):
    bpid: int  # bot peer id
    cid: int  # chat id
    name: str  # peer name
