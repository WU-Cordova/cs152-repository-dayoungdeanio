import random
from character import Character

class Game:
    """ the Dice Battle game logic."""

    def __init__(self, player1: Character, player2: Character):
        """ initializes game with two players."""
        self.player1 = player1
        self.player2 = player2

    def attack(self, attacker: Character, defender: Character):
        """ an attack where the attacker rolls a die to determine damage dealt."""
        die_roll = random.randint(1, 6)  # die (1-6)
        damage = die_roll * attacker.attack_power  # Scale attack power
        defender.health -= damage  # reduce defender’s health
        print(f"{attacker.name} rolls a {die_roll} and deals {damage} damage to {defender.name}.")
        if defender.health <= 0:
            print(f"{defender.name} has been defeated!")

    def start_battle(self):
        """ starts battle between two players."""
        print(f"Battle begins: {self.player1.name} vs {self.player2.name}!\n")
        
        players = [self.player1, self.player2]
        turn = 0

        while self.player1.health > 0 and self.player2.health > 0:
            attacker = players[turn % 2]
            defender = players[(turn + 1) % 2]

            print(f"\n{attacker.name}'s turn to attack!")
            self.attack(attacker, defender)

            if defender.health <= 0:
                print(f"\n{attacker.name} wins the battle!")
                break  # end game if someone is defeated

            turn += 1
            input("\nPress Enter to continue...")  # pause
