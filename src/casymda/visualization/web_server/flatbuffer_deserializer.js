import { casymda } from "./csa_generated.js";
console.log("flattbuffer deserializer loaded");

export async function deserialize_fb(response) {
  const array = await response.arrayBuffer(); // blob?
  const data = new Uint8Array(array);
  const buffer = new flatbuffers.ByteBuffer(data);
  const canvas = casymda.visualization.web_server.flatbuffers.Canvas.getRootAsCanvas(
    buffer
  );

  const state = {};

  const num_elements = canvas.contentLength();
  for (let i = 0; i < num_elements; i++) {
    const fb_element = canvas.content(i);
    const fb_typ = fb_element.elementType();
    const id_num = fb_element.id();

    const element = {};
    if (
      fb_typ == casymda.visualization.web_server.flatbuffers.ElementsUnion.Photo
    ) {
      const fb_photo = new casymda.visualization.web_server.flatbuffers.Photo();
      fb_photo.__init(fb_element.element(fb_element).bb_pos, buffer);
      element.type = "photo";
      element.path = fb_photo.path();
      element.factor = fb_photo.factor();
    } else if (
      fb_typ == casymda.visualization.web_server.flatbuffers.ElementsUnion.Image
    ) {
      // image
      const fb_image = new casymda.visualization.web_server.flatbuffers.Image();
      fb_image.__init(fb_element.element(fb_element).bb_pos, buffer);
      element.type = "image";
      element.x = fb_image.position().x();
      element.y = fb_image.position().y();
      element.anchor = [fb_image.anchor().x(), fb_image.anchor().y()];
      element.photo_id = fb_image.photoId();
      element.path = fb_image.path();
      element.factor = fb_image.factor();
    } else if (
      fb_typ == casymda.visualization.web_server.flatbuffers.ElementsUnion.Text
    ) {
      // text
      const fb_text = new casymda.visualization.web_server.flatbuffers.Text();
      fb_text.__init(fb_element.element(fb_element).bb_pos, buffer);
      element.type = "text";
      element.x = fb_text.position().x();
      element.y = fb_text.position().y();
      element.anchor = [fb_text.anchor().x(), fb_text.anchor().y()];
      element.text = fb_text.text();
      element.fill = fb_text.fill();
      element.font_family = fb_text.fontFamily();
      element.font_size = fb_text.fontSize();
    }
    state[id_num.toString()] = element; // move to end
  }
  return state;
}
