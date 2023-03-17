from typing import (
    Any,
    Callable,
    Dict,
    List,
    NamedTuple,
    Optional,
    Tuple,
)

VoidCallable = Callable[[None], None]


class Asset(NamedTuple):
    """An asset for the game (audio, image, etc.)."""

    name: str
    path: str

    # TODO(rob): Create some sort of enum class to specify which type of asset
    # this is.


class Button(NamedTuple):
    """An interactable GUI element."""

    selected_image_asset: str
    unselected_image_asset: str
    name: str

    left: Optional[str]
    right: Optional[str]
    up: Optional[str]
    down: Optional[str]

    center: Tuple[int, int]
    action: VoidCallable


class Image(NamedTuple):
    """A basic image in a GUI."""

    image_asset: str
    center: Tuple[int, int]


class GUISpec(NamedTuple):
    """An outline for the static elements within the GUI."""

    assets: List[Asset]
    buttons: List[Button]
    images: List[Image]

    cancel_action: VoidCallable

    def __init__(self, spec: Dict[str, Any], environment: Dict[str, VoidCallable]):
        self.assets = [Asset(a) for a in spec.get("assets", [])]
        self.buttons = [Button(b) for b in spec.get("buttons", [])]
        self.images = [Image(b) for b in spec.get("images", [])]

        if "cancel_action" in spec:
            self.cancel_action = environment[spec["cancel_action"]]

        # TODO(rob): We should probably validate things:
        # * any assets specified by buttons/images should exist.
        # * button links should exist.
        # * center coordinates should be on screen.
        # * asset/button names should be unique.
