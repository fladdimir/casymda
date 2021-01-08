console.log("animation_client.js loaded");

// constants
const BASE_URL = window.location.origin;
const START_URL = BASE_URL + "/start";
const PAUSE_URL = BASE_URL + "/pause";
const RESUME_URL = BASE_URL + "/resume";
const STOP_URL = BASE_URL + "/stop";
const STATE_URL = BASE_URL + "/state";
const RT_FACTOR_BASE_URL = BASE_URL + "/rt_factor?value=";

const CANVAS_WIDTH_URL = BASE_URL + "/width";
const CANVAS_HEIGHT_URL = BASE_URL + "/height";


const ANIMATION_CANVAS_PARENT_ID = "animation_canvas_parent";
let ANIMATION_CANVAS_PARENT;
document.addEventListener('DOMContentLoaded', () => { ANIMATION_CANVAS_PARENT = document.querySelector("#" + ANIMATION_CANVAS_PARENT_ID); });

const running_timeouts = [];
let stopped = false;
let state = {};


// HTTP HELPER
function post(url) {
    const request = new XMLHttpRequest();
    request.open("POST", url);
    request.send();
}

// SIMULATION INTERACTION
async function start_simulation() {
    stop_simulation();

    // retrieve canvas dimensions first
    const canvas_width = await get_canvas_width();
    const canvas_height = await get_canvas_height();

    post(START_URL);
    initialize_animation(ANIMATION_CANVAS_PARENT, canvas_width, canvas_height);

    state = {};

    stopped = false;
    request_state_loop();
}

function request_state_loop() {
    if (!stopped) running_timeouts.push(setTimeout(state_query, 20, [request_state_loop, animate_current_state]));
}

async function state_query(callbacks) {
    const response = await fetch(STATE_URL);
    state = await response.json();
    callbacks.forEach(callback => {
        callback();
    });
}

function animate_current_state() {
    animate_simulation(state);
}


function pause_simulation() {
    post(PAUSE_URL);
}

function resume_simulation() {
    post(RESUME_URL);
}

function stop_simulation() {
    stopped = true;
    post(STOP_URL);
    while (running_timeouts.length > 0) {
        clearTimeout(running_timeouts.pop());
    }
}

function speed_slider_changed_to(value) {
    value = 101 - value;  // 1 - 100
    value /= 100;  // 0.01 - 1
    value = Math.pow(value, 3);  // exponential speedup
    set_rt_factor(value);
    return value;
}

function set_rt_factor(value) {
    post(RT_FACTOR_BASE_URL + String(value));
}

async function get_canvas_height() {
    const response = await fetch(CANVAS_HEIGHT_URL);
    const content = await response.text();
    return Number(content);
}

async function get_canvas_width() {
    const response = await fetch(CANVAS_WIDTH_URL);
    const content = await response.text();
    return Number(content);
}
