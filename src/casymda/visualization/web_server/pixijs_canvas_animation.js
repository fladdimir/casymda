console.log("pixijs_canvas_animation.js loaded")
// pixijs-based animation

let type = "WebGL"
if (!PIXI.utils.isWebGLSupported()) {
    type = "canvas"
}
PIXI.utils.sayHello(type)

let app, loader;
let animated_elements;

// create pixi canvas at certain element
function initialize_animation(parent_dom_element, width, height) {

    remove_old_canvas_elements(parent_dom_element);
    app = new PIXI.Application({
        width: width, height: height,
        backgroundColor: 0xFFFFFF
    });
    app.ticker.maxFPS = 30;
    app.stage.sortableChildren = true;
    parent_dom_element.appendChild(app.view);

    loader = new PIXI.Loader();

    animated_elements = {};
}

// process given state
function animate_simulation(state) {

    // process all elements
    for (var key in state) {
        var state_element = state[key];
        if (state_element.type === "text") _process_text(key, state_element);
        else if (state_element.type === "photo") _process_resource(state_element); // "photo" means image resource (to be loaded)
        else if (state_element.type === "image") _process_image(key, state_element);
    }

    // also check if some animated elements are not present anymore
    destroy_removed_elements(state);
}

// PROCESS ELEMENTS HELPER
function _process_resource(state_element) {
    // check if the resource is already loaded and start to load it if not
    if (!(state_element.path in loader.resources) && !loader.loading) {
        let element_to_load = loader.add(state_element.path, "files?filepath=" + state_element.path);
        element_to_load.load();
    }
}

function _process_image(key, state_element) {
    var pixi_sprite;
    if (!(key in animated_elements) && state_element.path in loader.resources && loader.resources[state_element.path].isComplete) {
        // create new sprite
        pixi_sprite = new PIXI.Sprite.from("files?filepath=" + state_element.path);
        pixi_sprite.scale.set((state_element.factor, state_element.factor))
        pixi_sprite.anchor.set(state_element.anchor[0], state_element.anchor[1]);
        pixi_sprite.zIndex = parseInt(key);
        app.stage.addChild(pixi_sprite);
        animated_elements[key] = pixi_sprite;
    }
    if (key in animated_elements) {
        // update properties
        pixi_sprite = animated_elements[key];
        pixi_sprite.position.x = state_element.x;
        pixi_sprite.position.y = state_element.y;
    }
}

function _process_text(key, state_element) {
    var pixi_text;
    if (animated_elements[key] === undefined) {
        // create text on canvas
        pixi_text = new PIXI.Text("", { fontFamily: state_element.font_family, fontSize: state_element.font_size, fill: state_element.fill });
        pixi_text.anchor.set(state_element.anchor[0], state_element.anchor[1]);
        pixi_text.zIndex = parseInt(key);
        app.stage.addChild(pixi_text);
        animated_elements[key] = pixi_text;
    }
    // update properties: position / text
    pixi_text = animated_elements[key];
    pixi_text.position.x = state_element.x;
    pixi_text.position.y = state_element.y;
    pixi_text.text = state_element.text;
}


function remove_old_canvas_elements(parent_dom_element) {
    while (parent_dom_element && parent_dom_element.lastChild && parent_dom_element.lastChild.nodeName == "CANVAS") {
        parent_dom_element.removeChild(parent_dom_element.lastChild);
    }
}

function destroy_removed_elements(state) {
    for (var anim_key in animated_elements) {
        if (!(anim_key in state)) {
            animated_elements[anim_key].destroy();
            delete animated_elements[anim_key];
        }
    }
}
