import random

from pygame import Rect

from game.characters.player import Player
from game.maps.mapHandler import Map
from game.maps.mapsDict import MAPS_DICT, add_relative_way, PKMN_SPAWN_ZONE_DICT


class GameUpdater:

    def __init__(self, current_map, player: Player):
        self.current_map = current_map
        self.player = player

    def make_player_spawn(self, spawn_position: str = "playerSpawn", old_map_name: str = "") -> None:

        spawn_position += "_" + old_map_name
        spawn_position = spawn_position.removesuffix('_')
        player_position = self.current_map.tmx_data.get_object_by_name(spawn_position)
        self.player.position = [player_position.x, player_position.y]

    def collision_handler(self) -> None:
        for sprite in self.current_map.group.sprites():
            # collision handler : always handled because all maps have collisions
            if sprite.feet.collidelist(self.current_map.collision_walls) > -1:
                sprite.move_back()

    def portal_handler(self) -> tuple[bool, str, str, str]:
        for portal_name in self.current_map.portals_entries_dict:
            portal_rectangle: Rect = self.current_map.portals_entries_dict[portal_name]
            if self.player.feet.colliderect(portal_rectangle):
                # the playersprite enters the portal 'portal_name'
                new_map_source = MAPS_DICT[portal_name]
                previous_map_name = self.current_map.name
                return True, new_map_source, previous_map_name, portal_name
            return False, "", "", ""

    def pkmn_spawn_zone_handler(self) -> tuple[bool, str]:
        for pkmn_spawn_zone in self.current_map.pkmn_spawn_zone_dict:
            spawn_zone_rectangle: Rect = self.current_map.pkmn_spawn_zone_dict[pkmn_spawn_zone]
            if self.player.feet.colliderect(spawn_zone_rectangle):
                # the playersprite is in the pokemon spawn zone
                num = random.random()
                rate = PKMN_SPAWN_ZONE_DICT[pkmn_spawn_zone]["rate"]
                if num < rate:
                    return True, pkmn_spawn_zone
        return False, ""

    def update(self):
        self.current_map.group.update()  # update the game

        self.collision_handler()  # handle collisions for playersprite an npc (for all sprites in fact)

        # handle portal entry for playersprite and so change of map
        portal_handling_bool, new_map_source, previous_map_name, portal_name = self.portal_handler()
        if portal_handling_bool:
            self.current_map = Map(source=add_relative_way(new_map_source), df_layer=4,
                                   player=self.player, name=portal_name)
            if self.current_map.number_of_playerSpawn > 1:
                self.make_player_spawn(old_map_name=previous_map_name)
            else:  # only one playerSpawn
                self.make_player_spawn()

        pkmn_spawn_bool, pkmn_spawn_zone = self.pkmn_spawn_zone_handler()
        if pkmn_spawn_bool:
            print("battle!!!!!!!!!!!!!!!!")
            # TODO: MAKE BATTLES §§§§§§§§§§§§§§§§§§§§§§§§§

        return self.current_map, self.player
