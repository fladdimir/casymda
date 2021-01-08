#!/bin/bash
# lets do a complete package install and see if the examples work
# (unfortunately its not possible to obtain a useable coverage report this way,
#  since the source path of the xml will point to the site-packages directory)
eval "pip install ."
eval "python3 -m pytest examples"
