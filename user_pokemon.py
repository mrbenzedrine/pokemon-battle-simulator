from pokemon import Pokemon
import pickle

class UserPokemon(Pokemon):

    def __init__(self, name):

        super().__init__(name)

        try:
            last_state = self.load_last_state()
        except IOError:
            print('No previous save state existed, so creating a fresh one')
            initial_state = self.create_initial_state_file()

            self.level = initial_state['level']
            self.current_xp = initial_state['current_xp']
            self.level_up_xp = initial_state['level_up_xp']
            self.stats['HP'] = initial_state['HP']
            self.status_condition = initial_state['status_condition']
        else:
            print('Previous save state existed, so loading it')
            self.level = last_state['level']
            self.current_xp = last_state['current_xp']
            self.level_up_xp = last_state['level_up_xp']
            self.stats['HP'] = last_state['HP']
            self.status_condition = last_state['status_condition']

    def show_xp_to_next_level(self):
        print(self.level_up_xp - self.current_xp)

    def update_xp(self, gained_xp):
        print('Your %s gained %s xp!' % (self.name, gained_xp))
        print(self.current_xp)
        self.current_xp += gained_xp
        print('Your %s now has %s XP!' % (self.name, self.current_xp))

        # Now check if Pokemon has gained enough XP to go up a level

        self.check_if_should_level_up()

        # Now need to update the state to include the xp gained
        # from this interaction

        self.update_state_file()

    def check_if_should_level_up(self):
        if self.current_xp >= self.level_up_xp:
            self.level += 1
            print('Your %s is now level %s!' % (self.name, self.level))

            # Should also increase the level_up_xp and take the remainder
            # of the XP that is leftover after getting to the
            # next level and add it on

            remaining_xp = self.current_xp - self.level_up_xp

            self.current_xp = 0 + remaining_xp
            self.level_up_xp = 60

            self.increase_stats_after_level_up()

    def increase_stats_after_level_up(self):
        for key in self.stats:
            if key != 'HP':
                self.stats[key] = round(1.2 * self.stats[key])
            else:
                self.stats['HP'][0] = round(1.2 * self.stats['HP'][0])
                self.stats['HP'][1] = round(1.2 * self.stats['HP'][1])
            print(self.stats[key])

    def create_initial_state_file(self):
        # Needs to save the Pokemon's xp, level etc
        # in an external file whenever an instance of
        # this class is created
        initial_pokemon_state = {
            'level': 5,
            'current_xp': 0,
            'level_up_xp': 50,
            'HP': self.stats['HP'],
            'status_condition': self.status_condition
        }
        out_file = open(self.name + '_state', 'wb')
        pickle.dump(initial_pokemon_state, out_file)
        return initial_pokemon_state

    def update_state_file(self):
        new_pokemon_state = {
            'level': self.level,
            'current_xp': self.current_xp,
            'level_up_xp': self.level_up_xp,
            'HP': self.stats['HP'],
            'status_condition': self.status_condition
        }
        out_file = open(self.name + '_state', 'wb')
        pickle.dump(new_pokemon_state, out_file)

    def load_last_state(self):
        in_file = open(self.name + '_state', 'rb')
        last_pokemon_state = pickle.load(in_file)
        print(last_pokemon_state)
        return last_pokemon_state
