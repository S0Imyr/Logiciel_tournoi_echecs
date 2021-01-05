
class MenuView:
    """
    Vue d'un menu, avec son affichage et la demande de la clé
    """
    def __init__(self, menu):
        self.menu = menu

    def _display_menu(self):
        for key, option in self.menu.items():
            print(f"{key}. {option}")

    def get_user_choice(self):
        while True:
            # Afficher le menu
            self._display_menu()
            # demander le choix
            choice = input("Choissisez une option en inscrivant le nombre associé, ou q pour quitter")
            # Vérifier que le choix existe
            if choice in self.menu:
                return self.menu[choice]


if __name__ == "__main__":
    from chess.controllers.menus import Menu
    menutest = Menu()
    menutest.add("auto", "Lancer un tournoi", lambda: None)
    menutest.add("auto", "Ajouter un nouveau joueur", lambda: None)
    menutest.add("q", "Quitter", lambda: None)
    test = MenuView(menutest)
    test._display_menu()
    test.get_user_choice()
