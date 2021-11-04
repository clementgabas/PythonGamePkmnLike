from game.characters.playersprite import PlayerSprite
from game.pokemon.pokemon import Pokemon


class WildPkmn(Pokemon):
    pass


class Battle:

    def __init__(self, player: PlayerSprite, opponent: PlayerSprite | WildPkmn):
        self.player = player
        self.opponent = opponent
        self.turn_number = 1


    def start(self):
        print("Battle started!")
        print(f"PlayerSprite {self.player.name} vs. {self.opponent.name}")