import { useState } from "react"
import { AppBar, Button, ButtonGroup, Divider, Drawer, IconButton, List, ListItem, ListItemIcon, ListItemText, Toolbar, Typography } from "@mui/material"
import { Close, CropSquare, HomeRounded, Menu, Minimize, Settings } from "@mui/icons-material"
import { Link as RouterLink, useHistory } from "react-router-dom"
import "./index.scss"
import { appWindow } from "@tauri-apps/api/window"

const NavBar = () => {
    const history = useHistory()
    const [isDrawerOpen, setIsDrawerOpen] = useState(false)

    const toggleDrawer = () => {
        setIsDrawerOpen(!isDrawerOpen)
    }

    return (
        <AppBar position="static" id="header">
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
                <ButtonGroup variant="outlined">
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
