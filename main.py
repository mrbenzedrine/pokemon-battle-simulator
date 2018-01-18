from pokemon import Pokemon
from user_pokemon import UserPokemon
from battle import Battle

MyBulbasaur = UserPokemon('Bulbasaur')
TheirSquirtle = Pokemon('Squirtle')
MyParty = [MyBulbasaur]
TheirParty = [TheirSquirtle]
test_battle = Battle(MyParty, TheirParty)
test_battle.battle()
