# automatically generated by the FlatBuffers compiler, do not modify

# namespace: flatbuffers

import flatbuffers
from flatbuffers.compat import import_numpy

np = import_numpy()


class Anchor(object):
    __slots__ = ["_tab"]

    # Anchor
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Anchor
    def X(self):
        return self._tab.Get(
            flatbuffers.number_types.Float32Flags,
            self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(0),
        )

    # Anchor
    def Y(self):
        return self._tab.Get(
            flatbuffers.number_types.Float32Flags,
            self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(4),
        )


def CreateAnchor(builder, x, y):
    builder.Prep(4, 8)
    builder.PrependFloat32(y)
    builder.PrependFloat32(x)
    return builder.Offset()
