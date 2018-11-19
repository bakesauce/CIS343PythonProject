import curses
import curses.textpad
from exception.CLI_Audio_Exception import CLI_Audio_File_Exception
from exception.CLI_Audio_Exception import CLI_Audio_Screen_Size_Exception
import sys

"""
FrontEnd class
Authors: Mark Baker and Ira Woodring
Date: 11/19/2018
Class: CIS 343
Project: Python Project

"""
class FrontEnd:

    """
    initialization function
    """
    def __init__(self, player, library):
        self.player = player
        #self.player.play(sys.argv[1])
        self.library = library

        #Try/Except block to check if there is an error when opening the main menu screen
        try:
            curses.wrapper(self.menu)
        except: raise CLI_Audio_Screen_Size_Exception({"message:""Screen size not big enough!"})

    """
    Main menu, controls the functionality of the program. Displays options to the user for what they can do within the program
    """
    def menu(self, args):
        self.stdscr = curses.initscr()
        self.stdscr.border()
        self.stdscr.addstr(0,0, "cli-audio",curses.A_REVERSE)
        self.stdscr.addstr(5,10, "c - Change current song")
        self.stdscr.addstr(6,10, "p - Play/Pause")
        self.stdscr.addstr(7,10, "l - Library")
        self.stdscr.addstr(8,10, "r - Restart Current Song")
        self.stdscr.addstr(10,10, "ESC - Quit")
        self.updateSong()
        self.stdscr.refresh()
        while True:
            c = self.stdscr.getch()
            if c == 27:
                self.quit()
            elif c == ord('p'):
                self.player.pause()
            elif c == ord('c'):
                self.changeSong()
                self.updateSong()
                self.stdscr.touchwin()
                self.stdscr.refresh()
            #Option to restart the current song
            elif c == ord('r'):
                self.restartSong()
                self.updateSong()
                self.stdscr.touchwin()
                self.stdscr.refresh()
            #Option to display a new window with the library consisting of songs in the media directory
            elif c == ord('l'):
                self.library_menu()
                self.updateSong()
                self.stdscr.touchwin()
                self.stdscr.refresh()
    
    def updateSong(self):
        self.stdscr.addstr(15,10, "                                        ")
        self.stdscr.addstr(15,10, "Now playing: " + self.player.getCurrentSong())

    def changeSong(self):
        changeWindow = curses.newwin(5, 40, 5, 50)
        changeWindow.border()
        changeWindow.addstr(0,0, "What is the file path?", curses.A_REVERSE)
        self.stdscr.refresh()
        curses.echo()
        path = changeWindow.getstr(1,1, 30)
        curses.noecho()
        del changeWindow
        self.stdscr.touchwin()
        self.stdscr.refresh()
        print (self.player.getCurrentSong())

        #Since the program doesnt start with a song playing, code to make sure that if a song isnt playing
        #the player.stop function isnt called (would crash the program)
        if self.player.getCurrentSong() != "Nothing playing.":
            self.player.stop()
        print(type(path))

        #Try/except block to make sure the song the user is requesting actually exists, otherwise throws an error
        try:
            self.player.play(path.decode(encoding="utf-8"))
        except: raise CLI_Audio_File_Exception("File not found!")

    """
    Library menu function. Creates the window and lists the songs in the media directory. Allows the user
    to select a song to play based on the number next to it, or to press q to quit.
    """
    def library_menu(self):
        libraryMenu = curses.newwin(40, 50, 10, 50)
        libraryMenu.border()
        libraryMenu.addstr(0,0, "Song Library, enter the number associated with the song to play", curses.A_REVERSE)
        libraryMenu.addstr(3,0, "Press q to quit to main menu")

        #gets the library list from the library class
        current_library = self.library.getLibrary()

        #lists the songs in the window
        for i in range (len(current_library)):
            libraryMenu.addstr(i+6, 10, str(i) + " " + current_library[i])

        self.stdscr.refresh()
        curses.echo()
        path = libraryMenu.getstr(4,1,30)
        curses.noecho()

        #If the user press q, close the window and go back to main menu without altering what song is/is not playing
        if path.decode(encoding="utf-8") == 'q':
            del libraryMenu
            self.stdscr.touchwin()
            self.stdscr.refresh()
        #Otherwise, stop the current song and play the song the user requests
        else:
            if self.player.getCurrentSong() != "Nothing playing.":
                self.player.stop()

            del libraryMenu
            self.stdscr.touchwin()
            self.stdscr.refresh()
            self.player.play("./media/" + current_library[int(path)])

    """
    Restart method to restart whatever song is currently playing
    """
    def restartSong(self):
        current_song = self.player.getCurrentSong()
        self.player.stop()
        self.player.play(current_song)

    def quit(self):
        self.player.stop()
        exit()
