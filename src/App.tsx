import { Button, ColorScheme, ColorSchemeProvider, Flex, MantineProvider, Paper, UnstyledButton } from "@mantine/core"
import { useLocalStorage } from "@mantine/hooks"
import { useEffect } from "react"
import CustomAppShell from "./components/CustomAppShell"
import { BotStateProvider } from "./context/BotStateContext"
import { MessageLogProvider } from "./context/MessageLogContext"
import * as app from "@tauri-apps/api/app"
import { emit, listen } from "@tauri-apps/api/event"
import toast, { Toaster } from "react-hot-toast"
import StartHelper from "./helpers/StartHelper"
import { Icon } from "@iconify/react"

const App = () => {
    const [colorScheme, setColorScheme] = useLocalStorage<ColorScheme>({
        key: "mantine-color-scheme",
        defaultValue: "light",
        getInitialValueInEffect: true,
    })
    const toggleColorScheme = (value?: ColorScheme) => setColorScheme(value || (colorScheme === "dark" ? "light" : "dark"))

    // Check if an application update is available on GitHub.
    useEffect(() => {
        // Warn that the application's env is still set to development.
        if (import.meta.env.VITE_APP_ENVIRONMENT === "development") {
            toast.error(
                (t) => (
                    <Flex gap={"lg"} justify="center" align={"center"} direction="row" wrap="nowrap">
                        WARNING: This app is running in development environment.
                        <UnstyledButton onClick={() => toast.dismiss(t.id)} style={{ display: "flex" }}>
                            <Icon icon="fluent:dismiss-12-regular" width={20} height={20} />
                        </UnstyledButton>
                    </Flex>
                ),
                {
                    id: "environment-warning",
                }
            )
        }

        // Listens to the response from the tauri API on if an update is available.
        emit("tauri://update")
        listen("tauri://update-available", (res) => {
            interface Payload {
                body: string
                date: string | null
                version: string
            }

            let payload: Payload = res.payload as Payload
            console.log(`New version available: v${payload.version}`)
            getVersion(payload.version)
        })
    }, [])

    // Grab the program version.
    const getVersion = async (newVersion: string) => {
        await app
            .getVersion()
            .then((version) => {
                toast.success(
                    (t) => (
                        <Flex gap={"lg"} justify="center" align={"center"} direction="row" wrap="nowrap">
                            {`Update available:\nv${version} -> v${newVersion}`}
                            <Button
                                onClick={() => {
                                    window.open("https://github.com/steve1316/granblue-automation-pyautogui/releases", "_blank")
                                    toast.dismiss(t.id)
                                }}
                            >
                                Go to GitHub
                            </Button>
                            <UnstyledButton onClick={() => toast.dismiss(t.id)} style={{ display: "flex" }}>
                                <Icon icon="fluent:dismiss-12-regular" width={20} height={20} />
                            </UnstyledButton>
                        </Flex>
                    ),
                    {
                        id: "update-available",
                    }
                )
            })
            .catch(() => {
                toast.success(
                    (t) => (
                        <Flex gap={"lg"} justify="center" align={"center"} direction="row" wrap="nowrap">
                            {`Update available:`}
                            <Button
                                onClick={() => {
                                    window.open("https://github.com/steve1316/granblue-automation-pyautogui/releases", "_blank")
                                    toast.dismiss(t.id)
                                }}
                            >
                                Go to GitHub
                            </Button>
                            <UnstyledButton onClick={() => toast.dismiss(t.id)} style={{ display: "flex" }}>
                                <Icon icon="fluent:dismiss-12-regular" width={20} height={20} />
                            </UnstyledButton>
                        </Flex>
                    ),
                    {
                        id: "update-available",
                    }
                )
            })
    }

    return (
        <ColorSchemeProvider colorScheme={colorScheme} toggleColorScheme={toggleColorScheme}>
            <MantineProvider theme={{ colorScheme }} withGlobalStyles withNormalizeCSS>
                <BotStateProvider>
                    <MessageLogProvider>
                        <StartHelper />
                        <Paper>
                            <Toaster
                                position="top-center"
                                toastOptions={{
                                    duration: 5000,
                                    style: {
                                        color: "white",
                                        fontSize: 14,
                                    },
                                    success: {
                                        style: {
                                            backgroundColor: "darkgreen",
                                        },
                                    },
                                    error: {
                                        style: {
                                            backgroundColor: "darkred",
                                        },
                                    },
                                }}
                            />
                            <CustomAppShell />
                        </Paper>
                    </MessageLogProvider>
                </BotStateProvider>
            </MantineProvider>
        </ColorSchemeProvider>
    )
}

export default App
