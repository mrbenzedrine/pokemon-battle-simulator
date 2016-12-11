from all_pokemon_info import allPokemon


class Pokemon:
    # Pokemon main attributes

    # Stats (HP, Attack, Defense etc)
    # Moves (Tackle, Water Gun etc)
    # Type (Water, Fire, Grass etc)
    # Level

    def __init__(self, name):

        self.name = name
        self.type = allPokemon[name]['type']
        self.stats = allPokemon[name]['stats']
        self.moves = allPokemon[name]['moves']
        self.level = 5
        # self.current_xp = 0
        # self.level = self.load_last_state()['level']
        # self.current_xp = self.load_last_state()['current_xp']
        # self.level_up_xp = 50

    def say_name(self):
        print(self.name)

    def show_stats(self):
        print(self.stats)

    def show_moves(self):
        print(self.moves)

    def show_level(self):
        print(self.level)
