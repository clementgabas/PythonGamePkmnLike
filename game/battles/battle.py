from game.characters.player import Player


class WildPkmn:
    pass


class Battle:

    def __init__(self, player: Player, opponent: Player | WildPkmn):
        self.player = player
        self.opponent = opponent
