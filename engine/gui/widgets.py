import collections
import pathlib
from typing import (
    Any,
    Dict,
    List,
    NamedTuple,
    Optional,
    Tuple,
)

from engine import scripts, core


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
    action: scripts.GameCallable

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
            center=tuple(spec["center"]),
            action=scripts.load_callable(spec["action"]),
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

    cancel_action: Optional[scripts.GameCallable]

    initial_selected_button: Optional[Button]

    @classmethod
    def create(
        cls,
        spec: Dict[str, Any],
    ) -> "GUISpec":
        """Constructs a new GUISpec from raw dict data."""
        cancel_action = None
        if "cancel_action" in spec:
            cancel_action = scripts.load_callable(spec["cancel_action"])

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

    def validate(self) -> None:
        """Validates the GUISpec."""

        # Validation errors for images have not been tested
        if not self.assets:
            raise ValidationError("Must have at least one asset")
        if not self.buttons and not self.images:
            raise ValidationError("Must have at least one button or image")

        duplicate_assets = [
            asset for asset, count in collections.Counter(self.assets).items() if count > 1
        ]
        if len(duplicate_assets) > 0:
            raise ValidationError(f"Duplicate asset name(s): {duplicate_assets}")

        if len(set(self.assets)) != len(set(self.buttons)) + len(set(self.images)):
            # Can be general with the commented error below or
            # more detailed by iterating through the assets.
            # raise ValidationError(
            #     "Number of assets does not match the number of buttons and/or images."
            # )
            for asset in self.assets:
                if self.buttons and asset.name not in [
                    a.selected_image_asset for a in self.buttons
                ]:
                    raise ValidationError(f"Asset name not in buttons: {asset.name}")
                if self.buttons and asset.name not in [
                    a.unselected_image_asset for a in self.buttons
                ]:
                    raise ValidationError(f"Asset name not in buttons: {asset.name}")
                if self.images and asset.name not in [
                    a.image_asset for a in self.images
                ]:
                    raise ValidationError(f"Asset name not in images: {asset.name}")

        for a in self.assets:
            if not pathlib.Path(a.path).is_file():
                raise ValidationError(f"Asset path does not exist: {a.path}")

        duplicate_buttons = [
            button for button, count in collections.Counter(self.buttons).items() if count > 1
        ]
        if len(duplicate_buttons) > 0:
            raise ValidationError(f"Duplicate button name(s): {duplicate_buttons}")

        for button in self.buttons:
            if button.center[0] < 0 or button.center[0] > core.SCREEN_WIDTH:
                raise ValidationError(
                    f"Button {button.name} is off screen horizontally"
                )
            if button.center[1] < 0 or button.center[1] > core.SCREEN_HEIGHT:
                raise ValidationError(f"Button {button.name} is off screen vertically")

        duplicate_images = [
            image for image, count in collections.Counter(self.images).items() if count > 1
        ]
        if len(duplicate_images) > 0:
            raise ValidationError(f"Duplicate image name(s): {duplicate_images}")

        for image in self.images:
            if image.center[0] < 0 or image.center[0] > core.SCREEN_WIDTH:
                raise ValidationError(
                    f"Image {image.image_asset} is off screen horizontally"
                )
            if image.center[1] < 0 or image.center[1] > core.SCREEN_HEIGHT:
                raise ValidationError(
                    f"Image {image.image_asset} is off screen vertically"
                )


class ValidationError(Exception):
    """An error during validation."""
