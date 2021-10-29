import pytmx
import pyscroll
import pygame


class MapLoader:

    def __init__(self, source: str, df_layer: int, player, name: str = "", screen_size: tuple[int, int] = (800, 800)):

        self.df_layer = df_layer
        self.player = player
        self.name = name

        # Map loading
        self.tmx_data = pytmx.util_pygame.load_pygame(source)
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(data=self.map_data, size=screen_size)
        self.map_layer.zoom = 1.2

        self.collision_walls, self.portals_entries_dict, self.pkmn_spawn_zone_dict = self.make_collision_rectangle_lists()

        self.group = self.make_layers_group()

        self.number_of_playerSpawn = self.compute_nb_of_playerSpawn()

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

    def compute_nb_of_playerSpawn(self):
        count = 0
        for obj in self.tmx_data.objects:
            if obj.type == "playerSpawn":
                count += 1
        return count
