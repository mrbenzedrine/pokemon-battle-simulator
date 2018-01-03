from pokemon import Pokemon
from user_pokemon import UserPokemon
from battle import Battle

MyBulbasaur = UserPokemon('Bulbasaur')
TheirSquirtle = Pokemon('Squirtle')
test_battle = Battle(MyBulbasaur, TheirSquirtle)
test_battle.battle()
