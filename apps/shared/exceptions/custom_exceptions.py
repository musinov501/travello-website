class CustomException(Exception):
    def __init__(self, message_key: str, context: dict = None):
        self.message_key = message_key
        self.context = context or {}
        # Set the standard exception message
        super().__init__(f"{message_key} | Context: {self.context}")
