import { BrowserRouter as Router, Route, Switch } from "react-router-dom"
import NavBar from "./components/NavBar"
import Start from "./components/Start"
import { BotStateProvider } from "./context/BotStateContext"
import { MessageLogProvider } from "./context/MessageLogContext"
import ExtraSettings from "./pages/ExtraSettings"
import Home from "./pages/Home"
import Settings from "./pages/Settings"

function App() {
    return (
        <Router>
            <BotStateProvider>
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
                        <Route path="/extrasettings" exact>
                            <ExtraSettings />
                        </Route>
                    </Switch>
                </MessageLogProvider>
            </BotStateProvider>
        </Router>
    )
}

export default App
