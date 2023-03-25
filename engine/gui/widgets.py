import importlib
from typing import (
    Any,
    Callable,
    Dict,
    List,
    NamedTuple,
    Optional,
    Tuple,
)

from engine import game_state

GameCallable = Callable[[game_state.GameAPI], None]


def _load_callable(path: str) -> GameCallable:
    """Loads a callable object.

    Note that this doesn't actually check if the thing is callable, or checks the
    arguments/return type.
    """
    mod_name, class_name = path.rsplit(".", 1)

    # TODO(rob): Determine if this is insecure.
    mod = importlib.import_module(mod_name)
    return getattr(mod, class_name)


class Asset(NamedTuple):
    """An asset for the game (audio, image, etc.)."""

    name: str
    path: str


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
    action: GameCallable

    @classmethod
    def create(cls, spec: Dict[str, Any]) -> "Button":
        return Button(
            selected_image_asset=spec["selected_image_asset"],
            unselected_image_asset=spec["unselected_image_asset"],
            name=spec["name"],
            left=spec.get("left"),
            right=spec.get("right"),
            up=spec.get("up"),
            down=spec.get("down"),
            center=spec["center"],
            action=_load_callable(spec["action"]),
        )


class Image(NamedTuple):
    """A basic image in a GUI."""

    image_asset: str
    center: Tuple[int, int]


class GUISpec(NamedTuple):
    """An outline for the static elements within the GUI.

    This is a declarative spec, intending to lay out how a GUI will look in an easily
    serializable format like JSON, and then tie interactions to Python code.
    """

    assets: List[Asset]
    buttons: List[Button]
    images: List[Image]

    cancel_action: Optional[GameCallable]

    initial_selected_button: Optional[Button]

    @classmethod
    def create(
        cls,
        spec: Dict[str, Any],
    ) -> "GUISpec":
        """Constructs a new GUISpec from raw dict data."""
        cancel_action = None
        if "cancel_action" in spec:
            cancel_action = _load_callable(spec["cancel_action"])

        buttons = [Button.create(b) for b in spec.get("buttons", [])]

        selected_button_name = spec.get("initial_selected_button")
        selected_button = None
        if selected_button_name is not None:
            selected_button = next(
                (b for b in buttons if b.name == selected_button_name),
                None,
            )

        gui_spec = GUISpec(
            assets=[Asset(**a) for a in spec.get("assets", [])],
            buttons=buttons,
            images=[Image(**b) for b in spec.get("images", [])],
            cancel_action=cancel_action,
            initial_selected_button=selected_button,
        )

        cls.validate(gui_spec)
        return gui_spec

    def validate(self):
        """Validates the GUISpec."""
        from engine.core import SCREEN_WIDTH, SCREEN_HEIGHT

        len_assets = len(self.assets)
        no_buttons = len(self.buttons) == 0
        no_images = len(self.images) == 0
        # works
        if len_assets == 0:
            raise ValidationError("Must have at least one asset")
        if no_buttons & no_images:
            raise ValidationError("Must have at least one button or image")

        # works
        if len_assets != len(set(self.assets)):
            for asset in self.assets:
                if asset.name in [a.name for a in self.assets]:
                    raise ValidationError(f"Duplicate asset name: {asset.name}")
                if not no_buttons and asset.name not in [a.name for a in self.buttons]:
                    print(asset.name)
                    raise ValidationError(f"Asset name not in buttons: {asset.name}")
                if not no_images and asset.name not in [a.image_asset for a in self.images]:
                    raise ValidationError(f"Asset name not in images: {asset.name}")
        #  works
        seen_names = set()
        for button in self.buttons:
            if button.name in seen_names:
                raise ValidationError(f"Duplicate button name: {button.name}")
            else:
                seen_names.add(button.name)

        # untested
        seen_images = set()
        for image in self.images:
            if image.image_asset in seen_images:
                raise ValidationError(f"Duplicate image name: {image.image_asset}")
            else:
                seen_images.add(image.image_asset)

        for button in self.buttons:
            if button.center[0] < 0 or button.center[0] > SCREEN_WIDTH:
                raise ValidationError(f"Button {button.name} is off screen horizontally")
            # I believe the origin of the screen in Arcade if the bottom left corner
            if button.center[1] < 0 or button.center[1] > SCREEN_HEIGHT:
                raise ValidationError(f"Button {button.name} is off screen vertically")
        # No error but nonworking button when value is changed for initial_selected_button or button.name
        if self.initial_selected_button is not None:
            if self.initial_selected_button not in self.buttons:
                print(self.initial_selected_button)
                print(self.buttons)
                raise ValidationError(f"Initial selected button not in buttons: {self.initial_selected_button}")


class ValidationError(Exception):
    """An error during validation."""