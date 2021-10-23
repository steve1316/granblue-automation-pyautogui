import Home from "./pages/Home"
import { BrowserRouter as Router, Route, Switch } from "react-router-dom"
import NavBar from "./components/NavBar"
import Settings from "./pages/Settings"
import { ReadyProvider } from "./context/ReadyContext"
import { MessageLogProvider } from "./context/MessageLogContext"
import Start from "./components/Start"

function App() {
    return (
        <Router>
            <ReadyProvider>
                <MessageLogProvider>
                    <NavBar />
                    <Start />
                    <Switch>
                        <Route path="/" exact>
                            <Home />
                        </Route>
                        <Route path="/settings" exact>
                            <Settings />
                        </Route>
                    </Switch>
                </MessageLogProvider>
            </ReadyProvider>
        </Router>
    )
}

export default App
