class ExternalAPIError(Exception):
    """Exception raised for errors in the external API call.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Error occurred with the external API"):
        self.message = message
        super().__init__(self.message)
