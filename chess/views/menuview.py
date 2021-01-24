# -*- coding: utf-8 -*-


"""
This module takes care of the menus display.
"""


class MenuView:
    """ Handle the display of a given menu by asking to prompt the corresponding key. """
    def __init__(self, menu):
        self.menu = menu

    def _display_menu(self):
        """ Displays the key and option of the dictionary stored in menu."""
        for key, option in self.menu.items():
            print(f"{key}. {option}")

    def get_user_choice(self):
        """ Asks to input the key corresponding to the desired option. """
        while True:
            self._display_menu()
            choice = input("\nChoissisez une option en inscrivant "
                           "le nombre associé, ou q pour quitter: \n")
            if choice in self.menu:
                return self.menu[choice]
