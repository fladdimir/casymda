import {
  initialize_animation,
  animate_simulation,
} from "./pixijs_canvas_animation.js";
import { deserialize_fb } from "./flatbuffer_deserializer.js";

// constants
const BINARY_TRANSFER = true;
const BASE_URL = window.location.origin;
const START_URL = BASE_URL + "/start";
const PAUSE_URL = BASE_URL + "/pause";
const RESUME_URL = BASE_URL + "/resume";
const STOP_URL = BASE_URL + "/stop";
const STATE_URL = BASE_URL + "/state" + (BINARY_TRANSFER ? "_fb" : "");
const PARTIAL_STATE_URL =
  BASE_URL + "/partial_state" + (BINARY_TRANSFER ? "_fb" : "");
const RT_FACTOR_BASE_URL = BASE_URL + "/rt_factor?value=";

const CANVAS_WIDTH_URL = BASE_URL + "/width";
const CANVAS_HEIGHT_URL = BASE_URL + "/height";

const ANIMATION_CANVAS_PARENT_ID = "animation_canvas_parent";
let ANIMATION_CANVAS_PARENT;

const running_timeouts = [];
let stopped = false;
let state = {};
let time_of_last_full_update = 0;
const TIME_BETWEEN_FULL_UPDATES_MS = 500;

const LOG_PERFORMANCE = true;
let num_requests = 0;
let num_animation_updates = 0;
let animation_update_times = [];
const LOG_INTERVAL_SEC = 2;

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
  setup_request_state_loop();
  setup_animation_loop();
  if (LOG_PERFORMANCE) log_performance_loop();
}

function log_performance_loop() {
  let interval = window.setInterval(() => {
    console.log("Reqests/sec: " + num_requests / LOG_INTERVAL_SEC);
    console.log("Updates/sec: " + num_animation_updates / LOG_INTERVAL_SEC);
    console.log(
      "Average animation update time (ms): " +
        animation_update_times.reduce((a, b) => a + b, 0) /
          animation_update_times.length
    );
    num_requests = 0;
    num_animation_updates = 0;
    animation_update_times = [];
  }, LOG_INTERVAL_SEC * 1000);
  running_timeouts.push(interval);
}

function setup_request_state_loop() {
  let interval = window.setInterval(state_query, 35);
  running_timeouts.push(interval);
}

async function state_query() {
  if (Date.now() - time_of_last_full_update > TIME_BETWEEN_FULL_UPDATES_MS) {
    // full update
    time_of_last_full_update = Date.now();
    await full_state_update();
  } else {
    // partial update
    await partial_state_update();
  }
  num_requests++;
}

async function full_state_update() {
  const response = await fetch_state();
  state = await deserialize(response);
}

async function partial_state_update() {
  const partial_response = await fetch_partial_state();
  const partial_state = await deserialize(partial_response);
  state = partial_update(state, partial_state);
}

async function fetch_partial_state() {
  return fetch(PARTIAL_STATE_URL);
}

async function fetch_state() {
  return fetch(STATE_URL);
}

async function deserialize(response) {
  return BINARY_TRANSFER ? deserialize_binary(response) : response.json();
}

async function deserialize_binary(response) {
  return deserialize_fb(response);
}

function partial_update(state, partial_state) {
  return Object.assign(state, partial_state);
}

function setup_animation_loop() {
  const minTime = 35;
  let time = Date.now();
  animate_current_state(); // could be further improved by info on actually updated partial state
  time = Date.now() - time;
  if (LOG_PERFORMANCE) animation_update_times.push(time);
  let timeout = Math.max(minTime - time, 0);
  let interval = window.setTimeout(setup_animation_loop, timeout);
  running_timeouts.push(interval);
}

function animate_current_state() {
  animate_simulation(state);
  num_animation_updates++;
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
  value = 101 - value; // 1 - 100
  value /= 100; // 0.01 - 1
  value = Math.pow(value, 3); // exponential speedup
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

// document interaction
document.addEventListener("DOMContentLoaded", () => {
  ANIMATION_CANVAS_PARENT = document.querySelector(
    "#" + ANIMATION_CANVAS_PARENT_ID
  );
  var speed_slider = document.getElementById("speed_slider");
  var speed_label = document.getElementById("speed_label");
  function change_factor(value) {
    speed_label.innerHTML = (1 / speed_slider_changed_to(value)).toFixed(2);
  }
  change_factor(speed_slider.value);
  speed_slider.oninput = function () {
    change_factor(this.value);
  };
});

window.start_simulation = start_simulation;
window.pause_simulation = pause_simulation;
window.resume_simulation = resume_simulation;
window.stop_simulation = stop_simulation;

console.log("animation_client.js loaded");
