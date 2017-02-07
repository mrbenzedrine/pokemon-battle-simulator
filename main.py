from pokemon import Pokemon
from user_pokemon import UserPokemon
from battle import battle

MyParty = []
# My party of up to 6 pokemon
TheirParty = []
# Their party of up to 6 pokemon

MyBulbasaur = UserPokemon('Bulbasaur')
TheirSquirtle = Pokemon('Squirtle')
# MyBulbasaur.create_initial_state_file
# MyBulbasaur.load_last_state()

battle(MyBulbasaur, TheirSquirtle)
