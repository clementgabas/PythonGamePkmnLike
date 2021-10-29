import pygame
import random
from game.maps.mapLoader import MapLoader
from game.maps.mapsDict import MAPS_DICT, add_relative_way, PKMN_SPAWN_ZONE_DICT
from game.characters.player import Player


class Game:

    def __init__(self, init_map_source):
        # game window
        self.screen = pygame.display.set_mode(size=(800, 800))
        pygame.display.set_caption("Unnamed Yet")

        # Load player
        self.player = Player(0, 0)

        # Load the map
        init_map_source = add_relative_way(init_map_source)

        self.current_map = MapLoader(source=init_map_source, df_layer=5, player=self.player,
                                     screen_size=self.screen.get_size(), name="startVillage")
        self.load_new_map()

    def load_new_map(self, spawn_position: str = "playerSpawn", old_map_name: str = ""):

        spawn_position += "_" + old_map_name
        spawn_position = spawn_position.removesuffix('_')
        player_position = self.current_map.tmx_data.get_object_by_name(spawn_position)
        self.player.position = [player_position.x, player_position.y]

    def handle_input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self.player.move('up')
        if pressed[pygame.K_DOWN]:
            self.player.move('down')
        if pressed[pygame.K_LEFT]:
            self.player.move('left')
        if pressed[pygame.K_RIGHT]:
            self.player.move('right')

    def update(self):
        self.current_map.group.update()  # update the game

        for sprite in self.current_map.group.sprites():
            # collision handler : always handled because all maps have collisions
            if sprite.feet.collidelist(self.current_map.collision_walls) > -1:
                sprite.move_back()

            # portals handler
            for portal_name in self.current_map.portals_entries_dict:
                if self.player.feet.colliderect(self.current_map.portals_entries_dict[portal_name]):
                    # the player enters the portal 'portal_name'
                    new_map_source = MAPS_DICT[portal_name]
                    previous_map_name = self.current_map.name
                    self.current_map = MapLoader(source=add_relative_way(new_map_source), df_layer=4,
                                                 player=self.player, name=portal_name)
                    if self.current_map.number_of_playerSpawn > 1:
                        self.load_new_map(old_map_name=previous_map_name)
                    else:  # only one playerSpawn
                        self.load_new_map()

            # pkmn spawn zone handler
            for pkmn_spawn_zone in self.current_map.pkmn_spawn_zone_dict:
                if self.player.feet.colliderect(self.current_map.pkmn_spawn_zone_dict[pkmn_spawn_zone]):
                    # the player is in the pokemon spawn zone
                    num = random.random()
                    rate = PKMN_SPAWN_ZONE_DICT[pkmn_spawn_zone]["rate"]
                    if num < rate:
                        print("battle!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


    def run(self):
        clock = pygame.time.Clock()  # fps
        running = True

        while running:
            self.player.save_location()
            self.handle_input()  # input handler
            self.update()  # update the game
            self.current_map.group.center(self.player.rect)  # center the zoom on the player
            self.current_map.group.draw(self.screen)  # draw the layers on the map
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            clock.tick(60)
        pygame.quit()
