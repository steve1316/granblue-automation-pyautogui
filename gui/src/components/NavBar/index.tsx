import { useState, useEffect, useContext } from "react"
import { AppBar, Button, ButtonGroup, Divider, Drawer, IconButton, List, ListItem, ListItemIcon, ListItemText, Toolbar, Typography } from "@mui/material"
import { Close, CropSquare, HomeRounded, Menu, Minimize, Settings } from "@mui/icons-material"
import { Link as RouterLink, useHistory } from "react-router-dom"
import "./index.scss"
import { appWindow } from "@tauri-apps/api/window"
import { ReadyContext } from "../../context/ReadyContext"

const NavBar = () => {
    const history = useHistory()
    const [isDrawerOpen, setIsDrawerOpen] = useState(false)
    const [readyStatus, setReadyStatus] = useState("Status: Not Ready")

    const { status } = useContext(ReadyContext)
    useEffect(() => {
        if (status) {
            setReadyStatus("Status: Ready")
        } else {
            setReadyStatus("Status: Not Ready")
        }
    }, [status])

    const toggleDrawer = () => {
        setIsDrawerOpen(!isDrawerOpen)
    }

    return (
        <AppBar position="fixed" id="header">
            <Toolbar variant="dense" className="toolbar" data-tauri-drag-region>
                <IconButton className="menuButton" size="large" edge="start" color="inherit" aria-label="menu" sx={{ mr: 2 }} onClick={toggleDrawer}>
                    <Menu />
                </IconButton>
                <Drawer anchor="left" open={isDrawerOpen} onClose={toggleDrawer}>
                    <List className="list">
                        <RouterLink to="/" className="link">
                            <ListItem button key="home">
                                <ListItemIcon>
                                    <HomeRounded />
                                </ListItemIcon>
                                <ListItemText primary="Home" />
                            </ListItem>
                            <Divider />
                        </RouterLink>
                        <RouterLink to="/settings" className="link">
                            <ListItem button key="settings">
                                <ListItemIcon>
                                    <Settings />
                                </ListItemIcon>
                                <ListItemText primary="Settings" />
                            </ListItem>
                            <Divider />
                        </RouterLink>
                    </List>
                </Drawer>
                <Typography
                    variant="h6"
                    className="title"
                    onClick={() => {
                        history.push("/")
                    }}
                >
                    Granblue Automation
                </Typography>
                <div className="emptyDivider" />
                {status ? (
                    <Typography variant="caption" sx={{ display: "flex", flexDirection: "column", justifyContent: "flex-end", marginRight: "10px", color: "#76ff03" }}>
                        {readyStatus}
                    </Typography>
                ) : (
                    <Typography variant="caption" sx={{ display: "flex", flexDirection: "column", justifyContent: "flex-end", marginRight: "10px", color: "red" }}>
                        {readyStatus}
                    </Typography>
                )}
                <ButtonGroup variant="outlined" className="group">
                    <Button
                        className="navButton"
                        onClick={() =>
                            setTimeout(() => {
                                appWindow.minimize()
                            }, 125)
                        }
                    >
                        <Minimize />
                    </Button>
                    <Button
                        className="navButton"
                        onClick={() =>
                            setTimeout(() => {
                                appWindow.toggleMaximize()
                            }, 125)
                        }
                    >
                        <CropSquare />
                    </Button>
                    <Button
                        className="navButton"
                        onClick={() =>
                            setTimeout(() => {
                                appWindow.close()
                            }, 125)
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
