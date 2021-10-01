import React from "react"
import ReactDOM from "react-dom"
import "./index.css"
import App from "./App"
import { invoke } from "@tauri-apps/api/tauri"

// This will wait for the window to load before closing the splashscreen using the following rust command.
document.addEventListener("DOMContentLoaded", () => {
    invoke("close_splashscreen")
})

ReactDOM.render(
    <React.StrictMode>
        <App />
    </React.StrictMode>,
    document.getElementById("root")
)
