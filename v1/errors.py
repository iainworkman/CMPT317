class Error(Exception):
    """
    Base Exception class
    """
    
class StateError(Error):
    def __init__(self, message = None):
        if message is None:
            self.message = 'Error detected in state of class'
        else:
            self.message = message
            
            
class ArgumentError(Error):
    def __init__(self, message = None):
        if message is None:
            self.message = 'Error, bad argument provided'
        else:
            self.message = message