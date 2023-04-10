import React from "react"
import ReactDOM from "react-dom"
import App from "./App"

// Do not update to React 18. State updates in batch will break and stdout log will not work properly.
ReactDOM.render(
    <React.StrictMode>
        <App />
    </React.StrictMode>,
    document.getElementById("root")
)
