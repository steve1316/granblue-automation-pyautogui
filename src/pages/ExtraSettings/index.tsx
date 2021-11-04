import { Speed } from "@mui/icons-material"
import { Button, Checkbox, Divider, Fade, FormControlLabel, FormGroup, FormHelperText, Grid, InputAdornment, Stack, TextField, Typography } from "@mui/material"
import { Box } from "@mui/system"
import { Icon as Iconify } from "@iconify/react"
import "./index.scss"

const ExtraSettings = () => {
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
                        <TextField label="API Key" placeholder="Insert API Key here" multiline variant="filled" fullWidth />
                    </Grid>

                    <Grid item xs={6}>
                        <TextField label="API Key Secret" placeholder="Insert API Key Secret here" multiline variant="filled" fullWidth />
                    </Grid>

                    <Grid item xs={6}>
                        <TextField label="Access Token" placeholder="Insert Access Token here" multiline variant="filled" fullWidth />
                    </Grid>

                    <Grid item xs={6}>
                        <TextField label="Access Token Secret" placeholder="Insert Access Token Secret here" multiline variant="filled" fullWidth />
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
                    <FormControlLabel control={<Checkbox />} label="Enable Discord Notifications" />
                    <FormHelperText>Enable notifications of loot drops and errors encountered by the bot via Discord DMs.</FormHelperText>
                </FormGroup>

                <Grid container spacing={2} direction="row" justifyContent="center" alignItems="center">
                    <Grid item xs={6}>
                        <TextField label="Discord Token" placeholder="Insert Discord Token here" multiline variant="filled" fullWidth />
                    </Grid>

                    <Grid item xs={6}>
                        <TextField label="User ID" placeholder="Insert User ID here" multiline variant="filled" fullWidth />
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
                    <FormControlLabel control={<Checkbox />} label="Enable Auto-Restore" />
                    <FormHelperText>
                        Enable this option if you have already set the "Auto-Restore Notification Settings" to "Hide" in the game settings. It will shave off about 10 seconds every run. If enabled,
                        the following two options below are ignored.
                    </FormHelperText>
                </FormGroup>

                <FormGroup>
                    <FormControlLabel control={<Checkbox />} label="Enable Full Elixirs" />
                    <FormHelperText>Enable usage of full elixirs when refilling AP.</FormHelperText>
                </FormGroup>

                <FormGroup>
                    <FormControlLabel control={<Checkbox />} label="Enable Soul Balms" />
                    <FormHelperText>Enable usage of soul balms when refilling EP.</FormHelperText>
                </FormGroup>
            </div>
        )
    }

    const renderConfigurationSettings = () => {
        return (
            <div id="configuration">
                <Typography variant="h6" gutterBottom component="div" className="sectionTitle">
                    Configuration Settings <Iconify icon="icon-park-outline:setting-config" className="sectionTitleIcon" />
                </Typography>

                <Divider />

                <FormGroup sx={{ paddingBottom: "16px" }}>
                    <FormControlLabel control={<Checkbox />} label="Enable Bezier Curve Mouse Movement" />
                    <FormHelperText>Enable this option to have slow but human-like mouse movement. Disable this for fast but bot-like mouse movement.</FormHelperText>
                </FormGroup>

                <Grid container spacing={2} direction="row" justifyContent="center" alignItems="center">
                    <Grid item xs={6}>
                        <TextField
                            label="Mouse Speed"
                            variant="outlined"
                            type="number"
                            defaultValue={0.2}
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
                    <FormControlLabel control={<Checkbox />} label="Enable Delay Between Runs" />
                    <FormHelperText>Enable delay in seconds between runs to serve as a resting period.</FormHelperText>
                </FormGroup>

                <Grid container spacing={2} direction="row" justifyContent="center" alignItems="center">
                    <Grid item xs={6}>
                        <TextField
                            label="Delay In Seconds"
                            variant="outlined"
                            type="number"
                            defaultValue={15}
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

                <FormGroup sx={{ paddingBottom: "16px" }}>
                    <FormControlLabel control={<Checkbox />} label="Enable Randomized Delay Between Runs" />
                    <FormHelperText>Enable randomized delay in seconds between runs to serve as a resting period.</FormHelperText>
                </FormGroup>

                <Grid container spacing={2} direction="row" justifyContent="center" alignItems="center">
                    <Grid item xs={6}>
                        <TextField
                            label="Delay In Seconds Lower Bound"
                            variant="outlined"
                            type="number"
                            defaultValue={15}
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
                            variant="outlined"
                            type="number"
                            defaultValue={60}
                            inputProps={{ min: 1 }}
                            InputProps={{
                                endAdornment: <InputAdornment position="end">seconds</InputAdornment>,
                            }}
                            helperText="Set the Upper Bound for the resting period."
                            fullWidth
                        />
                    </Grid>
                </Grid>
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
