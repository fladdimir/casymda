# Tilemap-based simulation of object movements

The model contains an example for the casymda tilemap feature. Entities are moving on a small tilemap between the nodes "A" & "C".

## Setup the _CoordinatesHolder_

Parsed, processed (shortest paths), and cached (pickled) tilemap csv information is held by a managing `coordinates_holder`.
This coordinates-holder object is created/imported (from a _cooh-config_) as part of the `model_template` and before the generated model-blocks.
It can then be referenced by the blocks in need.
