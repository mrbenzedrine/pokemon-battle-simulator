from pokemon import Pokemon
from battle import Battle

MyBulbasaur = Pokemon('Bulbasaur')
MySquirtle = Pokemon('Squirtle')
TheirSquirtle = Pokemon('Squirtle')
TheirBulbasaur = Pokemon('Bulbasaur')
MyParty = [MyBulbasaur, MySquirtle]
TheirParty = [TheirSquirtle, TheirBulbasaur]
test_battle = Battle(MyParty, TheirParty)
test_battle.battle()
