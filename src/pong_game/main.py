from . import game
from . import assets_path
from core import utils


def main() -> None:
    """Game entry."""

    game_instance = game.PongGame(600, 400, "Pong Game", utils.load_image(f"{assets_path}/icon.png"))
    game_instance.start()
