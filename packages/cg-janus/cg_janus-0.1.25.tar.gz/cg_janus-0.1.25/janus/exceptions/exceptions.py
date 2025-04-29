class JanusError(Exception):
    def __init__(self, message: str = ""):
        super(JanusError, self).__init__()
        self.message = message


class ParseJSONError(JanusError):
    """Raises an error in case of an error when parsing a JSON file."""


class WorkflowNotSupportedError(JanusError):
    """Raises an error in case a request for an unsupported workflow was made."""
