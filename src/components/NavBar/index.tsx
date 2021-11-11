import { Close, CropSquare, HomeRounded, Menu, Minimize, Settings, SettingsSuggest } from "@mui/icons-material"
import { Alert, AppBar, Button, ButtonGroup, Divider, Drawer, IconButton, List, ListItem, ListItemIcon, ListItemText, Snackbar, Toolbar, Typography } from "@mui/material"
import * as app from "@tauri-apps/api/app"
import { appWindow } from "@tauri-apps/api/window"
import { useContext, useEffect, useState } from "react"
import { Link as RouterLink, useHistory } from "react-router-dom"
import { BotStateContext } from "../../context/BotStateContext"
import "./index.scss"

const NavBar = () => {
    const history = useHistory()
    const [isDrawerOpen, setIsDrawerOpen] = useState<boolean>(false)
    const [version, setVersion] = useState<string>("")

    const botStateContext = useContext(BotStateContext)

    useEffect(() => {
        getVersion()
    }, [])

    // Grab the program version.
    const getVersion = async () => {
        await app
            .getVersion()
            .then((version) => {
                console.log("Version is ", version)
                setVersion(version)
            })
            .catch(() => {
                setVersion("failed to get version")
            })
    }

    // Warn the user about refreshing the page.
    window.onbeforeunload = function (e) {
        if (botStateContext.refreshAlert) {
            return false
        }
    }

    // This event listener will fire before the onbeforeunload. This is so the Snackbar can show itself before the window popup appears.
    window.addEventListener("keydown", function (e) {
        if (e.key === "F5") {
            botStateContext.setRefreshAlert(true)
        }
    })

    const toggleDrawer = () => {
        setIsDrawerOpen(!isDrawerOpen)
    }

    return (
        <AppBar position="fixed" id="header">
            <Snackbar
                open={botStateContext.refreshAlert}
                anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
                autoHideDuration={10000}
                onClose={() => botStateContext.setRefreshAlert(false)}
                onClick={() => botStateContext.setRefreshAlert(false)}
            >
                <Alert severity="error">Do NOT reload/F5/refresh the "page" while the bot is RUNNING. You will have a runaway program.</Alert>
            </Snackbar>
            <Toolbar variant="dense" className="navToolbar" data-tauri-drag-region>
                <IconButton className="navMenuButton" size="large" edge="start" color="inherit" aria-label="menu" sx={{ mr: 2 }} onClick={toggleDrawer}>
                    <Menu />
                </IconButton>
                <Drawer anchor="left" open={isDrawerOpen} onClose={toggleDrawer}>
                    <List className="navList">
                        <RouterLink to="/" className="navLink">
                            <ListItem button key="home">
                                <ListItemIcon>
                                    <HomeRounded />
                                </ListItemIcon>
                                <ListItemText primary="Home" />
                            </ListItem>
                            <Divider />
                        </RouterLink>
                        <RouterLink to="/settings" className="navLink">
                            <ListItem button key="settings">
                                <ListItemIcon>
                                    <Settings />
                                </ListItemIcon>
                                <ListItemText primary="Settings" />
                            </ListItem>
                            <Divider />
                        </RouterLink>
                        <RouterLink to="/extrasettings" className="navLink">
                            <ListItem button key="extrasettings">
                                <ListItemIcon>
                                    <SettingsSuggest />
                                </ListItemIcon>
                                <ListItemText primary="Extra Settings" />
                            </ListItem>
                            <Divider />
                        </RouterLink>
                    </List>
                </Drawer>
                <Typography
                    variant="h6"
                    className="navTitle"
                    onClick={() => {
                        history.push("/")
                    }}
                >
                    Granblue Automation <Typography variant="caption">v{version}</Typography>
                </Typography>
                <div className="emptyDivider" />
                {botStateContext.isBotRunning ? (
                    <Typography variant="caption" sx={{ display: "flex", flexDirection: "column", justifyContent: "flex-end", marginRight: "10px", color: "#FFEB3B" }}>
                        Status: Running
                    </Typography>
                ) : botStateContext.readyStatus ? (
                    <Typography variant="caption" sx={{ display: "flex", flexDirection: "column", justifyContent: "flex-end", marginRight: "10px", color: "#76ff03" }}>
                        Status: Ready
                    </Typography>
                ) : (
                    <Typography variant="caption" sx={{ display: "flex", flexDirection: "column", justifyContent: "flex-end", marginRight: "10px", color: "red" }}>
                        Status: Not Ready
                    </Typography>
                )}
                <ButtonGroup variant="outlined" className="navGroup">
                    <Button
                        className="navButton"
                        onClick={() =>
                            setTimeout(() => {
                                appWindow.minimize()
                            }, 100)
                        }
                    >
                        <Minimize />
                    </Button>
                    <Button
                        className="navButton"
                        onClick={() =>
                            setTimeout(() => {
                                appWindow.toggleMaximize()
                            }, 100)
                        }
                    >
                        <CropSquare />
                    </Button>
                    <Button
                        className="navButton"
                        onClick={() =>
                            setTimeout(() => {
                                appWindow.close()
                            }, 100)
                        }
                    >
                        <Close />
                    </Button>
                </ButtonGroup>
            </Toolbar>
        </AppBar>
    )
}

export default NavBar
