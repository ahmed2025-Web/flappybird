from ..utils import GameConfig
from .entity import Entity


class GameOver(Entity):
    def __init__(self, config: GameConfig) -> None:
        super().__init__(
            config=config,
            image=config.images.game_over,
            x=0,
            y=0,
            w=config.window.width,
            h=config.window.height,
        )
