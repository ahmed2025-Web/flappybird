from ..utils import GameConfig
from .entity import Entity


class WelcomeMessage(Entity):
    def __init__(self, config: GameConfig) -> None:
        image = config.images.welcome_message
        super().__init__(
            config=config,
            image=image,
            x=0,
            y=0,
            w=config.window.width,
            h=config.window.height,
        )
