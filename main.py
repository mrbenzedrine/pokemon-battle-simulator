from pokemon import Pokemon
from user_pokemon import UserPokemon
from battle import battle

MyBulbasaur = UserPokemon('Bulbasaur')
TheirSquirtle = Pokemon('Squirtle')

battle(MyBulbasaur, TheirSquirtle)
