from fight import Fight
import party

class Battle():

    def __init__(self, user_party, enemy_party):

        self.user_party = user_party
        self.enemy_party = enemy_party
        self.round_number = 0

    def battle(self):

        while True:

            self.round_number += 1

            print('\n==================================')
            self.display_pokemon_info(self.user_party[0])
            self.display_pokemon_info(self.enemy_party[0])

            self.explore_menu_options()

            # Check if either pokemon has a burn or poison status effect before moving to another
            # turn

            check_burned_or_poisoned(self.user_party[0])
            check_burned_or_poisoned(self.enemy_party[0])

            # Now check if either party has run out of Pokemon

            if sum([pokemon.stats['HP'][0] for pokemon in self.user_party]) == 0 or sum([pokemon.stats['HP'][0] for pokemon in self.enemy_party]) == 0:
                break
            else:
                if self.user_party[0].stats['HP'][0] == 0:

                    print('Your %s has fainted!' % self.user_party[0].name)

                    # Now need to select another pokemon to send out
                    party.switch_out_pokemon(self.user_party, 'user')

                if self.enemy_party[0].stats['HP'][0] == 0:

                    print('Their %s has fainted!' % self.enemy_party[0].name)

                    # Opponent needs to send out another pokemon
                    party.switch_out_pokemon(self.enemy_party, 'enemy')

        if sum([pokemon.stats['HP'][0] for pokemon in self.user_party]) == 0:
            print('Sorry, you lost...')
        else:
            print('Congratulations, you won!')

        # Reset the stats multipliers and stat offsets of all pokemon

        for pokemon in self.user_party:
            pokemon.reset_stat_multipliers()
            pokemon.reset_stat_offsets()

        for pokemon in self.enemy_party:
            pokemon.reset_stat_multipliers()
            pokemon.reset_stat_offsets()

        print('\n==================================')
        print('User\n')
        for pokemon in self.user_party:
            self.display_pokemon_info(pokemon)
        print('\n')
        print('Opponent\n')
        for pokemon in self.enemy_party:
            self.display_pokemon_info(pokemon)
        print('\n')

    def choose_action(self):

        available_actions = [
            'Fight',
            'Pokemon',
        ]

        while True:
            print('\nWhat will %s do?' % self.user_party[0].name)

            for action in available_actions:
                print(action)
            print('\n')
            choice = input()

            if choice in available_actions:
                break
            else:
                print('That action doesn\'t exist, please choose a valid action')

        return choice

    def explore_menu_options(self):

        while True:

            # First need to choose an action (fight, pokemon)

            chosen_action = self.choose_action()

            # Have all options default to fight for now

            open_menu_function = {
                'Fight': self.open_fight_menu,
                'Pokemon': self.open_pokemon_menu,
            }.get(chosen_action, None)

            is_turn_completed = open_menu_function()

            if is_turn_completed:
                break

    def open_fight_menu(self):

        current_round = Fight(self.user_party[0], self.enemy_party[0], self.round_number)
        chosen_option = current_round.choose_move(current_round.user_pokemon)
        enemy_chosen_option = current_round.choose_random_move(current_round.enemy_pokemon)

        if chosen_option != 'Back':
            current_round.fight(chosen_option, enemy_chosen_option)
            return True

    def open_pokemon_menu(self):

        chosen_pokemon_party_index = party.user_choose_pokemon_to_switch_to(self.user_party)

        if chosen_pokemon_party_index == 0:
            print("%s is already in battle!" % self.user_party[0].name)
            return self.open_pokemon_menu()
        elif chosen_pokemon_party_index != -1:
            party[0].reset_stat_offsets()
            party.switch_pokemon(self.user_party, 0, chosen_pokemon_party_index)
            print("User sent out %s!" % self.user_party[0].name)

            # Now let the opponent take their turn
            opponents_turn = Fight(self.user_party[0], self.enemy_party[0], self.round_number)
            opponents_turn.one_side_attacks('enemy')
            return True

    def display_pokemon_info(self, pokemon):

        print("{}: {}HP Status: {}".format(pokemon.name, pokemon.stats['HP'][0], pokemon.status_condition))

def check_burned_or_poisoned(pokemon):

    if pokemon.status_condition is 'Poisoned' or pokemon.status_condition is 'Burned':
        print("%s is %s so it takes damage!" % (pokemon.name, pokemon.status_condition))
        pokemon.inflict_burn_or_poison_damage()
        print("%s\'s HP is now %s" % (pokemon.name, pokemon.stats['HP'][0]))
