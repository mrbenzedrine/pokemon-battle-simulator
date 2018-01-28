from fight import Fight
import party

class Battle():

    def __init__(self, user_party, enemy_party):

        self.user_party = user_party
        self.enemy_party = enemy_party
        self.round_number = 0

        self.pre_battle_checks()

    def battle(self):

        while True:

            self.round_number += 1

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
                    self.user_party[0].update_state_file()

                    # Now need to select another pokemon to send out
                    party.switch_out_pokemon(self.user_party, 'user')

                if self.enemy_party[0].stats['HP'][0] == 0:

                    print('Their %s has fainted!' % self.enemy_party[0].name)

                    # should then gain some xp for beating the opponent
                    self.user_party[0].update_xp(50)

                    # Opponent needs to send out another pokemon
                    party.switch_out_pokemon(self.enemy_party, 'enemy')

        if sum([pokemon.stats['HP'][0] for pokemon in self.user_party]) == 0:
            print('Sorry, you lost...')
        else:
            print('Congratulations, you won!')

        # Reset the stats multipliers of all pokemon

        for pokemon in self.user_party:
            pokemon.reset_stat_multipliers()

        for pokemon in self.enemy_party:
            pokemon.reset_stat_multipliers()

    def choose_action(self):

        available_actions = [
            'Fight',
            'Bag',
            'Pokemon',
            'Run'
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

    def pre_battle_checks(self):

        # Assume that both parties have at least 1 Pokemon with non-zero HP
        # going into the battle

        # Check if the first Pokemon in each party has non-zero HP; if not,
        # send out the first Pokemon in the party with non-zero HP

        if self.user_party[0].stats['HP'][0] == 0:
            user_party_index = party.get_first_available_pokemon(self.user_party)
            party.switch_pokemon(self.user_party, 0, user_party_index)

        if self.enemy_party[0].stats['HP'][0] == 0:
            enemy_party_index = party.get_first_available_pokemon(self.enemy_party)
            party.switch_out_pokemon(self.enemy_party, 0, enemy_party_index)

    def explore_menu_options(self):

        while True:

            # First need to choose an action (fight, bag, pokemon, run)

            chosen_action = self.choose_action()

            # Have all options default to fight for now

            open_menu_function = {
                'Fight': self.open_fight_menu,
                'Bag': self.open_fight_menu,
                'Pokemon': self.open_fight_menu,
                'Run': self.open_fight_menu
            }.get(chosen_action, None)

            is_turn_completed = open_menu_function()

            if is_turn_completed:
                break

    def open_fight_menu(self):

        current_round = Fight(self.user_party[0], self.enemy_party[0], self.round_number)
        chosen_option = current_round.choose_move(current_round.user_pokemon)

        if chosen_option != 'Back':
            # Make the opponent's Squirtle use Tackle as default for now
            current_round.fight(chosen_option, current_round.enemy_pokemon.moves['Tackle'])
            return True

def check_burned_or_poisoned(pokemon):

    if pokemon.status_condition is 'Poisoned' or pokemon.status_condition is 'Burned':
        print("%s is %s so it takes damage!" % (pokemon.name, pokemon.status_condition))
        pokemon.inflict_burn_or_poison_damage()
        print("%s\'s HP is now %s" % (pokemon.name, pokemon.stats['HP'][0]))
