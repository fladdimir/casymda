"""the location of this module corresponds to
the location of the icon image files"""
import os

from casymda.blocks.block_components.state import States

CURRENT_FILE_PATH = os.path.dirname(os.path.realpath(__file__))
STATE_PATHS = {}
for state in States:
    STATE_PATHS[state] = CURRENT_FILE_PATH + "/" + state.value + ".png"


def get_file_path(for_state: States) -> str:
    """returns the file path of the state icon"""
    return STATE_PATHS[for_state]
