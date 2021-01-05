class MenuEntry:
    """
    Entrée d'un menu, lie une option à son gestionnaire
    """
    def __init__(self, option, handler):
        self.option = option
        self.handler = handler

    def __repr__(self):
        return f"MenuEntry({self.option}, {self.handler})"

    def __str__(self):                  # Affichage print
        return str(self.option)


class Menu:
    """
    Menu liant clés et entrées
    """
    def __init__(self):
        self._entries = {}
        self._autokey = 1

    def __contains__(self, choice):
        return str(choice) in self._entries

    def __getitem__(self, choice):
        return self._entries[choice]

    def add(self, key, option, handler):
        if key == "auto":
            key = str(self._autokey)
            self._autokey += 1

        self._entries[str(key)] = MenuEntry(option, handler)

    def items(self):
        return self._entries.items()


if __name__ == "__main__":
    menu = Menu()
    menu.add("auto", "Lancer un tournoi", lambda: None)
    menu.add("auto", "Ajouter un nouveau joueur", lambda: None)
    menu.add("q", "Quitter", lambda: None)
    print(menu._entries)
    print(menu._entries['1'])