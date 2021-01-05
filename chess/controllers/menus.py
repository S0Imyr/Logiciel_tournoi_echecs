
class MenuEntry:
    """
    Entrée d'un menu, lie une option à son gestionnaire
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
    Menu liant clés, entrées, gestionnaire
    """
    def __init__(self):
        self._entries = {}
        self._autokey = 1

    def __contains__(self, choice):
        return str(choice) in self._entries

    def __getitem__(self, choice):
        return self._entries[choice]

    def add(self, key, option, handler):
        """
        permet d'ajouter des entrées, avec leur gestionnaire
        :param key: si égal à "auto", la clé va prendre la suite après 1 ou
        les clés précédemment "auto"
        :param option: option affiché à choisir
        :param handler: gestionnaire de l'option associée
        :return: None
        """
        if key == "auto":
            key = str(self._autokey)
            self._autokey += 1

        self._entries[str(key)] = MenuEntry(option, handler)

    def items(self):
        """
        permet d'accéder clé, entrées sans passer par _entries
        :return: clé, entrées du menu
        """
        return self._entries.items()


if __name__ == "__main__":
    menu = Menu()
    menu.add("auto", "Lancer un tournoi", lambda: None)
    menu.add("auto", "Ajouter un nouveau joueur", lambda: None)
    menu.add("q", "Quitter", lambda: None)
    print(menu.items())
    print(menu['1'])
