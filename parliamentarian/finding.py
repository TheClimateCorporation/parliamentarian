from typing import Any


class Finding:
    """Class for storing findings"""

    issue = ""
    detail = ""
    location: dict[str, Any] = {}
    severity = ""
    title = ""
    description = ""
    ignore_locations: dict[str, Any] = {}

    def __init__(self, issue, detail, location):
        self.issue = issue
        self.detail = detail
        self.location = location

    def __repr__(self):
        """Return a string for printing"""
        return "{} - {} - {}".format(self.issue, self.detail, self.location)
