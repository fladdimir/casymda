"""canvas"""

from abc import abstractmethod


class ScaledCanvas:
    """overview of canvas methods called from visualizer"""

    def __init__(self, scale: float) -> None:
        self.scale = scale

    @abstractmethod
    def load_image_file(self, path: str):
        """takes file path and returns loaded image file reference"""

    @abstractmethod
    def create_image(self, x_coord: int, y_coord: int, image_file, anchor="c") -> int:
        """places image on canvas and returns image reference"""

    @abstractmethod
    def create_text(
        self,
        x_coord: int,
        y_coord: int,
        text: str = "",
        anchor: str = "se",
        fill: str = "black",
        font: str = "Helvetica 16",
    ) -> int:
        """places text on canvas and returns reference"""

    @abstractmethod
    def delete(self, element_id: int) -> bool:
        """deletes element and returns True if deleted"""

    @abstractmethod
    def set_coords(self, element_id: int, x_y: tuple):
        """places the given element at a given position"""

    @abstractmethod
    def set_text_value(self, element_id: int, text: str):
        """changes the elements text"""

    @abstractmethod
    def get_width(self) -> int:
        """returns width"""

    @abstractmethod
    def get_height(self) -> int:
        """returns heigth"""

    def _scale_coords(self, x_y: tuple):
        """returns tuple values multiplied by factor"""
        return tuple(map(lambda c: int(c * self.scale), x_y))
