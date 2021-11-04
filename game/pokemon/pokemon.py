import pygame

from game.pokemon.pkmnNameToFileDict import PKMN_NAME_TO_SPRITE_DICT


class Move:
    pass


class Pokemon:

    def __init__(self, specie: str, surname: str, lvl: int, move_pool: list[Move], stats: dict[str, int]):
        self.specie = specie
        self.name = surname
        self.lvl = lvl
        self.move_pool = move_pool
        self.stats = stats
        self.sprite = pygame.image.load(PKMN_NAME_TO_SPRITE_DICT[self.specie])
        # self.image = #TODO:
        # stats
        self.hp = self.stats["hp"]
        self.max_hp = self.stats["hp"]
        self.atk = self.stats["atk"]
        self.def_ = self.stats["def"]
        self.spd = self.stats["spd"]
        self.sp_atk = self.stats["sp_atk"]
        self.sp_def = self.stats["sp_def"]
