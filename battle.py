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

            # First need to choose an action (fight, bag, pokemon, run)

            chosen_action = self.choose_action()

            if chosen_action == 'Fight' or \
                chosen_action == 'Bag' or \
                chosen_action == 'Pokemon' or \
                    chosen_action == 'Run':

                # Have all options default to fight for now

                Fight(self.user_party[0], self.enemy_party[0], self.round_number).fight()

            # Check if either pokemon has a burn or poison status effect before moving to another
            # turn

            if self.user_party[0].status_condition is 'Poisoned' or self.user_party[0].status_condition is 'Burned':
                print("%s is %s so it takes damage!" % (self.user_party[0].name, self.user_party[0].status_condition))
                self.user_party[0].inflict_burn_or_poison_damage()
                print("%s\'s HP is now %s" % (self.user_party[0].name, self.user_party[0].stats['HP'][0]))
            elif self.enemy_party[0].status_condition is 'Poisoned' or self.enemy_party[0].status_condition is 'Burned':
                print("%s is %s so it takes damage!" % (self.enemy_party[0].name, self.enemy_party[0].status_condition))
                self.enemy_party[0].inflict_burn_or_poison_damage()
                print("%s\'s HP is now %s" % (self.enemy_party[0].name, self.enemy_party[0].stats['HP'][0]))

            if self.user_party[0].stats['HP'][0] == 0:
                print('Your %s has fainted!' % self.user_party[0].name)
                self.user_party[0].update_state_file()
            if self.enemy_party[0].stats['HP'][0] == 0:
                print('Their %s has fainted!' % self.enemy_party[0].name)

                # should then gain some xp for beating the opponent

                self.user_party[0].update_xp(50)

            # Now check if either party has run out of Pokemon

            if sum([pokemon.stats['HP'][0] for pokemon in self.user_party]) == 0 or sum([pokemon.stats['HP'][0] for pokemon in self.enemy_party]) == 0:
                break
            else:
                if self.user_party[0].stats['HP'][0] == 0:
                    # Now need to select another pokemon to send out
                    chosen_pokemon_party_index = party.user_choose_pokemon_to_switch_to(self.user_party)
                    party.switch_pokemon(self.user_party, 0, chosen_pokemon_party_index)
                    print('You sent out %s!' % self.user_party[0].name)
                elif self.enemy_party[0].stats['HP'][0] == 0:
                    # Opponent needs to send out another pokemon
                    chosen_pokemon_party_index = party.enemy_choose_pokemon_to_switch_to(self.enemy_party)
                    party.switch_pokemon(self.enemy_party, 0, chosen_pokemon_party_index)
                    print('They sent out %s!' % self.enemy_party[0].name)

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
