"""
This file contains all issues that can be shown to the user for a field
"""

from abc import ABC
from dataclasses import dataclass
import time

ISSUE_LIFETIME = 20

@dataclass
class FieldIssue(ABC):
    def __init__(self, message):
        self.message = message
        self.revive()
    
    def revive(self):
        self.alive_until = time.time() + ISSUE_LIFETIME


class ErrorIssue(FieldIssue):
    def to_json(self):
        return {
            "type": "error",
            "message": self.message
        }

class WarningIssue(FieldIssue):
    def to_json(self):
        return {
            "type": "warning",
            "message": self.message
        }

# class 