import { useState, useEffect, useContext } from "react"
import { AppShell, Burger, Button, Code, createStyles, Group, Header, MediaQuery, Navbar, ScrollArea, useMantineTheme } from "@mantine/core"
import { getStylesRef, rem } from "@mantine/styles"
import { Icon } from "@iconify/react"
import LinksGroup from "../LinksGroup"
import Home from "../../pages/Home"
import NotFound from "../../pages/NotFound"
import ExtraSettings from "../../pages/ExtraSettings"
import Adjustments from "../../pages/Adjustments"
import Settings from "../../pages/Settings"
import * as app from "@tauri-apps/api/app"
import { BotStateContext } from "../../context/BotStateContext"
import { MessageLogContext } from "../../context/MessageLogContext"
import Ripple from "ripple-button"

const CustomAppShell = () => {
    interface ButtonConfig {
        icon: string
        iconColor: string
        buttonText: string
        buttonTextColor: string
    }

    const theme = useMantineTheme()
    const [active, setActive] = useState("Home")
    const [opened, setOpened] = useState(false)
    const [buttonConfig, setButtonConfig] = useState<ButtonConfig>({
        icon: "material-symbols:error-outline",
        iconColor: "red",
        buttonText: "Not Ready",
        buttonTextColor: "orange",
    })

    const bsc = useContext(BotStateContext)
    const mlc = useContext(MessageLogContext)

    useEffect(() => {
        getVersion()
    }, [])

    useEffect(() => {
        if (bsc.isBotRunning && bsc.readyStatus) {
            setButtonConfig({
                icon: "material-symbols:stop-circle-rounded",
                iconColor: "red",
                buttonText: "Stop",
                buttonTextColor: "white",
            })
        } else if (!bsc.isBotRunning && bsc.readyStatus) {
            setButtonConfig({
                icon: "material-symbols:play-circle-outline-rounded",
                iconColor: "green",
                buttonText: "Press to Start",
                buttonTextColor: "white",
            })
        } else {
            setButtonConfig({
                icon: "material-symbols:error-outline",
                iconColor: "red",
                buttonText: "Not Ready",
                buttonTextColor: "orange",
            })
        }
    }, [bsc.readyStatus, bsc.isBotRunning])

    // Grab the program version.
    const getVersion = async () => {
        await app
            .getVersion()
            .then((version) => {
                console.log(`Current program version is v${version}`)
                bsc.setAppVersion(version)
            })
            .catch(() => {
                bsc.setAppVersion("ERROR")
            })
    }

    const useStyles = createStyles((theme) => ({
        header: {
            paddingBottom: theme.spacing.md,
            marginBottom: `calc(${theme.spacing.md} * 1.5)`,
            borderBottom: `${rem(1)} solid ${theme.colorScheme === "dark" ? theme.colors.dark[4] : theme.colors.gray[2]}`,
        },

        footer: {
            paddingTop: theme.spacing.md,
            marginTop: theme.spacing.md,
            borderTop: `${rem(1)} solid ${theme.colorScheme === "dark" ? theme.colors.dark[4] : theme.colors.gray[2]}`,
        },

        link: {
            ...theme.fn.focusStyles(),
            display: "flex",
            alignItems: "center",
            textDecoration: "none",
            fontSize: theme.fontSizes.sm,
            color: theme.colorScheme === "dark" ? theme.colors.dark[1] : theme.colors.gray[7],
            padding: `${theme.spacing.xs} ${theme.spacing.sm}`,
            borderRadius: theme.radius.sm,
            fontWeight: 500,

            "&:hover": {
                backgroundColor: theme.colorScheme === "dark" ? theme.colors.dark[6] : theme.colors.gray[0],
                color: theme.colorScheme === "dark" ? theme.white : theme.black,

                [`& .${getStylesRef("icon")}`]: {
                    color: theme.colorScheme === "dark" ? theme.white : theme.black,
                },
            },
        },

        linkIcon: {
            ref: getStylesRef("icon"),
            color: theme.colorScheme === "dark" ? theme.colors.dark[2] : theme.colors.gray[6],
            marginRight: theme.spacing.sm,
        },

        linkActive: {
            "&, &:hover": {
                backgroundColor: theme.fn.variant({ variant: "light", color: theme.primaryColor }).background,
                color: theme.fn.variant({ variant: "light", color: theme.primaryColor }).color,
                [`& .${getStylesRef("icon")}`]: {
                    color: theme.fn.variant({ variant: "light", color: theme.primaryColor }).color,
                },
            },
        },
    }))

    const { classes } = useStyles()

    const pages = [
        { label: "Home", value: "Home", link: "/home", frontIcon: "ic:outline-home" },
        { label: "Settings", value: "Settings", link: "/settings", frontIcon: "ic:outline-settings" },
        {
            label: "Extra Settings",
            value: "Extra Settings",
            link: "/extrasettings",
            links: [
                { label: "Twitter", value: "Extra Settings", link: "/extrasettings#twitter" },
                { label: "Discord", value: "Extra Settings", link: "/extrasettings#discord" },
                { label: "Configuration", value: "Extra Settings", link: "/extrasettings#configuration" },
                { label: "Nightmare", value: "Extra Settings", link: "/extrasettings#nightmare" },
                { label: "Misc", value: "Extra Settings", link: "/extrasettings#misc" },
                { label: "Defender", value: "Extra Settings", link: "/extrasettings#defender" },
                { label: "API Integration", value: "Extra Settings", link: "/extrasettings#api-integration" },
                { label: "Device", value: "Extra Settings", link: "/extrasettings#device" },
            ],
            frontIcon: "ic:baseline-settings-suggest",
        },
        {
            label: "Adjustments",
            value: "Adjustments",
            link: "/adjustments",
            links: [
                { label: "Starting Calibration", value: "Adjustments", link: "/adjustments#starting-calibration" },
                { label: "General Image Searching", value: "Adjustments", link: "/adjustments#general-image-searching" },
                { label: "Check for Pending Battles", value: "Adjustments", link: "/adjustments#pending-battles" },
                { label: "Check for CAPTCHA", value: "Adjustments", link: "/adjustments#captcha" },
                { label: "Suppot Summon Selection Screen", value: "Adjustments", link: "/adjustments#support-summons" },
                { label: "Combat Mode", value: "Adjustments", link: "/adjustments#combat-mode" },
                { label: "Arcarum", value: "Adjustments", link: "/adjustments#arcarum" },
            ],
            frontIcon: "ic:outline-display-settings",
        },
    ]

    const renderPage = (value: string) => {
        if (value === "Home") {
            return <Home />
        } else if (value === "Settings") {
            return <Settings />
        } else if (value === "Extra Settings") {
            return <ExtraSettings />
        } else if (value === "Adjustments") {
            return <Adjustments />
        } else {
            return <NotFound />
        }
    }

    const links = pages.map((page) => <LinksGroup {...page} key={page.label} active={active} setActive={setActive} />)

    return (
        <AppShell
            styles={{
                main: {
                    background: theme.colorScheme === "dark" ? theme.colors.dark[8] : theme.colors.gray[0],
                },
            }}
            navbarOffsetBreakpoint="sm"
            navbar={
                <Navbar width={{ sm: 300 }} p="md" hiddenBreakpoint="sm" hidden={!opened}>
                    <Navbar.Section>
                        <Group className={classes.header} position="apart">
                            <Icon icon="logos:mantine-icon" width={25} height={25} />
                            <span>Granblue Automation</span>
                            <Code sx={{ fontWeight: 700 }}>{`v${bsc.appVersion}`}</Code>
                        </Group>
                    </Navbar.Section>

                    <Navbar.Section grow component={ScrollArea}>
                        {links}
                    </Navbar.Section>

                    <Navbar.Section className={classes.footer}>
                        <Group position="apart" spacing={0}>
                            <Ripple
                                color="rgba(226, 229, 241, 0.3)"
                                duration={500}
                                style={{ borderRadius: 8 }}
                                onClick={() => {
                                    if (bsc.isBotRunning) {
                                        bsc.setStartBot(false)
                                        bsc.setStopBot(true)
                                    } else if (bsc.readyStatus) {
                                        mlc.setMessageLog([])
                                        mlc.setAsyncMessages([])
                                        bsc.setStartBot(true)
                                        bsc.setStopBot(false)
                                    }
                                }}
                            >
                                <Button
                                    disabled={!bsc.readyStatus}
                                    p={8}
                                    leftIcon={<Icon icon={buttonConfig.icon} width={25} height={25} color={buttonConfig.iconColor} />}
                                    variant="subtle"
                                    radius={8}
                                >
                                    <span style={{ color: buttonConfig.buttonTextColor }}>{buttonConfig.buttonText}</span>
                                </Button>
                            </Ripple>
                        </Group>
                    </Navbar.Section>
                </Navbar>
            }
            header={
                <MediaQuery largerThan={"sm"} styles={{ display: "none" }}>
                    <Header height={{ base: 50, sm: 0 }} p="md">
                        <div style={{ display: "flex", alignItems: "center", height: "100%" }}>
                            <Burger opened={opened} onClick={() => setOpened(!opened)} size="sm" color={theme.colors.gray[6]} mr="xl" />
                        </div>
                    </Header>
                </MediaQuery>
            }
        >
            {renderPage(active)}
        </AppShell>
    )
}

export default CustomAppShell
