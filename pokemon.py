from all_pokemon_info import allPokemon

class Pokemon:

    def __init__(self, name):

        self.name = name
        self.type = allPokemon[name]['type']
        self.stats = allPokemon[name]['stats']
        self.moves = allPokemon[name]['moves']
        self.level = 5

    def say_name(self):
        print(self.name)

    def show_stats(self):
        print(self.stats)

    def show_moves(self):
        print(self.moves)

    def show_level(self):
        print(self.level)
