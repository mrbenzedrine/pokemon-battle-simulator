from fight import Fight

class Battle():

    def __init__(self, user_party, enemy_party):

        self.user_party = user_party
        self.enemy_party = enemy_party
        self.round_number = 0

    def battle(self):

        while sum([pokemon.stats['HP'][0] for pokemon in self.user_party]) > 0 and sum([pokemon.stats['HP'][0] for pokemon in self.enemy_party]) > 0:

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

        print('Your %s\'s HP is %s' % (self.user_party[0].name, self.user_party[0].stats['HP'][0]))
        print('Their %s\'s HP is %s' % (self.enemy_party[0].name, self.enemy_party[0].stats['HP'][0]))

        # Reset the stats multipliers of both pokemon

        self.user_party[0].reset_stat_multipliers()
        self.enemy_party[0].reset_stat_multipliers()

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
