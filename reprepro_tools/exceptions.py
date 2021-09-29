

class RepreproNotInstalledError(Exception):
    """Exception raised when reprepro is not installed"""

    def __init__(self, message="Reprepro is either not installed or we couldn't locate reprepro path Please ensure reprepro is installed"):
        self.message = message
        super().__init__(message)


class RepreproExecutionError(Exception):
    """Exception raised when en error occurred during reprepro call"""
