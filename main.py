from pokemon import Pokemon
from user_pokemon import UserPokemon
from battle import Battle

MyBulbasaur = UserPokemon('Bulbasaur')
MySquirtle = UserPokemon('Squirtle')
TheirSquirtle = Pokemon('Squirtle')
TheirBulbasaur = Pokemon('Bulbasaur')
MyParty = [MyBulbasaur, MySquirtle]
TheirParty = [TheirSquirtle, TheirBulbasaur]
test_battle = Battle(MyParty, TheirParty)
test_battle.battle()
