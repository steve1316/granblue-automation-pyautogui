import Home from "./pages/Home"
import { BrowserRouter as Router, Route, Switch } from "react-router-dom"
import NavBar from "./components/NavBar"
import Settings from "./pages/Settings"

function App() {
    return (
        <main>
            <Router>
                <NavBar />
                <Switch>
                    <Route path="/" component={Home} exact>
                        <Home />
                    </Route>
                    <Route path="/settings" component={Settings} exact>
                        <Settings />
                    </Route>
                </Switch>
            </Router>
        </main>
    )
}

export default App
