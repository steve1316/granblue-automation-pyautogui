import { BotStateContext } from "../../context/BotStateContext"
import { Box, Checkbox, Divider, Fade, FormControlLabel, FormGroup, FormHelperText, Grid, InputAdornment, Stack, TextField, Typography } from "@mui/material"
import { useContext } from "react"
import "./index.scss"

interface Props {
    value: number
    onChange: React.ChangeEventHandler<HTMLTextAreaElement | HTMLInputElement> | undefined
    label: string
    helperText: string
}

const DelayTextField = ({ value, onChange, label, helperText }: Props) => {
    return (
        <Grid container spacing={2} direction="row" justifyContent="center" alignItems="center">
            <Grid item xs={6}>
                <TextField
                    label={label}
                    value={value}
                    onChange={onChange}
                    variant="outlined"
                    type="number"
                    inputProps={{ min: 1, max: 999 }}
                    InputProps={{
                        endAdornment: <InputAdornment position="end">tries</InputAdornment>,
                    }}
                    helperText={helperText}
                    fullWidth
                    style={{ marginBottom: "16px" }}
                />
            </Grid>
            <Grid item xs={6} />
        </Grid>
    )
}

const renderStart = () => {
    return (
        <div>
            <Divider>
                <Typography variant="h6" component="div" className="sectionTitle">
                    Calibration
                </Typography>
            </Divider>

            <FormGroup sx={{ paddingBottom: "16px" }}>
                <FormControlLabel control={<Checkbox checked={false} onChange={() => {}} />} label="Enable Calibration Adjustments" />
                <FormHelperText>Enable adjustment of tries for Calibration.</FormHelperText>
            </FormGroup>

            {true ? (
                <DelayTextField
                    value={1}
                    onChange={() => {}}
                    label="Home Calibration"
                    helperText="Home calibration occurs when the bot is first started and attempts to find and save the location of the game window."
                />
            ) : null}
        </div>
    )
}

const renderGeneral = () => {
    return (
        <div>
            <Divider sx={{ marginBottom: "16px" }}>
                <Typography variant="h6" component="div" className="sectionTitle">
                    General Image Searching
                </Typography>
            </Divider>

            <FormGroup sx={{ paddingBottom: "16px" }}>
                <FormControlLabel control={<Checkbox checked={false} onChange={() => {}} />} label="Enable General Image Searching Adjustments" />
                <FormHelperText>Enable adjustment of tries for General.</FormHelperText>
            </FormGroup>

            {true ? (
                <div>
                    <DelayTextField
                        value={1}
                        onChange={() => {}}
                        label="General Image Template Matching for Buttons"
                        helperText="Set the default number of tries for button template matching. This will be overwritten by the specific settings down below if applicable."
                    />
                    <DelayTextField
                        value={1}
                        onChange={() => {}}
                        label="General Image Template Matching for Headers"
                        helperText="Set the default number of tries for header template matching. This will be overwritten by the specific settings down below if applicable."
                    />
                </div>
            ) : null}
        </div>
    )
}

const renderSupportSummonSelection = () => {
    return (
        <div>
            <Divider sx={{ marginBottom: "16px" }}>
                <Typography variant="h6" component="div" className="sectionTitle">
                    Support Summon Selection Screen
                </Typography>
            </Divider>

            <FormGroup sx={{ paddingBottom: "16px" }}>
                <FormControlLabel control={<Checkbox checked={false} onChange={() => {}} />} label="Enable Summon Selection Screen Adjustments" />
                <FormHelperText>Enable adjustment of tries for Support Summon Selection Screen.</FormHelperText>
            </FormGroup>

            {true ? (
                <DelayTextField
                    value={1}
                    onChange={() => {}}
                    label="Arrival at Support Summon Selection screen"
                    helperText="Set the default number of tries to check if the bot arrived at the Support Summon Selection screen."
                />
            ) : null}
        </div>
    )
}

const renderCombatMode = () => {
    return (
        <div>
            <Divider sx={{ marginBottom: "16px" }}>
                <Typography variant="h6" component="div" className="sectionTitle">
                    Combat Mode
                </Typography>
            </Divider>

            <FormGroup sx={{ paddingBottom: "16px" }}>
                <FormControlLabel control={<Checkbox checked={false} onChange={() => {}} />} label="Enable Combat Mode Adjustments" />
                <FormHelperText>Enable adjustment of tries for Combat Mode Adjustments.</FormHelperText>
            </FormGroup>

            {true ? (
                <div>
                    <DelayTextField
                        value={1}
                        onChange={() => {}}
                        label="Arrival at Combat Screen"
                        helperText="Set the default number of tries for checking when the bot arrives at the Combat Screen."
                    />
                    <DelayTextField value={1} onChange={() => {}} label="Skill Usage" helperText="Set the default number of tries for checking when a skill is used." />
                    <DelayTextField value={1} onChange={() => {}} label="Summon Usage" helperText="Set the default number of tries for checking when a Summon is used." />
                    <DelayTextField
                        value={1}
                        onChange={() => {}}
                        label="Waiting for Reload"
                        helperText="Set the default number of tries for checking when a reload is finished, whether or not the bot ends up back at the Combat screen or the Loot Collection screen."
                    />
                    <DelayTextField
                        value={1}
                        onChange={() => {}}
                        label="Waiting for Attack"
                        helperText="Set the default number of tries for checking when an attack is finished when the Attack button is pressed."
                    />
                </div>
            ) : null}
        </div>
    )
}

const renderLootCollection = () => {
    return (
        <div>
            <Divider sx={{ marginBottom: "16px" }}>
                <Typography variant="h6" component="div" className="sectionTitle">
                    Loot Collection Screen
                </Typography>
            </Divider>

            <FormGroup sx={{ paddingBottom: "16px" }}>
                <FormControlLabel control={<Checkbox checked={false} onChange={() => {}} />} label="Enable Loot Collection Screen Adjustments" />
                <FormHelperText>Enable adjustment of tries for Loot Collection Screen Adjustments.</FormHelperText>
            </FormGroup>

            {true ? (
                <DelayTextField
                    value={1}
                    onChange={() => {}}
                    label="Arrival at Loot Collection screen"
                    helperText="Set the default number of tries for checking when the bot arrives at the Loot Collection screen."
                />
            ) : null}
        </div>
    )
}

const renderCheckForPopups = () => {
    return (
        <div>
            <Divider sx={{ marginBottom: "16px" }}>
                <Typography variant="h6" component="div" className="sectionTitle">
                    Check for Popups
                </Typography>
            </Divider>

            <FormGroup sx={{ paddingBottom: "16px" }}>
                <FormControlLabel control={<Checkbox checked={false} onChange={() => {}} />} label="Enable Check for Popups Adjustments" />
                <FormHelperText>Enable adjustment of tries for Check for Popups Adjustments.</FormHelperText>
            </FormGroup>

            {true ? (
                <DelayTextField value={1} onChange={() => {}} label="Check for Popups" helperText="Set the default number of tries for checking for popups during various stages of bot navigation." />
            ) : null}
        </div>
    )
}

const Delays = () => {
    const bsc = useContext(BotStateContext)

    return (
        <Fade in={true}>
            <Box className="delaysContainer">
                <Stack className="delaysWrapper">
                    <div>
                        <Typography variant="h6" gutterBottom component="div" color="text.secondary" sx={{ marginBottom: "16px" }}>
                            Set the default number of tries for the following:
                        </Typography>
                    </div>

                    {renderStart()}

                    {renderGeneral()}

                    {renderSupportSummonSelection()}

                    {renderCombatMode()}

                    {renderLootCollection()}

                    {renderCheckForPopups()}
                </Stack>
            </Box>
        </Fade>
    )
}

export default Delays
