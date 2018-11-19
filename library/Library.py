import pyaudio
import wave
import curses
import sys
from os import listdir
from os.path import isfile, join

"""
Library class, pulls songs from ./media directory and puts them in a list

"""
class Library:

    """
    Initialization method, searches through the media directory and adds songs to the list
    """
    def __init__(self):
        self.library = []
        self.library = [f for f in listdir("./media/") if isfile(join("./media/", f))]

    """
    Getter method to return the current library
    """
    def getLibrary(self):
        return self.library


