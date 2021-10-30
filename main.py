import pygame

from game.maps.mapsDict import MAPS_DICT

from game.mainGame import Game

INIT_MAP = "startVillage"


if __name__ == '__main__':
    pygame.init()
    game = Game(init_map_filename=MAPS_DICT[INIT_MAP])
    game.run()


