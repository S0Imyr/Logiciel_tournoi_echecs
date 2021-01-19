
class MenuEntry:
    """
    Entry of a menu, which links an option and its handler
    """
    def __init__(self, option, handler):
        self.option = option
        self.handler = handler

    def __repr__(self):
        return f"MenuEntry({self.option}, {self.handler})"

    def __str__(self):
        return str(self.option)


class Menu:
    """
    Menu who handles the different entries
    """
    def __init__(self):
        self._entries = {}
        self._autokey = 1

    def __contains__(self, choice):
        return str(choice) in self._entries

    def __getitem__(self, choice):
        return self._entries[choice]

    def add(self, key, option, next_menu):
        """
        allows to add entries and their handler to the menu.
        :param key: if "auto", the key will take
        the first integer value available from 1.
        :param option: the displayed proposal.
        :param next_menu: the next menu given if the key is chosen.
        :return: None.
        """
        if key == "auto":
            key = str(self._autokey)
            self._autokey += 1

        self._entries[str(key)] = MenuEntry(option, next_menu)

    def items(self):
        """
        allows to get the key without using _entries.
        :return: the dictionary of keys and entries of the menu.
        """
        return self._entries.items()


if __name__ == "__main__":
    menu = Menu()
    menu.add("auto", "Lancer un tournoi", lambda: None)
    menu.add("auto", "Ajouter un nouveau joueur", lambda: None)
    menu.add("q", "Quitter", lambda: None)
    print(menu.items())
    print(menu['1'])
