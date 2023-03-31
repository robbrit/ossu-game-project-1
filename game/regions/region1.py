from engine import scripts


def building1_door(api: scripts.GameAPI) -> None:
    api.change_region("Region1Building1", "Entryway")


def building1_exit(api: scripts.GameAPI) -> None:
    api.change_region("Region1", "Building 1 Exit")
