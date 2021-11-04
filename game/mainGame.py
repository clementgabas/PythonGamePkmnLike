import pygame

from game.gameUpdater import GameUpdater
from game.maps.mapHandler import Map
from game.maps.mapsDict import add_relative_way
from game.characters.player import Player


class Game:

    def __init__(self, init_map_filename: str):
        # game window
        self.screen = pygame.display.set_mode(size=(800, 800))
        pygame.display.set_caption("Unnamed Yet")

        # Load playersprite
        self.player = Player("nom", 0, 0)

        # Load the map
        init_map_filename = add_relative_way(init_map_filename)

        self.current_map = Map(source=init_map_filename, df_layer=5, player=self.player,
                               screen_size=self.screen.get_size(), name="startVillage")
        self.make_player_spawn()

    def make_player_spawn(self, spawn_position: str = "playerSpawn", old_map_name: str = ""):

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
        updater = GameUpdater(self.current_map, self.player)
        self.current_map, self.player = updater.update()

    def run(self):
        clock = pygame.time.Clock()  # fps
        running = True

        while running:
            self.player.save_location()
            self.handle_input()  # input handler
            self.update()  # update the game via gameUpdater

            self.current_map.group.center(self.player.rect)  # center the zoom on the playersprite
            self.current_map.group.draw(self.screen)  # draw the layers on the map
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            clock.tick(60)
        pygame.quit()
