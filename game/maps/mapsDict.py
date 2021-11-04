MAPS_DICT = {
    "startVillage": "assets/maps/villagesAndCities/startVillage.tmx",
    # "startVillage": "assets/maps/lake/lake1.1.tmx",
    "house3_startVillage": "assets/maps/houses/house3_startVillage.tmx"
}

PKMN_SPAWN_ZONE_DICT = {
    "lightForrest_startVillage": {
        "rate": 0.1/30,
        "list_of_pkmn": {
            "pkmn1": "rate",
            "pkmn2": "rate"
        }
    }
}


def add_relative_way(way: str) -> str:
    return "./" + way
