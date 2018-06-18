import random
from type_chart import typeChart
from status_effects import status_effects_stat_changes
from status_effects import types_and_corresponding_status_conditions

class Fight:

    def __init__(self, user_pokemon, enemy_pokemon, round_number):

        self.user_pokemon = user_pokemon
        self.enemy_pokemon = enemy_pokemon
        self.round_number = round_number

    def fight(self, user_move, enemy_move):

        # Check Speed stats to see who moves first
        # (Won't be Speed stat alone that determines this,
        # but for now it'll do)

        opponent_moves_first = self.who_moves_first()

        self.perform_one_round(opponent_moves_first, user_move, enemy_move)

    def choose_move(self, pokemon):

        while True:
            print('\nWhat move do you choose?')

            for move in pokemon.moves:
                print(move)
            print('\n')
            print('Or use \'Back\' to go back to the menu')
            choice = input()

            if choice in pokemon.moves:
                chosen_option = pokemon.moves[choice]
                break
            elif choice == 'Back':
                chosen_option = choice
                break
            else:
                print('That choice doesn\'t exist, please select a valid choice')

        return chosen_option

    def who_moves_first(self):

        user_speed = round(self.user_pokemon.stats['Speed'] * self.user_pokemon.stats_multipliers['Speed'])
        enemy_speed = round(self.enemy_pokemon.stats['Speed'] * self.enemy_pokemon.stats_multipliers['Speed'])

        if user_speed >= enemy_speed:
            opponent_moves_first = False
        else:
            opponent_moves_first = True

        return opponent_moves_first

    def perform_one_round(self, opponent_moves_first, user_move, enemy_move):

        if opponent_moves_first:
            first_pokemon = self.enemy_pokemon
            first_pokemon_move = enemy_move
            second_pokemon = self.user_pokemon
            second_pokemon_move = user_move
        else:
            first_pokemon = self.user_pokemon
            first_pokemon_move = user_move
            second_pokemon = self.enemy_pokemon
            second_pokemon_move = enemy_move

        relevant_status_effects = ['Paralyzed', 'Frozen', 'Sleep']
        is_first_able_to_move = True
        is_second_able_to_move = True

        if first_pokemon.status_condition in relevant_status_effects:
            is_first_able_to_move = self.check_if_status_inflicted_pokemon_can_move(first_pokemon)

        if is_first_able_to_move:
            self.execute_move(first_pokemon, second_pokemon, first_pokemon_move)

        if second_pokemon.stats['HP'][0] == 0:
            return
        else:
            if second_pokemon.status_condition in relevant_status_effects:
                is_second_able_to_move = self.check_if_status_inflicted_pokemon_can_move(second_pokemon)

            if is_second_able_to_move:
                self.execute_move(second_pokemon, first_pokemon, second_pokemon_move)

    def check_if_status_inflicted_pokemon_can_move(self, attacking_pokemon):

        status_effect_probability_function = {
            'Paralyzed': self.paralyzed_status_effect_roll,
            'Frozen': self.frozen_status_effect_roll,
            'Sleep' : self.check_if_pokemon_should_wake
        }.get(attacking_pokemon.status_condition, None)

        if attacking_pokemon.status_condition is not 'Sleep':
            is_able_to_move = status_effect_probability_function()
        else:
            is_able_to_move = status_effect_probability_function(attacking_pokemon.sleep_turn_info)

        if is_able_to_move:
            self.remove_pokemon_status_condition(attacking_pokemon)
        else:
            print("%s is unable to move due to its %s status!" % (attacking_pokemon.name, attacking_pokemon.status_condition))

        return is_able_to_move

    def remove_pokemon_status_condition(self, pokemon):

        if pokemon.status_condition is 'Frozen':

            # Pokemon then thaws

            print("%s thawed out!" % pokemon.name)

        elif pokemon.status_condition is 'Sleep':

            # Pokemon wakes up

            pokemon.set_sleep_turn_info(None)
            print("%s woke up!" % pokemon.name)

        pokemon.remove_status_condition(status_effects_stat_changes[pokemon.status_condition])

    def execute_move(self, attacking_pokemon, defending_pokemon, attacking_pokemon_move):

        move_execution_function = {
            'Damage': self.execute_damage_move,
            'Stat': self.execute_stat_move,
            'StatusCondition': self.execute_status_condition_move
        }.get(attacking_pokemon_move['Category'], None)

        if move_execution_function is not None:
            does_move_hit = self.move_accuracy_roll(attacking_pokemon_move)
            if does_move_hit:
                move_execution_function(attacking_pokemon, defending_pokemon, attacking_pokemon_move)
            else:
                print("%s\'s move %s missed!" % (attacking_pokemon.name, attacking_pokemon_move['Name']))
        else:
            print("Error in the choosing of a move execution function")

    def execute_damage_move(self, attacking_pokemon, defending_pokemon, attacking_pokemon_move):

        move_type_check_result = self.move_type_check(attacking_pokemon_move['Type'], defending_pokemon)
        damage_multiplier = move_type_check_result[0]
        effectiveness_message = move_type_check_result[1]

        stat_multiplier = attacking_pokemon.stats_multipliers[attacking_pokemon_move['DependentStat']]

        attacking_pokemon.use_damage_move(attacking_pokemon_move, damage_multiplier * stat_multiplier, defending_pokemon)

        print('%s used %s!' % (attacking_pokemon.name, attacking_pokemon_move['Name']))
        if effectiveness_message is not None:
            print(effectiveness_message)

        is_status_effect_inflicted = False # set a default value of False

        if defending_pokemon.status_condition is None and attacking_pokemon_move['statusConditionInfliction'] is not 'Nothing':
            if attacking_pokemon_move['statusConditionInfliction'] is 'Possible':
                if 'alternativeStatusCondition' in attacking_pokemon_move:
                    potential_status_effect = attacking_pokemon_move['alternativeStatusCondition']
                else:
                    potential_status_effect = types_and_corresponding_status_conditions.get(attacking_pokemon_move['Type'], None)

                is_status_effect_inflicted = self.status_effect_probability_roll()

            elif attacking_pokemon_move['statusConditionInfliction'] is 'Guaranteed':
                is_status_effect_inflicted = True
                potential_status_effect = types_and_corresponding_status_conditions.get(attacking_pokemon_move['Type'], None)

        if is_status_effect_inflicted:
            defending_pokemon.apply_status_condition(potential_status_effect, status_effects_stat_changes[potential_status_effect])
            print("%s has been %s!" % (defending_pokemon.name, potential_status_effect))

    def execute_stat_move(self, attacking_pokemon, defending_pokemon, attacking_pokemon_move):

        move_type_check_result = self.move_type_check(attacking_pokemon_move['Type'], defending_pokemon)
        damage_multiplier = move_type_check_result[0]
        effectiveness_message = move_type_check_result[1]

        if attacking_pokemon_move['doesAffectUser']:
            target_pokemon = attacking_pokemon
        else:
            target_pokemon = defending_pokemon

        print('%s used %s!' % (attacking_pokemon.name, attacking_pokemon_move['Name']))
        if damage_multiplier != 0:
            attacking_pokemon.use_stat_move(attacking_pokemon_move, attacking_pokemon_move['Power'], target_pokemon)
            affected_stat = attacking_pokemon_move['AffectedStat']
            stat_with_applied_multiplier = round(target_pokemon.stats[affected_stat] * target_pokemon.stats_multipliers[affected_stat])
            print('%s\'s %s stat is now %s' % (target_pokemon.name, affected_stat, stat_with_applied_multiplier))
        else:
            print(effectiveness_message)

    def move_type_check(self, attacking_move_type, defending_pokemon):

        damage_multiplier = typeChart[attacking_move_type][defending_pokemon.type]

        # Check what message, if any, should be returned regarding the effectiveness of the
        # type of the move against the type of the defending pokemon

        effectiveness_message = None

        if damage_multiplier == 0:
            effectiveness_message = 'It doesn\'t affect ' + defending_pokemon.name + '...'
        elif damage_multiplier == 1/2:
            effectiveness_message = 'It\'s not very effective...'
        elif damage_multiplier == 2:
            effectiveness_message = 'It\'s super effective!'

        return (damage_multiplier, effectiveness_message)

    def status_effect_probability_roll(self):

        random_int = random.randint(0, 5)

        if random_int == 0:
            is_status_effect_inflicted = True
        else:
            is_status_effect_inflicted = False

        return is_status_effect_inflicted

    def paralyzed_status_effect_roll(self):

        random_int = random.randint(0,3)

        if random_int == 0:
            is_able_to_move = False
        else:
            is_able_to_move = True

        return is_able_to_move

    def frozen_status_effect_roll(self):

        random_int = random.randint(0,4)

        if random_int == 0:
            is_thawed = True
        else:
            is_thawed = False

        return is_thawed

    def sleep_status_effect_roll(self):

        # The number of turns a pokemon sleeps for is determined beforehand,
        # so roll to see how many turns the pokemon should sleep for

        turns_to_sleep = random.randint(1,5)

        return turns_to_sleep

    def check_if_pokemon_should_wake(self, turn_info):

        if self.round_number == turn_info[0] + turn_info[1]:
            should_pokemon_wake = True
        else:
            should_pokemon_wake = False

        return should_pokemon_wake

    def execute_status_condition_move(self, attacking_pokemon, defending_pokemon, attacking_pokemon_move):

        status_condition_to_inflict = types_and_corresponding_status_conditions.get(attacking_pokemon_move['Type'], None)

        if defending_pokemon.status_condition is None:
            defending_pokemon.apply_status_condition(status_condition_to_inflict, status_effects_stat_changes[status_condition_to_inflict])
            print("%s has been %s!" % (defending_pokemon.name, status_condition_to_inflict))
        else:
            print("%s is already %s so cannot be %s!" % (defending_pokemon.name, defending_pokemon.status_condition, status_condition_to_inflict))

    def move_accuracy_roll(self, move):

        random_value = random.random()

        if random_value <= move['Accuracy']:
            does_move_hit = True
        else:
            does_move_hit = False

        return does_move_hit
