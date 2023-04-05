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

from engine import scripts


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
        """Constructs a new Button from a dict."""
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
        dimensions: Tuple[int, int],
    ) -> "GUISpec":
        """Constructs a new GUISpec from raw dict data."""
        cancel_action = None
        if "cancel_action" in spec:
            cancel_action = scripts.load_callable(spec["cancel_action"])

        buttons = [Button.create(b) for b in spec.get("buttons", [])]

        selected_button_name = spec.get("initial_selected_button")
        selected_button = None
        if selected_button_name is not None:
            try:
                selected_button = next(
                    (b for b in buttons if b.name == selected_button_name)
                )
            except StopIteration as exc:
                raise ValidationError(
                    f"Initial select button {selected_button_name} does not exist."
                ) from exc

        gui_spec = GUISpec(
            assets=[Asset(**a) for a in spec.get("assets", [])],
            buttons=buttons,
            images=[Image(**b) for b in spec.get("images", [])],
            cancel_action=cancel_action,
            initial_selected_button=selected_button,
        )

        gui_spec.validate(dimensions)
        return gui_spec

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
