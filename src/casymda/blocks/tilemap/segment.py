from typing import Tuple


class Segment:
    """holds information about a segment of a path of an entity"""

    def __init__(
        self, origin, destination, direction, length, cumulated_length, cumulated_time
    ) -> None:
        self.origin: Tuple[float, float] = origin
        self.destination: Tuple[float, float] = destination
        self.direction: Tuple[float, float] = direction
        self.length: float = length
        self.cumulated_length: float = cumulated_length
        self.cumlated_time: float = cumulated_time
