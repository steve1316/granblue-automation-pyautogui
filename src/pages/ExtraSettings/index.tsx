import { Icon as Iconify } from "@iconify/react"
import { Speed } from "@mui/icons-material"
import {
    Alert,
    Button,
    Checkbox,
    CircularProgress,
    Divider,
    Fade,
    FormControlLabel,
    FormGroup,
    FormHelperText,
    Grid,
    InputAdornment,
    Modal,
    Snackbar,
    Stack,
    TextField,
    Typography,
} from "@mui/material"
import { Box, styled } from "@mui/system"
import { Command } from "@tauri-apps/api/shell"
import { useContext, useRef, useState } from "react"
import TransferList from "../../components/TransferList"
import { BotStateContext } from "../../context/BotStateContext"
import { readTextFile } from "@tauri-apps/api/fs"
import { open, DialogFilter } from "@tauri-apps/api/dialog"
import "./index.scss"
import axios, { AxiosError } from "axios"

// Custom input component for combat script file selection.
const Input = styled("input")({
    display: "none",
})

const ExtraSettings = () => {
    const [testPID, setTestPID] = useState(0)
    const [isModalOpen, setIsModalOpen] = useState<boolean>(false)
    const [showSnackbar, setShowSnackbar] = useState<boolean>(false)
    const [testInProgress, setTestInProgress] = useState<boolean>(false)
    const [testFailed, setTestFailed] = useState<boolean>(false)
    const [testErrorMessage, setTestErrorMessage] = useState<string>("")

    const bsc = useContext(BotStateContext)

    const inputRef = useRef<HTMLInputElement>(null)

    // Load the selected combat script text file.
    const loadNightmareCombatScript = (event: React.ChangeEvent<HTMLInputElement>) => {
        var files = event.currentTarget.files
        if (files !== null && files.length !== 0) {
            var selectedFile = files[0]
            if (selectedFile === null || selectedFile === undefined) {
                // Reset the nightmare combat script selected if none was selected from the file picker dialog.
                bsc.setSettings({ ...bsc.settings, nightmare: { ...bsc.settings.nightmare, nightmareCombatScriptName: "", nightmareCombatScript: [] } })
            } else {
                // Create the FileReader object and setup the function that will run after the FileReader reads the text file.
                var reader = new FileReader()
                reader.onload = function (loadedEvent) {
                    if (loadedEvent.target?.result !== null && loadedEvent.target?.result !== undefined) {
                        console.log("Loaded Nightmare Combat Script: ", loadedEvent.target.result)
                        const newCombatScript: string[] = loadedEvent.target.result.toString().split("\r\n")
                        bsc.setSettings({ ...bsc.settings, nightmare: { ...bsc.settings.nightmare, nightmareCombatScriptName: selectedFile.name, nightmareCombatScript: newCombatScript } })
                    } else {
                        console.log("Failed to read Nightmare combat script. Reseting to default empty combat script...")
                        bsc.setSettings({ ...bsc.settings, nightmare: { ...bsc.settings.nightmare, nightmareCombatScriptName: "", nightmareCombatScript: [] } })
                    }
                }

                // Read the text contents of the file.
                reader.readAsText(selectedFile)
            }
        } else {
            console.log("No file selected. Reseting to default empty combat script...")
            bsc.setSettings({ ...bsc.settings, nightmare: { ...bsc.settings.nightmare, nightmareCombatScriptName: "", nightmareCombatScript: [] } })
        }
    }

    const loadNightmareCombatScriptAlternative = () => {
        // Use an alternative file picker for selecting the combat script.
        let filter: DialogFilter = {
            extensions: ["txt"],
            name: "Combat Script filter",
        }

        open({ defaultPath: undefined, filters: [filter], multiple: false })
            .then((filePath) => {
                if (typeof filePath === "string") {
                    readTextFile(filePath)
                        .then((data) => {
                            console.log("Loaded Nightmare Combat Script via alternative method: ", data)
                            const newCombatScript: string[] = data
                                .toString()
                                .replace(/\r\n/g, "\n") // Replace LF with CRLF.
                                .replace(/[\r\n]/g, "\n")
                                .replace("\t", "") // Replace tab characters.
                                .replace(/\t/g, "")
                                .split("\n")
                            bsc.setSettings({
                                ...bsc.settings,
                                nightmare: { ...bsc.settings.nightmare, nightmareCombatScriptName: filePath.replace(/^.*[\\/]/, ""), nightmareCombatScript: newCombatScript },
                            })
                        })
                        .catch((err) => {
                            console.log(`Failed to read Nightmare combat script via alternative method: ${err}\n\nReseting to default empty combat script...`)
                            bsc.setSettings({ ...bsc.settings, nightmare: { ...bsc.settings.nightmare, nightmareCombatScriptName: "", nightmareCombatScript: [] } })
                        })
                } else {
                    console.log(`No file selected.\n\nReseting to default empty combat script...`)
                    bsc.setSettings({ ...bsc.settings, nightmare: { ...bsc.settings.nightmare, nightmareCombatScriptName: "", nightmareCombatScript: [] } })
                }
            })
            .catch((e) => {
                console.log("Error while resolving the path to the combat script: ", e)
            })
    }

    // Load the selected combat script text file.
    const loadDefenderCombatScript = (event: React.ChangeEvent<HTMLInputElement>) => {
        var files = event.currentTarget.files
        if (files !== null && files.length !== 0) {
            var selectedFile = files[0]
            if (selectedFile === null || selectedFile === undefined) {
                // Reset the defender combat script selected if none was selected from the file picker dialog.
                bsc.setSettings({ ...bsc.settings, sandbox: { ...bsc.settings.sandbox, defenderCombatScriptName: "", defenderCombatScript: [] } })
            } else {
                // Create the FileReader object and setup the function that will run after the FileReader reads the text file.
                var reader = new FileReader()
                reader.onload = function (loadedEvent) {
                    if (loadedEvent.target?.result !== null && loadedEvent.target?.result !== undefined) {
                        console.log("Loaded Sandbox Defender Combat Script: ", loadedEvent.target.result)
                        const newCombatScript: string[] = loadedEvent.target.result.toString().split("\r\n")
                        bsc.setSettings({ ...bsc.settings, sandbox: { ...bsc.settings.sandbox, defenderCombatScriptName: selectedFile.name, defenderCombatScript: newCombatScript } })
                    } else {
                        console.log("Failed to read Sandbox Defender combat script. Reseting to default empty combat script...")
                        bsc.setSettings({ ...bsc.settings, sandbox: { ...bsc.settings.sandbox, defenderCombatScriptName: "", defenderCombatScript: [] } })
                    }
                }

                // Read the text contents of the file.
                reader.readAsText(selectedFile)
            }
        } else {
            console.log("No file selected. Reseting to default empty combat script...")
            bsc.setSettings({ ...bsc.settings, sandbox: { ...bsc.settings.sandbox, defenderCombatScriptName: "", defenderCombatScript: [] } })
        }
    }

    const loadDefenderCombatScriptAlternative = () => {
        // Use an alternative file picker for selecting the combat script.
        let filter: DialogFilter = {
            extensions: ["txt"],
            name: "Combat Script filter",
        }

        open({ defaultPath: undefined, filters: [filter], multiple: false })
            .then((filePath) => {
                if (typeof filePath === "string") {
                    readTextFile(filePath)
                        .then((data) => {
                            console.log("Loaded Sandbox Defender Combat Script via alternative method: ", data)
                            const newCombatScript: string[] = data
                                .toString()
                                .replace(/\r\n/g, "\n") // Replace LF with CRLF.
                                .replace(/[\r\n]/g, "\n")
                                .replace("\t", "") // Replace tab characters.
                                .replace(/\t/g, "")
                                .split("\n")
                            bsc.setSettings({
                                ...bsc.settings,
                                sandbox: { ...bsc.settings.sandbox, defenderCombatScriptName: filePath.replace(/^.*[\\/]/, ""), defenderCombatScript: newCombatScript },
                            })
                        })
                        .catch((err) => {
                            console.log(`Failed to read Sandbox Defender combat script via alternative method: ${err}\n\nReseting to default empty combat script...`)
                            bsc.setSettings({ ...bsc.settings, sandbox: { ...bsc.settings.sandbox, defenderCombatScriptName: "", defenderCombatScript: [] } })
                        })
                } else {
                    console.log(`No file selected.\n\nReseting to default empty combat script...`)
                    bsc.setSettings({ ...bsc.settings, sandbox: { ...bsc.settings.sandbox, defenderCombatScriptName: "", defenderCombatScript: [] } })
                }
            })
            .catch((e) => {
                console.log("Error while resolving the path to the combat script: ", e)
            })
    }

    // Render settings for Twitter.
    const renderTwitterSettings = () => {
        return (
            <div id="twitter">
                <Typography variant="h6" gutterBottom component="div" className="sectionTitle">
                    Twitter Settings <Iconify icon="akar-icons:twitter-fill" className="twitterTitleIcon" />
                </Typography>

                <Divider />

                <Typography variant="subtitle1" gutterBottom component="div" color="text.secondary">
                    Please visit the wiki on the GitHub page for instructions on how to get these keys and tokens.
                </Typography>

                <FormGroup sx={{ paddingBottom: "16px" }}>
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={bsc.settings.twitter.twitterUseVersion2}
                                onChange={(e) => {
                                    bsc.setSettings({ ...bsc.settings, twitter: { ...bsc.settings.twitter, twitterUseVersion2: e.target.checked } })
                                }}
                            />
                        }
                        label="Enable if using Twitter API V2. Disable if using V1.1"
                    />
                    <FormHelperText>If enabled, then only the bearer token will be needed. No need for the consumer keys and such.</FormHelperText>
                </FormGroup>

                <Grid container spacing={2} direction="row" justifyContent="center" alignItems="center">
                    {!bsc.settings.twitter.twitterUseVersion2 ? (
                        <>
                            <Grid item xs={6}>
                                <TextField
                                    label="API Key"
                                    value={bsc.settings.twitter.twitterAPIKey}
                                    onChange={(e) => bsc.setSettings({ ...bsc.settings, twitter: { ...bsc.settings.twitter, twitterAPIKey: e.target.value } })}
                                    placeholder="Insert API Key here"
                                    multiline
                                    variant="filled"
                                    fullWidth
                                />
                            </Grid>

                            <Grid item xs={6}>
                                <TextField
                                    label="API Key Secret"
                                    value={bsc.settings.twitter.twitterAPIKeySecret}
                                    onChange={(e) => bsc.setSettings({ ...bsc.settings, twitter: { ...bsc.settings.twitter, twitterAPIKeySecret: e.target.value } })}
                                    placeholder="Insert API Key Secret here"
                                    multiline
                                    variant="filled"
                                    fullWidth
                                />
                            </Grid>

                            <Grid item xs={6}>
                                <TextField
                                    label="Access Token"
                                    value={bsc.settings.twitter.twitterAccessToken}
                                    onChange={(e) => bsc.setSettings({ ...bsc.settings, twitter: { ...bsc.settings.twitter, twitterAccessToken: e.target.value } })}
                                    placeholder="Insert Access Token here"
                                    multiline
                                    variant="filled"
                                    fullWidth
                                />
                            </Grid>

                            <Grid item xs={6}>
                                <TextField
                                    label="Access Token Secret"
                                    value={bsc.settings.twitter.twitterAccessTokenSecret}
                                    onChange={(e) => bsc.setSettings({ ...bsc.settings, twitter: { ...bsc.settings.twitter, twitterAccessTokenSecret: e.target.value } })}
                                    placeholder="Insert Access Token Secret here"
                                    multiline
                                    variant="filled"
                                    fullWidth
                                />
                            </Grid>
                        </>
                    ) : (
                        <Grid item xs={12}>
                            <TextField
                                label="Bearer Token"
                                value={bsc.settings.twitter.twitterBearerToken}
                                onChange={(e) => bsc.setSettings({ ...bsc.settings, twitter: { ...bsc.settings.twitter, twitterBearerToken: e.target.value } })}
                                placeholder="Insert Bearer Token here"
                                multiline
                                variant="filled"
                                fullWidth
                            />
                        </Grid>
                    )}

                    <Grid item>
                        <Box sx={{ m: 1, position: "relative" }}>
                            <Button variant="contained" startIcon={<Speed />} className="twitterButton" onClick={() => testTwitter()} disabled={testInProgress}>
                                Test Twitter API
                            </Button>
                            {testInProgress && (
                                <CircularProgress
                                    size={24}
                                    sx={{
                                        position: "absolute",
                                        top: "50%",
                                        left: "50%",
                                        marginTop: "-12px",
                                        marginLeft: "-12px",
                                    }}
                                />
                            )}
                        </Box>
                    </Grid>
                </Grid>
            </div>
        )
    }

    // Render settings for Discord.
    const renderDiscordSettings = () => {
        return (
            <div id="discord">
                <Typography variant="h6" gutterBottom component="div" className="sectionTitle">
                    Discord Settings <Iconify icon="akar-icons:discord-fill" className="discordTitleIcon" />
                </Typography>

                <Divider />

                <Typography variant="subtitle1" gutterBottom component="div" color="text.secondary">
                    Please visit the wiki on the GitHub page for instructions on how to get the token and user ID.
                </Typography>

                <FormGroup sx={{ paddingBottom: "16px" }}>
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={bsc.settings.discord.enableDiscordNotifications}
                                onChange={(e) => bsc.setSettings({ ...bsc.settings, discord: { ...bsc.settings.discord, enableDiscordNotifications: e.target.checked } })}
                            />
                        }
                        label="Enable Discord Notifications"
                    />
                    <FormHelperText>Enable notifications of loot drops and errors encountered by the bot via Discord DMs.</FormHelperText>
                </FormGroup>

                <Grid container spacing={2} direction="row" justifyContent="center" alignItems="center">
                    <Grid item xs={6}>
                        <TextField
                            label="Discord Token"
                            value={bsc.settings.discord.discordToken}
                            onChange={(e) => bsc.setSettings({ ...bsc.settings, discord: { ...bsc.settings.discord, discordToken: e.target.value } })}
                            placeholder="Insert Discord Token here"
                            multiline
                            variant="filled"
                            fullWidth
                        />
                    </Grid>

                    <Grid item xs={6}>
                        <TextField
                            label="User ID"
                            value={bsc.settings.discord.discordUserID}
                            onChange={(e) => bsc.setSettings({ ...bsc.settings, discord: { ...bsc.settings.discord, discordUserID: e.target.value } })}
                            placeholder="Insert User ID here"
                            multiline
                            variant="filled"
                            fullWidth
                        />
                    </Grid>

                    <Grid item>
                        <Box sx={{ m: 1, position: "relative" }}>
                            <Button variant="contained" startIcon={<Speed />} className="twitterButton" onClick={() => testDiscord()} disabled={testInProgress}>
                                Test Discord API
                            </Button>
                            {testInProgress && (
                                <CircularProgress
                                    size={24}
                                    sx={{
                                        position: "absolute",
                                        top: "50%",
                                        left: "50%",
                                        marginTop: "-12px",
                                        marginLeft: "-12px",
                                    }}
                                />
                            )}
                        </Box>
                    </Grid>
                </Grid>
            </div>
        )
    }

    // Render settings for Configuration.
    const renderConfigurationSettings = () => {
        return (
            <div id="configuration">
                <Typography variant="h6" gutterBottom component="div" className="sectionTitle">
                    Configuration Settings <Iconify icon="icon-park-outline:setting-config" className="sectionTitleIcon" />
                </Typography>

                <Divider />

                <br />

                <Typography variant="subtitle1" gutterBottom component="div" color="text.secondary">
                    The following setting below is useful if you have a fast enough connection that pages load almost instantly. If the amount selected reduces the delay to the negatives, then it will
                    default back to its original delay. Beware that changing this setting may lead to unintended behavior as the bot will be going faster, depending on how much you reduce each delay
                    by.
                </Typography>

                <br />

                <Grid container spacing={2} direction="row" justifyContent="center" alignItems="center">
                    <Grid item xs={6}>
                        <TextField
                            label="Reduce Delays by X Seconds"
                            value={bsc.settings.configuration.reduceDelaySeconds}
                            onChange={(e) => bsc.setSettings({ ...bsc.settings, configuration: { ...bsc.settings.configuration, reduceDelaySeconds: Number(e.target.value) } })}
                            variant="outlined"
                            type="number"
                            inputProps={{ min: 0.0, step: 0.1 }}
                            InputProps={{
                                endAdornment: <InputAdornment position="end">seconds</InputAdornment>,
                            }}
                            helperText="Reduces each delay across the whole application by X amount of seconds."
                            fullWidth
                        />
                    </Grid>

                    <Grid item xs={6} />
                </Grid>

                <Divider />

                <FormGroup sx={{ paddingBottom: "16px" }}>
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={bsc.settings.configuration.enableBezierCurveMouseMovement}
                                onChange={(e) => bsc.setSettings({ ...bsc.settings, configuration: { ...bsc.settings.configuration, enableBezierCurveMouseMovement: e.target.checked } })}
                            />
                        }
                        label="Enable Bezier Curve Mouse Movement"
                    />
                    <FormHelperText>
                        Enable this option to have slow but human-like mouse movement. Disable this for fast but bot-like mouse movement. Note that enabling this will disable the Mouse Speed setting.
                    </FormHelperText>
                </FormGroup>

                <Grid container spacing={2} direction="row" justifyContent="center" alignItems="center">
                    <Grid item xs={6}>
                        <TextField
                            label="Mouse Speed"
                            value={bsc.settings.configuration.mouseSpeed}
                            onChange={(e) => bsc.setSettings({ ...bsc.settings, configuration: { ...bsc.settings.configuration, mouseSpeed: Number(e.target.value) } })}
                            variant="outlined"
                            type="number"
                            inputProps={{ min: 0, step: 0.1 }}
                            InputProps={{
                                endAdornment: <InputAdornment position="end">seconds</InputAdornment>,
                            }}
                            helperText="Set how fast a mouse operation finishes."
                            disabled={bsc.settings.configuration.enableBezierCurveMouseMovement}
                            fullWidth
                        />
                    </Grid>

                    <Grid item xs={6} />
                </Grid>

                <FormGroup sx={{ paddingBottom: "16px" }}>
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={bsc.settings.configuration.enableDelayBetweenRuns}
                                onChange={(e) => {
                                    if (e.target.checked && bsc.settings.configuration.enableRandomizedDelayBetweenRuns) {
                                        bsc.setSettings({ ...bsc.settings, configuration: { ...bsc.settings.configuration, enableRandomizedDelayBetweenRuns: false } })
                                    }

                                    bsc.setSettings({ ...bsc.settings, configuration: { ...bsc.settings.configuration, enableDelayBetweenRuns: e.target.checked } })
                                }}
                            />
                        }
                        label="Enable Delay Between Runs"
                    />
                    <FormHelperText>Enable delay in seconds between runs to serve as a resting period.</FormHelperText>
                </FormGroup>

                {bsc.settings.configuration.enableDelayBetweenRuns && !bsc.settings.configuration.enableRandomizedDelayBetweenRuns ? (
                    <Grid container spacing={2} direction="row" justifyContent="center" alignItems="center">
                        <Grid item xs={6}>
                            <TextField
                                label="Delay In Seconds"
                                value={bsc.settings.configuration.delayBetweenRuns}
                                onChange={(e) => bsc.setSettings({ ...bsc.settings, configuration: { ...bsc.settings.configuration, delayBetweenRuns: Number(e.target.value) } })}
                                variant="outlined"
                                type="number"
                                inputProps={{ min: 1 }}
                                InputProps={{
                                    endAdornment: <InputAdornment position="end">seconds</InputAdornment>,
                                }}
                                helperText="Set the delay in seconds for the resting period."
                                fullWidth
                            />
                        </Grid>

                        <Grid item xs={6} />
                    </Grid>
                ) : null}

                <FormGroup sx={{ paddingBottom: "16px" }}>
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={bsc.settings.configuration.enableRandomizedDelayBetweenRuns}
                                onChange={(e) => {
                                    if (e.target.checked && bsc.settings.configuration.enableDelayBetweenRuns) {
                                        bsc.setSettings({ ...bsc.settings, configuration: { ...bsc.settings.configuration, enableDelayBetweenRuns: false } })
                                    }

                                    bsc.setSettings({ ...bsc.settings, configuration: { ...bsc.settings.configuration, enableRandomizedDelayBetweenRuns: e.target.checked } })
                                }}
                            />
                        }
                        label="Enable Randomized Delay Between Runs"
                    />
                    <FormHelperText>Enable randomized delay in seconds between runs to serve as a resting period.</FormHelperText>
                </FormGroup>

                {!bsc.settings.configuration.enableDelayBetweenRuns && bsc.settings.configuration.enableRandomizedDelayBetweenRuns ? (
                    <Grid container spacing={2} direction="row" justifyContent="center" alignItems="center">
                        <Grid item xs={6}>
                            <TextField
                                label="Delay In Seconds Lower Bound"
                                value={bsc.settings.configuration.delayBetweenRunsLowerBound}
                                onChange={(e) => {
                                    // Perform validation so that the value does not violate the opposing bound.
                                    if (Number(e.target.value) > bsc.settings.configuration.delayBetweenRunsUpperBound) {
                                        bsc.setSettings({
                                            ...bsc.settings,
                                            configuration: { ...bsc.settings.configuration, delayBetweenRunsLowerBound: bsc.settings.configuration.delayBetweenRunsUpperBound },
                                        })
                                    } else {
                                        bsc.setSettings({ ...bsc.settings, configuration: { ...bsc.settings.configuration, delayBetweenRunsLowerBound: Number(e.target.value) } })
                                    }
                                }}
                                variant="outlined"
                                type="number"
                                inputProps={{ min: 1 }}
                                InputProps={{
                                    endAdornment: <InputAdornment position="end">seconds</InputAdornment>,
                                }}
                                helperText="Set the Lower Bound for the resting period."
                                fullWidth
                            />
                        </Grid>

                        <Grid item xs={6}>
                            <TextField
                                label="Delay In Seconds Upper Bound"
                                value={bsc.settings.configuration.delayBetweenRunsUpperBound}
                                onChange={(e) => {
                                    // Perform validation so that the value does not violate the opposing bound.
                                    if (Number(e.target.value) < bsc.settings.configuration.delayBetweenRunsLowerBound) {
                                        bsc.setSettings({
                                            ...bsc.settings,
                                            configuration: { ...bsc.settings.configuration, delayBetweenRunsUpperBound: bsc.settings.configuration.delayBetweenRunsLowerBound },
                                        })
                                    } else {
                                        bsc.setSettings({ ...bsc.settings, configuration: { ...bsc.settings.configuration, delayBetweenRunsUpperBound: Number(e.target.value) } })
                                    }
                                }}
                                variant="outlined"
                                type="number"
                                inputProps={{ min: 1 }}
                                InputProps={{
                                    endAdornment: <InputAdornment position="end">seconds</InputAdornment>,
                                }}
                                helperText="Set the Upper Bound for the resting period."
                                fullWidth
                            />
                        </Grid>
                    </Grid>
                ) : null}

                <FormGroup sx={{ paddingBottom: "16px" }}>
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={bsc.settings.raid.enableAutoExitRaid}
                                onChange={(e) => {
                                    bsc.setSettings({ ...bsc.settings, raid: { ...bsc.settings.raid, enableAutoExitRaid: e.target.checked } })
                                }}
                            />
                        }
                        label="Enable Auto Exiting Raids"
                    />
                    <FormHelperText>Enables backing out of a Raid without retreating while under Semi/Full Auto after a certain period of time has passed.</FormHelperText>
                </FormGroup>

                {bsc.settings.raid.enableAutoExitRaid ? (
                    <Grid container spacing={2} direction="row" justifyContent="center" alignItems="center">
                        <Grid item xs={6}>
                            <TextField
                                label="Max Time Allowed for Semi/Full Auto"
                                value={bsc.settings.raid.timeAllowedUntilAutoExitRaid}
                                onChange={(e) => {
                                    bsc.setSettings({ ...bsc.settings, raid: { ...bsc.settings.raid, timeAllowedUntilAutoExitRaid: Number(e.target.value) } })
                                }}
                                variant="outlined"
                                type="number"
                                inputProps={{ min: 1, max: 15 }}
                                InputProps={{
                                    endAdornment: <InputAdornment position="end">minutes</InputAdornment>,
                                }}
                                helperText="Set the maximum amount of minutes to be in a Raid while under Semi/Full Auto before moving on to the next Raid."
                                fullWidth
                            />
                        </Grid>
                        <Grid item xs={6} />
                    </Grid>
                ) : null}

                <FormGroup sx={{ paddingBottom: "16px" }}>
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={bsc.settings.raid.enableNoTimeout}
                                onChange={(e) => {
                                    bsc.setSettings({ ...bsc.settings, raid: { ...bsc.settings.raid, enableNoTimeout: e.target.checked } })
                                }}
                            />
                        }
                        label="Enable No Timeout"
                    />
                    <FormHelperText>Enable no timeouts when attempting to farm Raids that appear infrequently.</FormHelperText>
                </FormGroup>

                <FormGroup sx={{ paddingBottom: "16px" }}>
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={bsc.settings.configuration.enableRefreshDuringCombat}
                                onChange={(e) => {
                                    bsc.setSettings({ ...bsc.settings, configuration: { ...bsc.settings.configuration, enableRefreshDuringCombat: e.target.checked } })
                                }}
                            />
                        }
                        label="Enable Refreshing during Combat"
                    />
                    <FormHelperText>
                        Enables the ability to refresh to speed up Combat Mode whenever the Attack button disappears when it is pressed or during Full/Semi Auto. This option takes precedence above any
                        other related setting to reloading during combat except via the reload command in a script.
                    </FormHelperText>
                </FormGroup>

                <FormGroup sx={{ paddingBottom: "16px" }}>
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={bsc.settings.configuration.enableAutoQuickSummon}
                                onChange={(e) => {
                                    bsc.setSettings({ ...bsc.settings, configuration: { ...bsc.settings.configuration, enableAutoQuickSummon: e.target.checked } })
                                }}
                            />
                        }
                        label="Enable Automatic Quick Summon during Full/Semi Auto"
                    />
                    <FormHelperText>
                        Enables the ability to automatically use Quick Summon during Full/Semi Auto. Note that this option only takes into effect when "Enable Refreshing during Combat" is turned on
                        and that the bot is fighting a battle that is compatible with refreshing during combat.
                    </FormHelperText>
                </FormGroup>

                <FormGroup sx={{ paddingBottom: "16px" }}>
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={bsc.settings.configuration.enableBypassResetSummon}
                                onChange={(e) => {
                                    bsc.setSettings({ ...bsc.settings, configuration: { ...bsc.settings.configuration, enableBypassResetSummon: e.target.checked } })
                                }}
                            />
                        }
                        label="Enable Bypassing Reset Summon Procedure"
                    />
                    <FormHelperText>
                        Enables bypassing the bot resetting Summons if there are none of your chosen found during Summon Selection. The bot will reload the page and select the very first summon at the
                        top of the list.
                    </FormHelperText>
                </FormGroup>

                <FormGroup sx={{ paddingBottom: "16px" }}>
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={bsc.settings.configuration.staticWindow}
                                onChange={(e) => {
                                    bsc.setSettings({ ...bsc.settings, configuration: { ...bsc.settings.configuration, staticWindow: e.target.checked } })
                                }}
                            />
                        }
                        label="Enable static window calibration"
                    />
                    <FormHelperText>
                        Enable calibration of game window to be static. This will assume that you do not move the game window around during the bot process. Otherwise, the bot will not see where to go
                        next. Disable to have the whole computer screen act as the game window and you can move around the window during the bot process as you wish.
                    </FormHelperText>
                </FormGroup>

                <FormGroup sx={{ paddingBottom: "16px" }}>
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={bsc.settings.configuration.enableMouseSecurityAttemptBypass}
                                onChange={(e) => {
                                    bsc.setSettings({ ...bsc.settings, configuration: { ...bsc.settings.configuration, enableMouseSecurityAttemptBypass: e.target.checked } })
                                }}
                            />
                        }
                        label="Enable attempt at bypassing possible bot detection via mouse"
                    />
                    <FormHelperText>
                        Enable attempt at bypassing possible bot detection via mouse. What this does is moves the mouse off of the game window after every run and waits several seconds there before
                        resuming bot operations.
                    </FormHelperText>
                </FormGroup>
            </div>
        )
    }

    const renderNightmareSettings = () => {
        if (
            bsc.settings.nightmare.enableNightmare &&
            (bsc.settings.game.farmingMode === "Special" ||
                bsc.settings.game.farmingMode === "Event" ||
                bsc.settings.game.farmingMode === "Event (Token Drawboxes)" ||
                bsc.settings.game.farmingMode === "Xeno Clash" ||
                bsc.settings.game.farmingMode === "Rise of the Beasts")
        ) {
            var title: string = ""
            if (bsc.settings.game.farmingMode === "Special") {
                title = "Dimensional Halo"
            } else if (bsc.settings.game.farmingMode === "Rise of the Beasts") {
                title = "Extreme+"
            } else {
                title = "Nightmare"
            }

            return (
                <div id="nightmare">
                    <Typography variant="h6" gutterBottom component="div" className="sectionTitle">
                        {title} Settings <Iconify icon="ri:sword-fill" className="sectionTitleIcon" />
                    </Typography>

                    <Divider />

                    <Typography variant="subtitle1" gutterBottom component="div" color="text.secondary">
                        If none of these settings are changed, then the bot will reuse the settings for the Farming Mode.
                    </Typography>

                    <FormGroup sx={{ paddingBottom: "16px" }}>
                        <FormControlLabel
                            control={
                                <Checkbox
                                    checked={bsc.settings.nightmare.enableCustomNightmareSettings}
                                    onChange={(e) => bsc.setSettings({ ...bsc.settings, nightmare: { ...bsc.settings.nightmare, enableCustomNightmareSettings: e.target.checked } })}
                                />
                            }
                            label={`Enable Custom Settings for ${title}`}
                        />
                        <FormHelperText>Enable customizing individual settings for {title}</FormHelperText>
                    </FormGroup>

                    {bsc.settings.nightmare.enableCustomNightmareSettings ? (
                        <Stack spacing={2}>
                            <Grid container>
                                <Grid item xs={6}>
                                    {!bsc.settings.misc.alternativeCombatScriptSelector ? (
                                        <div>
                                            <Input ref={inputRef} accept=".txt" id="combat-script-loader" type="file" onChange={(e) => loadNightmareCombatScript(e)} />
                                            <TextField
                                                variant="filled"
                                                label="Nightmare Combat Script"
                                                value={bsc.settings.nightmare.nightmareCombatScriptName !== "" ? bsc.settings.nightmare.nightmareCombatScriptName : "None Selected"}
                                                inputProps={{ readOnly: true }}
                                                InputLabelProps={{ shrink: true }}
                                                helperText="Select a Combat Script"
                                                onClick={() => inputRef.current?.click()}
                                                fullWidth
                                            />
                                        </div>
                                    ) : (
                                        <TextField
                                            variant="filled"
                                            label="Nightmare Combat Script"
                                            value={bsc.settings.nightmare.nightmareCombatScriptName !== "" ? bsc.settings.nightmare.nightmareCombatScriptName : "None Selected"}
                                            inputProps={{ readOnly: true }}
                                            InputLabelProps={{ shrink: true }}
                                            helperText="Select a Combat Script (alternative method)"
                                            onClick={() => loadNightmareCombatScriptAlternative()}
                                            fullWidth
                                        />
                                    )}
                                </Grid>
                                <Grid item xs />
                            </Grid>

                            <Grid container>
                                <Grid item xs={6}>
                                    <Button variant="contained" onClick={handleModalOpen} fullWidth>
                                        Select Nightmare Support Summons
                                    </Button>
                                    <Modal className="supportSummonModal" open={isModalOpen} onClose={handleModalClose}>
                                        <div>
                                            <Typography>Select Nightmare Support Summon(s)</Typography>
                                            <Box id="nightmareModalContainer" className="supportSummonContainer">
                                                <TransferList isNightmare={true} />
                                            </Box>
                                        </div>
                                    </Modal>
                                </Grid>
                                <Grid item xs />
                            </Grid>

                            <Grid container direction="row">
                                <Grid item id="gridItemNightmareGroup" xs={4}>
                                    <TextField
                                        label="Group #"
                                        variant="filled"
                                        type="number"
                                        error={bsc.settings.nightmare.nightmareGroupNumber < 1 || bsc.settings.nightmare.nightmareGroupNumber > 7}
                                        value={bsc.settings.nightmare.nightmareGroupNumber}
                                        inputProps={{ min: 1, max: 7 }}
                                        onChange={(e) => bsc.setSettings({ ...bsc.settings, nightmare: { ...bsc.settings.nightmare, nightmareGroupNumber: parseInt(e.target.value) } })}
                                        helperText="From 1 to 7"
                                        className="textfield"
                                    />
                                </Grid>

                                <Grid item xs={8} />

                                <Grid item id="gridItemNightmareParty" xs={4}>
                                    <TextField
                                        label="Party #"
                                        variant="filled"
                                        type="number"
                                        error={bsc.settings.nightmare.nightmarePartyNumber < 1 || bsc.settings.nightmare.nightmarePartyNumber > 6}
                                        value={bsc.settings.nightmare.nightmarePartyNumber}
                                        inputProps={{ min: 1, max: 6 }}
                                        onChange={(e) => bsc.setSettings({ ...bsc.settings, nightmare: { ...bsc.settings.nightmare, nightmarePartyNumber: parseInt(e.target.value) } })}
                                        helperText="From 1 to 6"
                                        className="textfield"
                                    />
                                </Grid>
                            </Grid>
                        </Stack>
                    ) : null}
                </div>
            )
        }
    }

    const renderMiscSettings = () => {
        return (
            <div id="misc">
                <Typography variant="h6" gutterBottom component="div" className="sectionTitle">
                    Misc Settings <Iconify icon="dashicons:admin-settings" className="sectionTitleIcon" />
                </Typography>

                <Divider />

                <FormGroup sx={{ paddingBottom: "16px" }}>
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={bsc.settings.misc.guiLowPerformanceMode}
                                onChange={(e) => {
                                    bsc.setSettings({ ...bsc.settings, misc: { ...bsc.settings.misc, guiLowPerformanceMode: e.target.checked } })
                                }}
                            />
                        }
                        label="Enable GUI Low Performance Mode"
                    />
                    <FormHelperText>Enable to disable background animations of the GUI.</FormHelperText>
                </FormGroup>

                <FormGroup sx={{ paddingBottom: "16px" }}>
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={bsc.settings.misc.alternativeCombatScriptSelector}
                                onChange={(e) => {
                                    bsc.setSettings({ ...bsc.settings, misc: { ...bsc.settings.misc, alternativeCombatScriptSelector: e.target.checked } })
                                }}
                            />
                        }
                        label="Enable Alternative File Picker for Combat Script selection"
                    />
                    <FormHelperText>Enable this if the regular method of combat script selection failed.</FormHelperText>
                </FormGroup>
            </div>
        )
    }

    // Arcarum sandbox settings
    const renderSandboxDefenderSettings = () => {
        if (bsc.settings.sandbox.enableDefender && bsc.settings.game.farmingMode === "Arcarum Sandbox") {
            var title: string = "Defender"

            return (
                <div id="defender">
                    <Typography variant="h6" gutterBottom component="div" className="sectionTitle">
                        {title} Settings <Iconify icon="ri:sword-fill" className="sectionTitleIcon" />
                    </Typography>

                    <Divider />

                    <Typography variant="subtitle1" gutterBottom component="div" color="text.secondary">
                        If none of these settings are changed, then the bot will reuse the settings for the Farming Mode.
                    </Typography>

                    <FormGroup sx={{ paddingBottom: "16px" }}>
                        <FormControlLabel
                            control={
                                <Checkbox
                                    checked={bsc.settings.sandbox.enableCustomDefenderSettings}
                                    onChange={(e) => bsc.setSettings({ ...bsc.settings, sandbox: { ...bsc.settings.sandbox, enableCustomDefenderSettings: e.target.checked } })}
                                />
                            }
                            label={`Enable Custom Settings for ${title}`}
                        />
                        <FormHelperText>Enable customizing individual settings for {title}</FormHelperText>
                    </FormGroup>

                    {bsc.settings.sandbox.enableCustomDefenderSettings ? (
                        <Stack spacing={2}>
                            <Grid container>
                                <Grid item xs={6}>
                                    {!bsc.settings.misc.alternativeCombatScriptSelector ? (
                                        <div>
                                            <Input ref={inputRef} accept=".txt" id="combat-script-loader" type="file" onChange={(e) => loadDefenderCombatScript(e)} />
                                            <TextField
                                                variant="filled"
                                                label="Defender Combat Script"
                                                value={bsc.settings.sandbox.defenderCombatScriptName !== "" ? bsc.settings.sandbox.defenderCombatScriptName : "None Selected"}
                                                inputProps={{ readOnly: true }}
                                                InputLabelProps={{ shrink: true }}
                                                helperText="Select a Combat Script"
                                                onClick={() => inputRef.current?.click()}
                                                fullWidth
                                            />
                                        </div>
                                    ) : (
                                        <TextField
                                            variant="filled"
                                            label="Defender Combat Script"
                                            value={bsc.settings.sandbox.defenderCombatScriptName !== "" ? bsc.settings.sandbox.defenderCombatScriptName : "None Selected"}
                                            inputProps={{ readOnly: true }}
                                            InputLabelProps={{ shrink: true }}
                                            helperText="Select a Combat Script (alternative method)"
                                            onClick={() => loadDefenderCombatScriptAlternative()}
                                            fullWidth
                                        />
                                    )}
                                </Grid>
                                <Grid item xs />
                            </Grid>

                            <Grid container>
                                <Grid item xs={6}>
                                    <TextField
                                        label="How many times to run"
                                        variant="filled"
                                        type="number"
                                        error={bsc.settings.sandbox.numberOfDefenders < 1}
                                        value={bsc.settings.sandbox.numberOfDefenders}
                                        inputProps={{ min: 1 }}
                                        onChange={(e) => bsc.setSettings({ ...bsc.settings, sandbox: { ...bsc.settings.sandbox, numberOfDefenders: parseInt(e.target.value) } })}
                                        className="textfield"
                                    />
                                </Grid>
                                <Grid item xs />
                            </Grid>

                            <Grid container direction="row">
                                <Grid item id="gridItemDefenderGroup" xs={4}>
                                    <TextField
                                        label="Group #"
                                        variant="filled"
                                        type="number"
                                        error={bsc.settings.sandbox.defenderGroupNumber < 1 || bsc.settings.sandbox.defenderGroupNumber > 7}
                                        value={bsc.settings.sandbox.defenderGroupNumber}
                                        inputProps={{ min: 1, max: 7 }}
                                        onChange={(e) => bsc.setSettings({ ...bsc.settings, sandbox: { ...bsc.settings.sandbox, defenderGroupNumber: parseInt(e.target.value) } })}
                                        helperText="From 1 to 7"
                                        className="textfield"
                                    />
                                </Grid>

                                <Grid item xs={8} />

                                <Grid item id="gridItemDefenderParty" xs={4}>
                                    <TextField
                                        label="Party #"
                                        variant="filled"
                                        type="number"
                                        error={bsc.settings.sandbox.defenderPartyNumber < 1 || bsc.settings.sandbox.defenderPartyNumber > 6}
                                        value={bsc.settings.sandbox.defenderPartyNumber}
                                        inputProps={{ min: 1, max: 6 }}
                                        onChange={(e) => bsc.setSettings({ ...bsc.settings, sandbox: { ...bsc.settings.sandbox, defenderPartyNumber: parseInt(e.target.value) } })}
                                        helperText="From 1 to 6"
                                        className="textfield"
                                    />
                                </Grid>
                            </Grid>
                        </Stack>
                    ) : null}
                </div>
            )
        }
    }

    // API Integration settings
    const renderAPIIntegrationSettings = () => {
        const title: string = "API Integration"
        return (
            <div id="api-integration">
                <Typography variant="h6" gutterBottom component="div" className="sectionTitle">
                    {title} Settings <Iconify icon="ri:sword-fill" className="sectionTitleIcon" />
                </Typography>

                <Divider />

                <Typography variant="subtitle1" gutterBottom component="div" color="text.secondary">
                    You can opt-in to this feature where the bot will automatically send successful results from the Loot Collection process and you can view your results and similar ones over on the
                    Granblue Automation Statistics website.
                </Typography>

                <FormGroup sx={{ paddingBottom: "16px" }}>
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={bsc.settings.api.enableOptInAPI}
                                onChange={(e) => bsc.setSettings({ ...bsc.settings, api: { ...bsc.settings.api, enableOptInAPI: e.target.checked } })}
                            />
                        }
                        label={`Enable Opt-in for ${title}`}
                    />
                    <FormHelperText>Enable API Integration with Granblue Automation Statistics</FormHelperText>
                </FormGroup>

                {bsc.settings.api.enableOptInAPI ? (
                    <div>
                        <Typography variant="subtitle1" gutterBottom component="p" color="text.secondary">
                            {`How this works:\n\nInput your username and password below that you used to register a new account on the website. The account registered on the website will be used to associate your success results from the Loot Collection process. A success result describes the Loot Collection process detecting a item drop after each run.`}
                        </Typography>

                        <Grid container spacing={2} direction="row" justifyContent="center" alignItems="center">
                            <Grid item xs={6}>
                                <TextField
                                    label="Username"
                                    value={bsc.settings.api.username}
                                    onChange={(e) => bsc.setSettings({ ...bsc.settings, api: { ...bsc.settings.api, username: e.target.value } })}
                                    placeholder="Insert your username here"
                                    multiline
                                    variant="filled"
                                    fullWidth
                                />
                            </Grid>

                            <Grid item xs={6}>
                                <TextField
                                    label="Password"
                                    value={bsc.settings.api.password}
                                    onChange={(e) => bsc.setSettings({ ...bsc.settings, api: { ...bsc.settings.api, password: e.target.value } })}
                                    placeholder="Insert your password here"
                                    multiline
                                    variant="filled"
                                    fullWidth
                                />
                            </Grid>

                            <Grid item>
                                <Box sx={{ m: 1, position: "relative" }}>
                                    <Button variant="contained" startIcon={<Speed />} className="twitterButton" onClick={(e) => testAPIIntegration(e)} disabled={testInProgress}>
                                        Test Login into API
                                    </Button>
                                    {testInProgress && (
                                        <CircularProgress
                                            size={24}
                                            sx={{
                                                position: "absolute",
                                                top: "50%",
                                                left: "50%",
                                                marginTop: "-12px",
                                                marginLeft: "-12px",
                                            }}
                                        />
                                    )}
                                </Box>
                            </Grid>
                        </Grid>
                    </div>
                ) : null}
            </div>
        )
    }

    // Attempt to kill the bot process if it is still active.
    const handleStop = async () => {
        if (testPID !== 0) {
            console.log("Killing process tree now...")
            const output = await new Command("powershell", `taskkill /F /T /PID ${testPID}`).execute() // Windows specific
            console.log(`Result of killing bot process using PID ${testPID}: \n${output.stdout}`)
            setTestPID(0)
        }
    }

    // Test Twitter API key.
    const testTwitter = async () => {
        // Construct the shell command using Tauri Command API.
        const command = new Command("python", ["backend/test.py", "9"])

        // Attach event listeners.
        command.on("close", (data) => {
            console.log(`\nChild process finished with code ${data.code}`)
            handleStop()

            setTestInProgress(false)
        })
        command.on("error", (error) => {
            console.log(`\nChild process finished with error ${error}`)
            handleStop()

            setTestFailed(true)
            setShowSnackbar(true)
        })
        command.stdout.on("data", (line: string) => {
            if (line.indexOf("Test successfully completed.") !== -1) {
                console.log("Testing Twitter API was successful.")
                setTestFailed(false)
                setShowSnackbar(true)
            } else if (line.indexOf("Test failed.") !== -1) {
                console.log("Testing Twitter API was unsuccessful.")
                setTestFailed(true)
                setTestErrorMessage(line)
                setShowSnackbar(true)
            }
        })
        command.stderr.on("data", (line) => {
            console.log("ERROR: ", line)
        })

        // Create the child process.
        const child = await command.spawn()
        console.log("PID: ", child.pid)
        setTestPID(child.pid)
        setTestInProgress(true)
    }

    // Test Discord API key.
    const testDiscord = async () => {
        // Construct the shell command using Tauri Command API.
        const command = new Command("python", ["backend/test.py", "10"])

        // Attach event listeners.
        command.on("close", (data) => {
            console.log(`\nChild process finished with code ${data.code}`)
            handleStop()

            setTestInProgress(false)
        })
        command.on("error", (error) => {
            console.log(`\nChild process finished with error ${error}`)
            handleStop()

            setTestFailed(true)
            setShowSnackbar(true)
        })
        command.stdout.on("data", (line: string) => {
            if (line.indexOf("Test successfully completed.") !== -1) {
                console.log("Testing Discord API was successful.")
                setTestFailed(false)
                setShowSnackbar(true)
            } else if (line.indexOf("Test failed.") !== -1) {
                console.log("Testing Discord API was unsuccessful.")
                setTestFailed(true)
                setTestErrorMessage(line)
                setShowSnackbar(true)
            }
        })
        command.stderr.on("data", (line) => {
            console.log("ERROR: ", line)
        })

        // Create the child process.
        const child = await command.spawn()
        console.log("PID: ", child.pid)
        setTestPID(child.pid)
        setTestInProgress(true)
    }

    const testAPIIntegration = (e: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
        e.preventDefault()
        setTestInProgress(true)
        axios
            .post(`${bsc.entryPoint}/api/login`, { username: bsc.settings.api.username, password: bsc.settings.api.password }, { withCredentials: true })
            .then(() => {
                setTestFailed(false)
            })
            .catch((e: AxiosError) => {
                setTestFailed(true)
                setTestErrorMessage(e.message)
            })
            .finally(() => {
                setTestInProgress(false)
                setShowSnackbar(true)
            })
    }

    // Show or hide the Support Summon Selection component.
    const handleModalOpen = () => setIsModalOpen(true)
    const handleModalClose = () => setIsModalOpen(false)

    return (
        <Fade in={true}>
            <Box className={bsc.settings.misc.guiLowPerformanceMode ? "extraSettingsContainerLowPerformance" : "extraSettingsContainer"}>
                <Snackbar
                    open={showSnackbar}
                    anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
                    autoHideDuration={10000}
                    onClose={() => setShowSnackbar(false)}
                    onClick={() => setShowSnackbar(false)}
                >
                    {testFailed ? <Alert severity="error">{testErrorMessage}</Alert> : <Alert severity="success">Test was successful.</Alert>}
                </Snackbar>

                <Stack spacing={2} className="extraSettingsWrapper">
                    {renderNightmareSettings()}

                    {renderSandboxDefenderSettings()}

                    {renderAPIIntegrationSettings()}

                    {renderTwitterSettings()}

                    {renderDiscordSettings()}

                    {renderConfigurationSettings()}

                    {renderMiscSettings()}
                </Stack>
            </Box>
        </Fade>
    )
}

export default ExtraSettings
