class ArmCtrlError(Exception):
    """
    Base class for exceptions in the RosBoard library.
    """

class SerialPortError(ArmCtrlError):
    """
    Exception raised for errors related to the serial port.

    :param message: Explanation of the error.
    :type message: str
    """

    def __init__(self, message="Serial port error"):
        self.message = message
        super().__init__(self.message)

class DataTransmissionError(ArmCtrlError):
    """
    Exception raised for errors during data transmission.

    :param message: Explanation of the error.
    :type message: str
    """

    def __init__(self, message="Data transmission error"):
        self.message = message
        super().__init__(self.message)

class ThreadCreationError(ArmCtrlError):
    """
    Exception raised when creating threads for data reception fails.

    :param message: Explanation of the error.
    :type message: str
    """

    def __init__(self, message="Thread creation error"):
        self.message = message
        super().__init__(self.message)

class DataProcessError(ArmCtrlError):
    """
    Exception raised when creating threads for data reception fails.

    :param message: Explanation of the error.
    :type message: str
    """

    def __init__(self, message="Thread creation error"):
        self.message = message
        super().__init__(self.message)
