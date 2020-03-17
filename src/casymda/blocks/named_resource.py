"""named resource"""
from simpy import Resource


class NamedResource(Resource):
    """simpy resource with name"""

    def __init__(self, env, name, capacity=1, xy=None, ways=None):
        super().__init__(env, capacity=capacity)

        self.name = name
        self.xy = xy
        self.ways = ways
