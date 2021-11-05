import { Icon as Iconify } from "@iconify/react"
import { Speed } from "@mui/icons-material"
import { Button, Checkbox, Divider, Fade, FormControlLabel, FormGroup, FormHelperText, Grid, InputAdornment, Stack, TextField, Typography } from "@mui/material"
import { Box } from "@mui/system"
import { useContext } from "react"
import { BotStateContext } from "../../context/BotStateContext"
import "./index.scss"

const ExtraSettings = () => {
    const bot = useContext(BotStateContext)

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
                        control={<Checkbox checked={bot.enableTwitterStreamAPI} onChange={(e) => bot.setEnableTwitterStreamAPI(e.target.checked)} />}
                        label="Enable usage of Twitter Stream API"
                    />
                    <FormHelperText>Enable usage of Twitter Stream API for Raid farming.</FormHelperText>
                </FormGroup>

                <Grid container spacing={2} direction="row" justifyContent="center" alignItems="center">
                    <Grid item xs={6}>
                        <TextField
                            label="API Key"
                            value={bot.twitterAPIKey}
                            onChange={(e) => bot.setTwitterAPIKey(e.target.value)}
                            placeholder="Insert API Key here"
                            multiline
                            variant="filled"
                            fullWidth
                        />
                    </Grid>

                    <Grid item xs={6}>
                        <TextField
                            label="API Key Secret"
                            value={bot.twitterAPIKeySecret}
                            onChange={(e) => bot.setTwitterAPIKeySecret(e.target.value)}
                            placeholder="Insert API Key Secret here"
                            multiline
                            variant="filled"
                            fullWidth
                        />
                    </Grid>

                    <Grid item xs={6}>
                        <TextField
                            label="Access Token"
                            value={bot.twitterAccessToken}
                            onChange={(e) => bot.setTwitterAccessToken(e.target.value)}
                            placeholder="Insert Access Token here"
                            multiline
                            variant="filled"
                            fullWidth
                        />
                    </Grid>

                    <Grid item xs={6}>
                        <TextField
                            label="Access Token Secret"
                            value={bot.twitterAccessTokenSecret}
                            onChange={(e) => bot.setTwitterAccessTokenSecret(e.target.value)}
                            placeholder="Insert Access Token Secret here"
                            multiline
                            variant="filled"
                            fullWidth
                        />
                    </Grid>

                    <Grid item>
                        <Button variant="contained" startIcon={<Speed />} className="twitterButton">
                            Test Twitter API
                        </Button>
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
                        control={<Checkbox checked={bot.enableDiscordNotifications} onChange={(e) => bot.setEnableDiscordNotifications(e.target.checked)} />}
                        label="Enable Discord Notifications"
                    />
                    <FormHelperText>Enable notifications of loot drops and errors encountered by the bot via Discord DMs.</FormHelperText>
                </FormGroup>

                <Grid container spacing={2} direction="row" justifyContent="center" alignItems="center">
                    <Grid item xs={6}>
                        <TextField
                            label="Discord Token"
                            value={bot.discordToken}
                            onChange={(e) => bot.setDiscordToken(e.target.value)}
                            placeholder="Insert Discord Token here"
                            multiline
                            variant="filled"
                            fullWidth
                        />
                    </Grid>

                    <Grid item xs={6}>
                        <TextField
                            label="User ID"
                            value={bot.discordUserID}
                            onChange={(e) => bot.setDiscordUserID(e.target.value)}
                            placeholder="Insert User ID here"
                            multiline
                            variant="filled"
                            fullWidth
                        />
                    </Grid>

                    <Grid item>
                        <Button variant="contained" startIcon={<Speed />} className="discordButton">
                            Test Discord API
                        </Button>
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
                    <FormControlLabel control={<Checkbox checked={bot.enableAutoRestore} onChange={(e) => bot.setEnableAutoRestore(e.target.checked)} />} label="Enable Auto-Restore" />
                    <FormHelperText>
                        Enable this option if you have already set the "Auto-Restore Notification Settings" to "Hide" in the game settings. It will shave off about 10 seconds every run. If enabled,
                        the following two options below are ignored.
                    </FormHelperText>
                </FormGroup>

                <FormGroup>
                    <FormControlLabel control={<Checkbox checked={bot.enableFullElixir} onChange={(e) => bot.setEnableFullElixir(e.target.checked)} />} label="Enable Full Elixirs" />
                    <FormHelperText>Enable usage of full elixirs when refilling AP.</FormHelperText>
                </FormGroup>

                <FormGroup>
                    <FormControlLabel control={<Checkbox checked={bot.enableSoulBalm} onChange={(e) => bot.setEnableSoulBalm(e.target.checked)} />} label="Enable Soul Balms" />
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
                        control={<Checkbox checked={bot.enableBezierCurveMouseMovement} onChange={(e) => bot.setEnableBezierCurveMouseMovement(e.target.checked)} />}
                        label="Enable Bezier Curve Mouse Movement"
                    />
                    <FormHelperText>Enable this option to have slow but human-like mouse movement. Disable this for fast but bot-like mouse movement.</FormHelperText>
                </FormGroup>

                <Grid container spacing={2} direction="row" justifyContent="center" alignItems="center">
                    <Grid item xs={6}>
                        <TextField
                            label="Mouse Speed"
                            value={bot.mouseSpeed}
                            onChange={(e) => bot.setMouseSpeed(Number(e.target.value))}
                            variant="outlined"
                            type="number"
                            inputProps={{ min: 0, step: 0.1 }}
                            InputProps={{
                                endAdornment: <InputAdornment position="end">seconds</InputAdornment>,
                            }}
                            helperText="Set how fast a mouse operation finishes."
                            fullWidth
                        />
                    </Grid>

                    <Grid item xs={6} />
                </Grid>

                <FormGroup sx={{ paddingBottom: "16px" }}>
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={bot.enableDelayBetweenRuns}
                                onChange={(e) => {
                                    if (e.target.checked && bot.enableRandomizedDelayBetweenRuns) {
                                        bot.setEnableRandomizedDelayBetweenRuns(false)
                                    }

                                    bot.setEnableDelayBetweenRuns(e.target.checked)
                                }}
                            />
                        }
                        label="Enable Delay Between Runs"
                    />
                    <FormHelperText>Enable delay in seconds between runs to serve as a resting period.</FormHelperText>
                </FormGroup>

                {bot.enableDelayBetweenRuns && !bot.enableRandomizedDelayBetweenRuns ? (
                    <Grid container spacing={2} direction="row" justifyContent="center" alignItems="center">
                        <Grid item xs={6}>
                            <TextField
                                label="Delay In Seconds"
                                value={bot.delayBetweenRuns}
                                onChange={(e) => bot.setDelayBetweenRuns(Number(e.target.value))}
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
                                checked={bot.enableRandomizedDelayBetweenRuns}
                                onChange={(e) => {
                                    if (e.target.checked && bot.enableDelayBetweenRuns) {
                                        bot.setEnableDelayBetweenRuns(false)
                                    }

                                    bot.setEnableRandomizedDelayBetweenRuns(e.target.checked)
                                }}
                            />
                        }
                        label="Enable Randomized Delay Between Runs"
                    />
                    <FormHelperText>Enable randomized delay in seconds between runs to serve as a resting period.</FormHelperText>
                </FormGroup>

                {!bot.enableDelayBetweenRuns && bot.enableRandomizedDelayBetweenRuns ? (
                    <Grid container spacing={2} direction="row" justifyContent="center" alignItems="center">
                        <Grid item xs={6}>
                            <TextField
                                label="Delay In Seconds Lower Bound"
                                value={bot.delayBetweenRunsLowerBound}
                                onChange={(e) => {
                                    // Perform validation so that the value does not violate the opposing bound.
                                    if (Number(e.target.value) > bot.delayBetweenRunsUpperBound) {
                                        bot.setDelayBetweenRunsLowerBound(bot.delayBetweenRunsUpperBound)
                                    } else {
                                        bot.setDelayBetweenRunsLowerBound(Number(e.target.value))
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
                                value={bot.delayBetweenRunsUpperBound}
                                onChange={(e) => {
                                    // Perform validation so that the value does not violate the opposing bound.
                                    if (Number(e.target.value) < bot.delayBetweenRunsLowerBound) {
                                        bot.setDelayBetweenRunsUpperBound(bot.delayBetweenRunsLowerBound)
                                    } else {
                                        bot.setDelayBetweenRunsUpperBound(Number(e.target.value))
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
            </div>
        )
    }

    const renderDimensionalHaloSettings = () => {}

    const renderEventSettings = () => {}

    const renderRiseOfTheBeastsSettings = () => {}

    const renderXenoClashSettings = () => {}

    const renderArcarumSettings = () => {}

    return (
        <Fade in={true}>
            <Box className="container">
                <Stack spacing={2} className="wrapper">
                    {renderTwitterSettings()}

                    {renderDiscordSettings()}

                    {renderRefillSettings()}

                    {renderConfigurationSettings()}
                </Stack>
            </Box>
        </Fade>
    )
}

export default ExtraSettings
