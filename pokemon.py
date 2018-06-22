from copy import deepcopy
from all_pokemon_info import allPokemon

class Pokemon:

    def __init__(self, name):

        self.name = name
        self.type = allPokemon[name]['type']
        self.stats = deepcopy(allPokemon[name]['stats'])
        self.moves = deepcopy(allPokemon[name]['moves'])
        self.level = 5
        self.stats_multipliers = {
            'Attack': 1,
            'SpecialAttack': 1,
            'Defense': 1,
            'SpecialDefense': 1,
            'Speed': 1
        }
        self.stat_offsets = {
            'Attack': 0,
            'SpecialAttack': 0,
            'Defense': 0,
            'SpecialDefense': 0,
            'Speed': 0
        }
        self.status_condition = None
        self.sleep_turn_info = None

    def use_damage_move(self, move, damage_multiplier, enemy_pokemon):

        move_damage = round(move['Power'] * damage_multiplier / 5)
        enemy_pokemon.subtract_hp(move_damage)

    def subtract_hp(self, damage):

        if self.stats['HP'][0] - damage < 0:
            self.stats['HP'][0] = 0
        else:
            self.stats['HP'][0] -= damage

    def use_stat_move(self, move, stat_offset, enemy_pokemon):

        is_stat_within_lower_bound = enemy_pokemon.stat_offsets[move['AffectedStat']] + stat_offset >= -6
        is_stat_within_higher_bound = enemy_pokemon.stat_offsets[move['AffectedStat']] + stat_offset <= 6

        if is_stat_within_lower_bound and is_stat_within_higher_bound:
            enemy_pokemon.offset_stat(move['AffectedStat'], stat_offset)
        elif not is_stat_within_lower_bound:
            print("%s\'s %s stat cannot go any lower!" % (enemy_pokemon.name, move['AffectedStat']))
        elif not is_stat_within_higher_bound:
            print("%s\'s %s stat cannot go any higher!" % (enemy_pokemon.name, move['AffectedStat']))

    def multiply_stat(self, stat, stat_multiplier):
        self.stats_multipliers[stat] = stat_multiplier * self.stats_multipliers[stat]

    def reset_stat_multipliers(self):

        for stat in self.stats_multipliers:
            self.stats_multipliers[stat] = 1

    def offset_stat(self, stat, stat_offset):

        self.stat_offsets[stat] += stat_offset

    def reset_stat_offsets(self):

        for stat in self.stat_offsets:
            self.stat_offsets[stat] = 0

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
