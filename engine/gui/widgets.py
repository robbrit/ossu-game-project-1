import collections
import dataclasses
import pathlib
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
)

from engine import scripts


@dataclasses.dataclass
class Asset:
    """An asset for the game (audio, image, etc.)."""

    name: str
    path: str


@dataclasses.dataclass
class Button:
    """An interactable GUI element."""

    selected_image_asset: str
    unselected_image_asset: str
    name: str

    center: Tuple[int, int]
    action: scripts.GameCallable

    left: Optional[str] = None
    right: Optional[str] = None
    up: Optional[str] = None
    down: Optional[str] = None

    def __init__(
        self,
        selected_image_asset: str,
        unselected_image_asset: str,
        name: str,
        center: Tuple[int, int],
        action: str,
        left: Optional[str] = None,
        right: Optional[str] = None,
        up: Optional[str] = None,
        down: Optional[str] = None,
    ):
        self.selected_image_asset = selected_image_asset
        self.unselected_image_asset = unselected_image_asset
        self.name = name
        self.center = center
        self.left = left
        self.right = right
        self.up = up
        self.down = down

        self.action = scripts.load_callable(action)  # type: ignore


@dataclasses.dataclass
class Image:
    """A basic image in a GUI."""

    image_asset: str
    center: Tuple[int, int]


@dataclasses.dataclass
class GUISpec:
    """An outline for the static elements within the GUI.

    This is a declarative spec, intending to lay out how a GUI will look in an easily
    serializable format like JSON, and then tie interactions to Python code.
    """

    assets: List[Asset]
    buttons: List[Button]
    images: List[Image]

    cancel_action: Optional[scripts.GameCallable]
    initial_selected_button: Optional[Button] = None

    def __init__(
        self,
        assets: Optional[List[Dict[str, Any]]],
        buttons: Optional[List[Dict[str, Any]]],
        images: Optional[List[Dict[str, Any]]],
        cancel_action: Optional[str] = None,
        initial_selected_button: Optional[str] = None,
    ):
        self.assets = [Asset(**asset) for asset in (assets or [])]
        self.buttons = [Button(**button) for button in (buttons or [])]
        self.images = [Image(**image) for image in (images or [])]

        if cancel_action:
            self.cancel_action = scripts.load_callable(cancel_action)

        if initial_selected_button:
            self.initial_selected_button = next(
                button
                for button in self.buttons
                if button.name == initial_selected_button
            )

    def validate(self, dimensions: Tuple[int, int]) -> None:
        """Validates the GUISpec."""

        if not self.buttons and not self.images:
            raise ValidationError("Must have at least one button or image")

        asset_names = collections.Counter([a.name for a in self.assets])
        duplicate_assets = [asset for asset, count in asset_names.items() if count > 1]
        if duplicate_assets:
            raise ValidationError(f"Duplicate asset name: {duplicate_assets}.")

        button_names = collections.Counter([b.name for b in self.buttons])
        duplicate_buttons = [name for name, count in button_names.items() if count > 1]
        if duplicate_buttons:
            raise ValidationError(f"Duplicate button name: {duplicate_buttons}")

        image_names = collections.Counter([i.image_asset for i in self.images])
        duplicate_images = [image for image, count in image_names.items() if count > 1]
        if duplicate_images:
            raise ValidationError(f"Duplicate image name(s): {duplicate_images}")

        for button in self.buttons:
            if button.selected_image_asset not in [a.name for a in self.assets]:
                raise ValidationError(
                    f"Button {button.selected_image_asset} not in assets"
                )

        for image in self.images:
            if image.image_asset not in [i.name for i in self.assets]:
                raise ValidationError(f"Image {image.image_asset} not in assets")

        for asset in self.assets:
            if not pathlib.Path(asset.path).is_file():
                raise ValidationError(f"Asset path does not exist: {asset.path}")

        screen_width, screen_height = dimensions

        for button in self.buttons:
            if button.center[0] < 0 or button.center[0] > screen_width:
                raise ValidationError(
                    f"Button {button.name} is off screen horizontally"
                )
            if button.center[1] < 0 or button.center[1] > screen_height:
                raise ValidationError(f"Button {button.name} is off screen vertically")
            for direction in ["left", "right", "up", "down"]:
                name = getattr(button, direction)
                if name and name not in button_names:
                    raise ValidationError(
                        f"Button {name} referenced by {direction} not in buttons"
                    )

        for image in self.images:
            if image.center[0] < 0 or image.center[0] > screen_width:
                raise ValidationError(
                    f"Image {image.image_asset} is off screen horizontally"
                )
            if image.center[1] < 0 or image.center[1] > screen_height:
                raise ValidationError(
                    f"Image {image.image_asset} is off screen vertically"
                )


class ValidationError(Exception):
    """An error during validation."""
