import flatbuffers

from . import Anchor, Canvas, CanvasPosition, Element, Image, Photo, Text
from .ElementsUnion import ElementsUnion


def serialize(state: dict):

    num_elements = len(state)
    fb = flatbuffers.Builder(1024)  # default decisive?

    elements = []
    i: str
    e: dict
    for i, e in state.items():

        if e["type"] == "photo":
            path = fb.CreateString(e["path"])
            Photo.PhotoStart(fb)
            Photo.PhotoAddFactor(fb, e["factor"])
            Photo.PhotoAddPath(fb, path)
            elementBody = Photo.PhotoEnd(fb)
            elementType = ElementsUnion.Photo

        elif e["type"] == "image":
            path = fb.CreateString(e["path"])
            Image.ImageStart(fb)
            Image.ImageAddAnchor(fb, Anchor.CreateAnchor(fb, *e["anchor"]))
            Image.ImageAddFactor(fb, e["factor"])
            Image.ImageAddPath(fb, path)
            Image.ImageAddPhotoId(fb, e["photo_id"])
            Image.ImageAddPosition(
                fb, CanvasPosition.CreateCanvasPosition(fb, e["x"], e["y"])
            )
            elementBody = Image.ImageEnd(fb)
            elementType = ElementsUnion.Image

        elif e["type"] == "text":
            fill = fb.CreateString(e["fill"])
            font = fb.CreateString(e["font_family"])
            text = fb.CreateString(e["text"])
            Text.TextStart(fb)
            Text.TextAddAnchor(fb, Anchor.CreateAnchor(fb, *e["anchor"]))
            Text.TextAddFill(fb, fill)
            Text.TextAddFontFamily(fb, font)
            Text.TextAddFontSize(fb, e["font_size"])
            Text.TextAddPosition(
                fb, CanvasPosition.CreateCanvasPosition(fb, e["x"], e["y"])
            )
            Text.TextAddText(fb, text)
            elementBody = Text.TextEnd(fb)
            elementType = ElementsUnion.Text

        Element.ElementStart(fb)
        Element.ElementAddId(fb, int(i))
        Element.ElementAddElementType(fb, elementType)
        Element.ElementAddElement(fb, elementBody)
        element = Element.ElementEnd(fb)
        elements.append(element)

    Canvas.CanvasStartContentVector(fb, num_elements)
    for elem in elements:
        fb.PrependUOffsetTRelative(elem)
    content = fb.EndVector(num_elements)

    Canvas.CanvasStart(fb)
    Canvas.CanvasAddContent(fb, content)
    canvas = Canvas.CanvasEnd(fb)

    fb.Finish(canvas)
    binary = fb.Output()

    return binary
