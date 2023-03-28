from engine import game_state


def building1_door(api: game_state.GameAPI) -> None:
    api.change_region("Region1Building1", "Entryway")


def building1_exit(api: game_state.GameAPI) -> None:
    api.change_region("Region1", "Building 1 Exit")
