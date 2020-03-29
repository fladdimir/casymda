"""json-serializable flat dictionary canvas"""
from casymda.visualization.canvas.scaled_canvas import ScaledCanvas

ANCHOR_DICT = {
    "c": [0.5, 0.5],
    "nw": [0, 0],
    "n": [0.5, 0],
    "ne": [1, 0],
    "e": [1, 0.5],
    "se": [1, 1],
    "s": [0.5, 1],
    "sw": [0, 1],
    "w": [0, 0.5],
}


class WebCanvas(ScaledCanvas):
    """implements the scaled canvas,
    using a dictionary to gather information on objects.
    dictionary is flat so that it can be shared between multiple processes"""

    def __init__(self, dictionary, width, height, scale=1.0):
        super().__init__(scale)
        self.dict = dictionary
        self.width = width
        self.height = height

        self.photo_lookup = {}

        self.element_id_counter = 0

    def load_image_file(self, path):
        potential_key = path
        if potential_key in self.photo_lookup:
            return self.photo_lookup[potential_key]
        self.element_id_counter += 1
        self.dict[self.element_id_counter] = {
            "factor": self.scale,
            "path": path,
            "type": "photo",
        }
        self.photo_lookup[potential_key] = self.element_id_counter
        return self.element_id_counter

    def create_image(self, x_coord, y_coord, image_file, anchor="c"):
        x_coord, y_coord = self._scale_coords((x_coord, y_coord))
        self.element_id_counter += 1
        self.dict[self.element_id_counter] = {
            "x": x_coord,
            "y": y_coord,
            "anchor": ANCHOR_DICT[anchor],
            "type": "image",
            "photo_id": image_file,
            "path": self.dict[image_file]["path"],
            "factor": self.dict[image_file]["factor"],
        }
        return self.element_id_counter

    def create_text(
        self, x_coord, y_coord, text="", anchor="se", fill="black", font="Helvetica 16"
    ):
        x_coord, y_coord = self._scale_coords((x_coord, y_coord))
        self.element_id_counter += 1
        self.dict[self.element_id_counter] = {
            "x": x_coord,
            "y": y_coord,
            "anchor": ANCHOR_DICT[anchor],
            "type": "text",
            "text": text,
            "fill": fill,
            "font_family": font.split(" ")[0],
            "font_size": int(font.split(" ")[1]),
        }
        return self.element_id_counter

    def delete(self, element_id):
        if element_id in self.dict:
            del self.dict[element_id]
            return True
        return False

    def set_coords(self, element_id, x_y):
        x_coord, y_coord = self._scale_coords(x_y)
        if element_id in self.dict:
            entry = self.dict[element_id]
            entry["x"] = x_coord
            entry["y"] = y_coord
            self.dict[element_id] = entry
            return True
        return False

    def set_text_value(self, element_id, text=""):
        if element_id in self.dict:
            entry = self.dict[element_id]
            entry["text"] = text
            self.dict[element_id] = entry
            return True
        return False

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height
