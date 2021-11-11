#![cfg_attr(
  all(not(debug_assertions), target_os = "windows"),
  windows_subsystem = "windows"
)]

use std::time::Duration;
use std::thread::sleep;
use rand::Rng;
use tauri::Manager;
#[tauri::command]
fn close_splashscreen(window: tauri::Window) {
  // Wait a random number of seconds.
  let mut rng = rand::thread_rng();
  sleep(Duration::new(rng.gen_range(1..2), 0));

  // Close splashscreen window.
  if let Some(splashscreen) = window.get_window("splashscreen") {
    splashscreen.close().unwrap();
  }
  // Show main window.
  window.get_window("main").unwrap().show().unwrap();
}

fn main() {
  tauri::Builder::default()
    .invoke_handler(tauri::generate_handler![close_splashscreen])
    .run(tauri::generate_context!())
    .expect("error while running tauri application");
}