import random
from typing import Callable, TypeVar, ParamSpec

from player import Player


T = TypeVar("T")
P = ParamSpec("P")


def in_play(started: bool) -> Callable[[Callable[P, T]], Callable[P, T]]:
    def in_play(method: Callable[P, T]) -> Callable[P, T]:
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            if len(args) == 0:
                raise TypeError("in_play only valid for Board methods")

            self = args[0]
            if not isinstance(self, Board):
                raise TypeError(f"in_play only valid for Board methods, not '{self.__class__.__qualname__}'")

            if self.started != started:
                raise RuntimeError(
                    f"{method.__qualname__} cannot be called unless the game {'is' if started else 'is not'} started"
                )

            return method(*args, **kwargs)
        return wrapper
    return in_play


class Board:
    def __init__(self) -> None:
        self.players: list[Player] = []
        self.current_turn = 0
        self.started = False
        # self.chance = []
        self.dice = (0, 0)

    def _roll(self):
        self.dice = (random.randrange(6) + 1, random.randrange(6) + 1)

    @in_play(False)
    def add_player(self, new_player: Player):
        if sum([1 for player in self.players if player.name == new_player.name or player.piece == new_player.piece]):
            # Player name and piece must be unique
            raise NotImplemented
        else:
            self.players.append(new_player)
            

    @in_play(False)
    def remove_player(self, name: str):
        self.players = [player for player in self.players if player.name != name]

    @in_play(False)
    def start(self):
        if len(self.players) > 1:
            self.started = True

