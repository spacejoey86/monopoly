class Player:
    def __init__(self, name: str, piece: str) -> None:
        self.name = name
        self.piece = piece

    def move(self) -> None:
        raise NotImplemented