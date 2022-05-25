class ParhlException(Exception):
    def __init__(self, message, line=None):
        super().__init__(message)
        self.line = line
    
    def __str__(self):
        return (f"{super().__str__()} at line: {self.line}"
            if self.line else super().__str__())
    
    def with_line(self, line):
        self.line = line
        return self