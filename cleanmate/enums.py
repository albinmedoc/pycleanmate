"""Common enums for Cleanmate vacuum."""
from enum import Enum

class WorkMode(Enum):
    """The cleaning intensity."""
    Intensive = 7
    Standard = 1
    Silent = 9

class WorkState(Enum):
    """The work state."""
    Cleaning = 1
    Paused = 2
    Charging = 5
    Problem = 9

class MopMode(Enum):
    """The mop intensity."""
    High = 20
    Medium = 40
    Low = 60
