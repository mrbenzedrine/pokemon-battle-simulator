from all_pokemon_info import allPokemon

class Pokemon:

    def __init__(self, name):

        self.name = name
        self.type = allPokemon[name]['type']
        self.stats = allPokemon[name]['stats']
        self.moves = allPokemon[name]['moves']
        self.level = 5
        self.stats_multipliers = {
            'Attack': 1,
            'SpecialAttack': 1,
            'Defense': 1,
            'SpecialDefense': 1,
            'Speed': 1
        }

    def use_physical_move(self, move, damage_multiplier, enemy_pokemon):

        move_damage = (move['Power'] * damage_multiplier) / 5
        enemy_pokemon.subtract_hp(move_damage)

    def subtract_hp(self, damage):

        if(self.stats['HP'][0] - damage < 0):
            self.stats['HP'][0] = 0
        else:
            self.stats['HP'][0] -= damage

    def use_status_move(self, move, stat_multiplier, enemy_pokemon):

        enemy_pokemon.multiply_stat(move['AffectedStat'], stat_multiplier)

    def multiply_stat(self, stat, stat_multiplier):

        self.stats_multipliers[stat] = stat_multiplier * self.stats_multipliers[stat]
