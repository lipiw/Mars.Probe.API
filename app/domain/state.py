from abc import ABC, abstractmethod
from enum import Enum

class Direction(str, Enum):
    NORTH = "NORTH"
    EAST = "EAST"
    SOUTH = "SOUTH"
    WEST = "WEST"

class IDirectionState(ABC):
    @abstractmethod
    def turn_left(self) -> 'IDirectionState':
        pass

    @abstractmethod
    def turn_right(self) -> 'IDirectionState':
        pass

    @abstractmethod
    def move(self, x: int, y: int) -> tuple[int, int]:
        pass

    @property
    @abstractmethod
    def direction(self) -> Direction:
        pass

# Implementações Concretas para cada estado (direção)
class NorthState(IDirectionState):
    def turn_left(self) -> 'IDirectionState':
        return WestState()

    def turn_right(self) -> 'IDirectionState':
        return EastState()

    def move(self, x: int, y: int) -> tuple[int, int]:
        return x, y + 1

    @property
    def direction(self) -> Direction:
        return Direction.NORTH

class EastState(IDirectionState):
    def turn_left(self) -> 'IDirectionState':
        return NorthState()

    def turn_right(self) -> 'IDirectionState':
        return SouthState()

    def move(self, x: int, y: int) -> tuple[int, int]:
        return x + 1, y

    @property
    def direction(self) -> Direction:
        return Direction.EAST

class SouthState(IDirectionState):
    def turn_left(self) -> 'IDirectionState':
        return EastState()

    def turn_right(self) -> 'IDirectionState':
        return WestState()

    def move(self, x: int, y: int) -> tuple[int, int]:
        return x, y - 1

    @property
    def direction(self) -> Direction:
        return Direction.SOUTH

class WestState(IDirectionState):
    def turn_left(self) -> 'IDirectionState':
        return SouthState()

    def turn_right(self) -> 'IDirectionState':
        return NorthState()

    def move(self, x: int, y: int) -> tuple[int, int]:
        return x - 1, y

    @property
    def direction(self) -> Direction:
        return Direction.WEST

# Um "helper" ou "factory" para criar o estado inicial a partir do Enum
DIRECTION_STATE_MAP: dict[Direction, IDirectionState] = {
    Direction.NORTH: NorthState(),
    Direction.EAST: EastState(),
    Direction.SOUTH: SouthState(),
    Direction.WEST: WestState(),
}