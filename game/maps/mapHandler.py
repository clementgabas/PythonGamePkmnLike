import pytmx
import pyscroll
import pygame
from game.characters.player import Player


class MapLoader:

    def __init__(self, filename: str, screen_size: tuple[int, int] = (808, 800)):
        self.tmx_data = pytmx.util_pygame.load_pygame(filename)
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(data=self.map_data, size=screen_size)

    def load(self):
        return self.tmx_data, self.map_data, self.map_layer


class Map:

    ZOOM_VALUE: int = 1.2

    def __init__(self, source: str, df_layer: int, player: Player, name: str = "",
                 screen_size: tuple[int, int] = (800, 800)):

        self.df_layer: int = df_layer  # number of layer on the map
        self.player: Player = player
        self.name: str = name  # name of the map

        # Map loading
        mapLoader = MapLoader(filename=source, screen_size=screen_size)
        self.tmx_data, self.map_data, self.map_layer = mapLoader.load()
        self.map_layer.zoom = self.ZOOM_VALUE

        self.collision_walls, self.portals_entries_dict, self.pkmn_spawn_zone_dict = self.make_collision_rectangle_lists()

        self.group = self.make_layers_group()

        self.number_of_playerSpawn = self.compute_nb_of_player_spawn()

    def make_collision_rectangle_lists(self):
        # Collisions rectangles and portals entries rectangles
        collision_list = []
        portals_entry_dict = {}
        pkmn_spawn_zone_dict = {}

        for obj in self.tmx_data.objects:
            match obj.type:
                case "collision":  # object of type collision : the player cannot enter the polygon
                    collision_list.append(pygame.Rect(obj.x, obj.y - 32, obj.width, obj.height))
                case "portal_entry":
                    portals_entry_dict[obj.name] = pygame.Rect(obj.x, obj.y - 32, obj.width, obj.height)
                case "pokemonSpawnZone":
                    pkmn_spawn_zone_dict[obj.name] = pygame.Rect(obj.x, obj.y - 32, obj.width, obj.height)

        return collision_list, portals_entry_dict, pkmn_spawn_zone_dict

    def make_layers_group(self):
        # Draw on layers
        group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=self.df_layer)
        group.add(self.player)
        return group

    def compute_nb_of_player_spawn(self):
        count = 0
        for obj in self.tmx_data.objects:
            if obj.type == "playerSpawn":
                count += 1
        return count
