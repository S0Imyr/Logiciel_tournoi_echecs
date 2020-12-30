import views.input


class Menu:
    def __init__(self, list_of_entries, list_of_entry_messages):
        self.list_of_entries = list_of_entries
        self.list_of_entry_messages = list_of_entry_messages

    def prompt_menu(self):
        number = 1
        for entry in range(len(self.list_of_entries)):
            self.list_of_entries[entry] = input(f"{number}."+self.list_of_entry_messages[entry])
            number += 1
