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
        self.status_condition = None
        self.sleep_turn_info = None

    def use_physical_move(self, move, damage_multiplier, enemy_pokemon):

        move_damage = round(move['Power'] * damage_multiplier / 5)
        enemy_pokemon.subtract_hp(move_damage)

    def subtract_hp(self, damage):

        if(self.stats['HP'][0] - damage < 0):
            self.stats['HP'][0] = 0
        else:
            self.stats['HP'][0] -= damage

    def use_stat_move(self, move, stat_multiplier, enemy_pokemon):

        enemy_pokemon.multiply_stat(move['AffectedStat'], stat_multiplier)

    def multiply_stat(self, stat, stat_multiplier):

        self.stats_multipliers[stat] = stat_multiplier * self.stats_multipliers[stat]

    def reset_stat_multipliers(self):

        for stat in self.stats_multipliers:
            self.stats_multipliers[stat] = 1

    def apply_status_condition(self, status_condition, stat_change):

        self.status_condition = status_condition

        if stat_change != None:
            for stat in stat_change:
                self.multiply_stat(stat, stat_change[stat])

    def inflict_burn_or_poison_damage(self):

        damage = round(1/8 * self.stats['HP'][1])
        self.subtract_hp(damage)

    def remove_status_condition(self, stat_change):

        if stat_change is not None:
            # Undo stat change that was caused by the status condition that is inflicted
            for stat in stat_change:
                multiplier_reciprocal = 1/stat_change[stat]
                self.stats_multipliers[stat] *= multiplier_reciprocal

        self.status_condition = None

    def set_sleep_turn_info(self, sleep_turn_info):

        self.sleep_turn_info = sleep_turn_info
