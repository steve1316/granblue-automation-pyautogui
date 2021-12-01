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

    const bot = useContext(BotStateContext)

    const inputRef = useRef<HTMLInputElement>(null)

    // Load the selected combat script text file.
    const loadNightmareCombatScript = (event: React.ChangeEvent<HTMLInputElement>) => {
        var files = event.currentTarget.files
        if (files !== null && files.length !== 0) {
            var selectedFile = files[0]
            if (selectedFile === null || selectedFile === undefined) {
                // Reset the nightmare combat script selected if none was selected from the file picker dialog.
                bot.setSettings({ ...bot.settings, nightmare: { ...bot.settings.nightmare, nightmareCombatScriptName: "", nightmareCombatScript: [] } })
            } else {
                // Create the FileReader object and setup the function that will run after the FileReader reads the text file.
                var reader = new FileReader()
                reader.onload = function (loadedEvent) {
                    if (loadedEvent.target?.result !== null && loadedEvent.target?.result !== undefined) {
                        console.log("Loaded Nightmare Combat Script: ", loadedEvent.target.result)
                        const newCombatScript: string[] = loadedEvent.target.result.toString().split("\r\n")
                        bot.setSettings({ ...bot.settings, nightmare: { ...bot.settings.nightmare, nightmareCombatScriptName: selectedFile.name, nightmareCombatScript: newCombatScript } })
                    } else {
                        console.log("Failed to read Nightmare combat script. Reseting to default empty combat script...")
                        bot.setSettings({ ...bot.settings, nightmare: { ...bot.settings.nightmare, nightmareCombatScriptName: "", nightmareCombatScript: [] } })
                    }
                }

                // Read the text contents of the file.
                reader.readAsText(selectedFile)
            }
        } else {
            console.log("No file selected. Reseting to default empty combat script...")
            bot.setSettings({ ...bot.settings, nightmare: { ...bot.settings.nightmare, nightmareCombatScriptName: "", nightmareCombatScript: [] } })
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
                            bot.setSettings({
                                ...bot.settings,
                                nightmare: { ...bot.settings.nightmare, nightmareCombatScriptName: filePath.replace(/^.*[\\/]/, ""), nightmareCombatScript: newCombatScript },
                            })
                        })
                        .catch((err) => {
                            console.log(`Failed to read Nightmare combat script via alternative method: ${err}\n\nReseting to default empty combat script...`)
                            bot.setSettings({ ...bot.settings, nightmare: { ...bot.settings.nightmare, nightmareCombatScriptName: "", nightmareCombatScript: [] } })
                        })
                } else {
                    console.log(`No file selected.\n\nReseting to default empty combat script...`)
                    bot.setSettings({ ...bot.settings, nightmare: { ...bot.settings.nightmare, nightmareCombatScriptName: "", nightmareCombatScript: [] } })
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

                <Grid container spacing={2} direction="row" justifyContent="center" alignItems="center">
                    <Grid item xs={6}>
                        <TextField
                            label="API Key"
                            value={bot.settings.twitter.twitterAPIKey}
                            onChange={(e) => bot.setSettings({ ...bot.settings, twitter: { ...bot.settings.twitter, twitterAPIKey: e.target.value } })}
                            placeholder="Insert API Key here"
                            multiline
                            variant="filled"
                            fullWidth
                        />
                    </Grid>

                    <Grid item xs={6}>
                        <TextField
                            label="API Key Secret"
                            value={bot.settings.twitter.twitterAPIKeySecret}
                            onChange={(e) => bot.setSettings({ ...bot.settings, twitter: { ...bot.settings.twitter, twitterAPIKeySecret: e.target.value } })}
                            placeholder="Insert API Key Secret here"
                            multiline
                            variant="filled"
                            fullWidth
                        />
                    </Grid>

                    <Grid item xs={6}>
                        <TextField
                            label="Access Token"
                            value={bot.settings.twitter.twitterAccessToken}
                            onChange={(e) => bot.setSettings({ ...bot.settings, twitter: { ...bot.settings.twitter, twitterAccessToken: e.target.value } })}
                            placeholder="Insert Access Token here"
                            multiline
                            variant="filled"
                            fullWidth
                        />
                    </Grid>

                    <Grid item xs={6}>
                        <TextField
                            label="Access Token Secret"
                            value={bot.settings.twitter.twitterAccessTokenSecret}
                            onChange={(e) => bot.setSettings({ ...bot.settings, twitter: { ...bot.settings.twitter, twitterAccessTokenSecret: e.target.value } })}
                            placeholder="Insert Access Token Secret here"
                            multiline
                            variant="filled"
                            fullWidth
                        />
                    </Grid>

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
                                checked={bot.settings.discord.enableDiscordNotifications}
                                onChange={(e) => bot.setSettings({ ...bot.settings, discord: { ...bot.settings.discord, enableDiscordNotifications: e.target.checked } })}
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
                            value={bot.settings.discord.discordToken}
                            onChange={(e) => bot.setSettings({ ...bot.settings, discord: { ...bot.settings.discord, discordToken: e.target.value } })}
                            placeholder="Insert Discord Token here"
                            multiline
                            variant="filled"
                            fullWidth
                        />
                    </Grid>

                    <Grid item xs={6}>
                        <TextField
                            label="User ID"
                            value={bot.settings.discord.discordUserID}
                            onChange={(e) => bot.setSettings({ ...bot.settings, discord: { ...bot.settings.discord, discordUserID: e.target.value } })}
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

    const renderRefillSettings = () => {
        return (
            <div id="refill">
                <Typography variant="h6" gutterBottom component="div" className="sectionTitle">
                    Refill Settings <Iconify icon="ion:flask" className="sectionTitleIcon" />
                </Typography>

                <Divider />

                <FormGroup>
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={bot.settings.configuration.enableAutoRestore}
                                onChange={(e) => bot.setSettings({ ...bot.settings, configuration: { ...bot.settings.configuration, enableAutoRestore: e.target.checked } })}
                            />
                        }
                        label="Enable Auto-Restore"
                    />
                    <FormHelperText>
                        Enable this option if you have already set the "Auto-Restore Notification Settings" to "Hide" in the game settings. It will shave off about 10 seconds every run. If enabled,
                        the following two options below are ignored.
                    </FormHelperText>
                </FormGroup>

                <FormGroup>
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={bot.settings.configuration.enableFullElixir}
                                onChange={(e) => bot.setSettings({ ...bot.settings, configuration: { ...bot.settings.configuration, enableFullElixir: e.target.checked } })}
                            />
                        }
                        label="Enable Full Elixirs"
                    />
                    <FormHelperText>Enable usage of full elixirs when refilling AP.</FormHelperText>
                </FormGroup>

                <FormGroup>
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={bot.settings.configuration.enableSoulBalm}
                                onChange={(e) => bot.setSettings({ ...bot.settings, configuration: { ...bot.settings.configuration, enableSoulBalm: e.target.checked } })}
                            />
                        }
                        label="Enable Soul Balms"
                    />
                    <FormHelperText>Enable usage of soul balms when refilling EP.</FormHelperText>
                </FormGroup>
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

                <FormGroup sx={{ paddingBottom: "16px" }}>
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={bot.settings.configuration.enableBezierCurveMouseMovement}
                                onChange={(e) => bot.setSettings({ ...bot.settings, configuration: { ...bot.settings.configuration, enableBezierCurveMouseMovement: e.target.checked } })}
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
                            value={bot.settings.configuration.mouseSpeed}
                            onChange={(e) => bot.setSettings({ ...bot.settings, configuration: { ...bot.settings.configuration, mouseSpeed: Number(e.target.value) } })}
                            variant="outlined"
                            type="number"
                            inputProps={{ min: 0, step: 0.1 }}
                            InputProps={{
                                endAdornment: <InputAdornment position="end">seconds</InputAdornment>,
                            }}
                            helperText="Set how fast a mouse operation finishes."
                            disabled={bot.settings.configuration.enableBezierCurveMouseMovement}
                            fullWidth
                        />
                    </Grid>

                    <Grid item xs={6} />
                </Grid>

                <FormGroup sx={{ paddingBottom: "16px" }}>
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={bot.settings.configuration.enableDelayBetweenRuns}
                                onChange={(e) => {
                                    if (e.target.checked && bot.settings.configuration.enableRandomizedDelayBetweenRuns) {
                                        bot.setSettings({ ...bot.settings, configuration: { ...bot.settings.configuration, enableRandomizedDelayBetweenRuns: e.target.checked } })
                                    }

                                    bot.setSettings({ ...bot.settings, configuration: { ...bot.settings.configuration, enableDelayBetweenRuns: false } })
                                }}
                            />
                        }
                        label="Enable Delay Between Runs"
                    />
                    <FormHelperText>Enable delay in seconds between runs to serve as a resting period.</FormHelperText>
                </FormGroup>

                {bot.settings.configuration.enableDelayBetweenRuns && !bot.settings.configuration.enableRandomizedDelayBetweenRuns ? (
                    <Grid container spacing={2} direction="row" justifyContent="center" alignItems="center">
                        <Grid item xs={6}>
                            <TextField
                                label="Delay In Seconds"
                                value={bot.settings.configuration.delayBetweenRuns}
                                onChange={(e) => bot.setSettings({ ...bot.settings, configuration: { ...bot.settings.configuration, delayBetweenRuns: Number(e.target.value) } })}
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
                ) : (
                    ""
                )}

                <FormGroup sx={{ paddingBottom: "16px" }}>
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={bot.settings.configuration.enableRandomizedDelayBetweenRuns}
                                onChange={(e) => {
                                    if (e.target.checked && bot.settings.configuration.enableDelayBetweenRuns) {
                                        bot.setSettings({ ...bot.settings, configuration: { ...bot.settings.configuration, enableDelayBetweenRuns: false } })
                                    }

                                    bot.setSettings({ ...bot.settings, configuration: { ...bot.settings.configuration, enableRandomizedDelayBetweenRuns: e.target.checked } })
                                }}
                            />
                        }
                        label="Enable Randomized Delay Between Runs"
                    />
                    <FormHelperText>Enable randomized delay in seconds between runs to serve as a resting period.</FormHelperText>
                </FormGroup>

                {!bot.settings.configuration.enableDelayBetweenRuns && bot.settings.configuration.enableRandomizedDelayBetweenRuns ? (
                    <Grid container spacing={2} direction="row" justifyContent="center" alignItems="center">
                        <Grid item xs={6}>
                            <TextField
                                label="Delay In Seconds Lower Bound"
                                value={bot.settings.configuration.delayBetweenRunsLowerBound}
                                onChange={(e) => {
                                    // Perform validation so that the value does not violate the opposing bound.
                                    if (Number(e.target.value) > bot.settings.configuration.delayBetweenRunsUpperBound) {
                                        bot.setSettings({
                                            ...bot.settings,
                                            configuration: { ...bot.settings.configuration, delayBetweenRunsLowerBound: bot.settings.configuration.delayBetweenRunsUpperBound },
                                        })
                                    } else {
                                        bot.setSettings({ ...bot.settings, configuration: { ...bot.settings.configuration, delayBetweenRunsLowerBound: Number(e.target.value) } })
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
                                value={bot.settings.configuration.delayBetweenRunsUpperBound}
                                onChange={(e) => {
                                    // Perform validation so that the value does not violate the opposing bound.
                                    if (Number(e.target.value) < bot.settings.configuration.delayBetweenRunsLowerBound) {
                                        bot.setSettings({
                                            ...bot.settings,
                                            configuration: { ...bot.settings.configuration, delayBetweenRunsUpperBound: bot.settings.configuration.delayBetweenRunsLowerBound },
                                        })
                                    } else {
                                        bot.setSettings({ ...bot.settings, configuration: { ...bot.settings.configuration, delayBetweenRunsUpperBound: Number(e.target.value) } })
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
                ) : (
                    ""
                )}

                <FormGroup sx={{ paddingBottom: "16px" }}>
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={bot.settings.raid.enableAutoExitRaid}
                                onChange={(e) => {
                                    bot.setSettings({ ...bot.settings, raid: { ...bot.settings.raid, enableAutoExitRaid: e.target.checked } })
                                }}
                            />
                        }
                        label="Enable Auto Exiting Raids"
                    />
                    <FormHelperText>Enables backing out of a Raid without retreating while under Semi/Full Auto after a certain period of time has passed.</FormHelperText>
                </FormGroup>

                {bot.settings.raid.enableAutoExitRaid ? (
                    <Grid container spacing={2} direction="row" justifyContent="center" alignItems="center">
                        <Grid item xs={6}>
                            <TextField
                                label="Max Time Allowed for Semi/Full Auto"
                                value={bot.settings.raid.timeAllowedUntilAutoExitRaid}
                                onChange={(e) => {
                                    bot.setSettings({ ...bot.settings, raid: { ...bot.settings.raid, timeAllowedUntilAutoExitRaid: Number(e.target.value) } })
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
                ) : (
                    ""
                )}

                <FormGroup sx={{ paddingBottom: "16px" }}>
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={bot.settings.raid.enableNoTimeout}
                                onChange={(e) => {
                                    bot.setSettings({ ...bot.settings, raid: { ...bot.settings.raid, enableNoTimeout: e.target.checked } })
                                }}
                            />
                        }
                        label="Enable No Timeout"
                    />
                    <FormHelperText>Enable no timeouts when attempting to farm Raids that appear infrequently.</FormHelperText>
                </FormGroup>
            </div>
        )
    }

    const renderNightmareSettings = () => {
        if (
            bot.settings.nightmare.enableNightmare &&
            (bot.settings.game.farmingMode === "Special" ||
                bot.settings.game.farmingMode === "Event" ||
                bot.settings.game.farmingMode === "Event (Token Drawboxes)" ||
                bot.settings.game.farmingMode === "Xeno Clash" ||
                bot.settings.game.farmingMode === "Rise of the Beasts")
        ) {
            var title: string = ""
            if (bot.settings.game.farmingMode === "Special") {
                title = "Dimensional Halo"
            } else if (bot.settings.game.farmingMode === "Rise of the Beasts") {
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
                                    checked={bot.settings.nightmare.enableCustomNightmareSettings}
                                    onChange={(e) => bot.setSettings({ ...bot.settings, nightmare: { ...bot.settings.nightmare, enableCustomNightmareSettings: e.target.checked } })}
                                />
                            }
                            label={`Enable Custom Settings for ${title}`}
                        />
                        <FormHelperText>Enable customizing individual settings for {title}</FormHelperText>
                    </FormGroup>

                    {bot.settings.nightmare.enableCustomNightmareSettings ? (
                        <Stack spacing={2}>
                            <Grid container>
                                <Grid item xs={6}>
                                    {!bot.settings.misc.alternativeCombatScriptSelector ? (
                                        <div>
                                            <Input ref={inputRef} accept=".txt" id="combat-script-loader" type="file" onChange={(e) => loadNightmareCombatScript(e)} />
                                            <TextField
                                                variant="filled"
                                                label="Nightmare Combat Script"
                                                value={bot.settings.nightmare.nightmareCombatScriptName !== "" ? bot.settings.nightmare.nightmareCombatScriptName : "None Selected"}
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
                                            value={bot.settings.nightmare.nightmareCombatScriptName !== "" ? bot.settings.nightmare.nightmareCombatScriptName : "None Selected"}
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
                                        error={bot.settings.nightmare.nightmareGroupNumber < 1 || bot.settings.nightmare.nightmareGroupNumber > 7}
                                        value={bot.settings.nightmare.nightmareGroupNumber}
                                        inputProps={{ min: 1, max: 7 }}
                                        onChange={(e) => bot.setSettings({ ...bot.settings, nightmare: { ...bot.settings.nightmare, nightmareGroupNumber: parseInt(e.target.value) } })}
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
                                        error={bot.settings.nightmare.nightmarePartyNumber < 1 || bot.settings.nightmare.nightmarePartyNumber > 6}
                                        value={bot.settings.nightmare.nightmarePartyNumber}
                                        inputProps={{ min: 1, max: 6 }}
                                        onChange={(e) => bot.setSettings({ ...bot.settings, nightmare: { ...bot.settings.nightmare, nightmarePartyNumber: parseInt(e.target.value) } })}
                                        helperText="From 1 to 6"
                                        className="textfield"
                                    />
                                </Grid>
                            </Grid>
                        </Stack>
                    ) : (
                        ""
                    )}
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
                                checked={bot.settings.misc.guiLowPerformanceMode}
                                onChange={(e) => {
                                    bot.setSettings({ ...bot.settings, misc: { ...bot.settings.misc, guiLowPerformanceMode: e.target.checked } })
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
                                checked={bot.settings.misc.alternativeCombatScriptSelector}
                                onChange={(e) => {
                                    bot.setSettings({ ...bot.settings, misc: { ...bot.settings.misc, alternativeCombatScriptSelector: e.target.checked } })
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

    // Show or hide the Support Summon Selection component.
    const handleModalOpen = () => setIsModalOpen(true)
    const handleModalClose = () => setIsModalOpen(false)

    return (
        <Fade in={true}>
            <Box className={bot.settings.misc.guiLowPerformanceMode ? "extraSettingsContainerLowPerformance" : "extraSettingsContainer"}>
                <Snackbar
                    open={showSnackbar}
                    anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
                    autoHideDuration={10000}
                    onClose={() => setShowSnackbar(false)}
                    onClick={() => setShowSnackbar(false)}
                >
                    {testFailed ? <Alert severity="error">Test was not successful.</Alert> : <Alert severity="success">Test was successful.</Alert>}
                </Snackbar>

                <Stack spacing={2} className="extraSettingsWrapper">
                    {renderNightmareSettings()}

                    {renderTwitterSettings()}

                    {renderDiscordSettings()}

                    {renderRefillSettings()}

                    {renderConfigurationSettings()}

                    {renderMiscSettings()}
                </Stack>
            </Box>
        </Fade>
    )
}

export default ExtraSettings
