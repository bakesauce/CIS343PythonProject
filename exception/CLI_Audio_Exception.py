
"""
Exception classes
"""
class CLI_Audio_Exception(Exception):

    def __init__(self, message):
        super().__init__(message)



class CLI_Audio_File_Exception(CLI_Audio_Exception):

    def __init__(self, message):

        super().__init__(message)

class CLI_Audio_Screen_Size_Exception(CLI_Audio_Exception):

    def __init__(self, message):

        super().__init__(message)