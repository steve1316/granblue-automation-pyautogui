import { BotStateContext } from "../../context/BotStateContext"
import { Box, Checkbox, Divider, Fade, FormControlLabel, FormGroup, FormHelperText, Grid, InputAdornment, Stack, TextField, Typography } from "@mui/material"
import { useContext } from "react"
import "./index.scss"

const Adjustments = () => {
    const bsc = useContext(BotStateContext)

    interface Props {
        value: number
        onChange: React.ChangeEventHandler<HTMLTextAreaElement | HTMLInputElement> | undefined
        label: string
        helperText: string
    }

    const CustomTextField = ({ value, onChange, label, helperText }: Props) => {
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
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={bsc.settings.adjustment.enableCalibrationAdjustment}
                                onChange={(e) => {
                                    bsc.setSettings({ ...bsc.settings, adjustment: { ...bsc.settings.adjustment, enableCalibrationAdjustment: e.target.checked } })
                                }}
                            />
                        }
                        label="Enable Calibration Adjustments"
                    />
                    <FormHelperText>Enable adjustment of tries for Calibration.</FormHelperText>
                </FormGroup>

                {bsc.settings.adjustment.enableCalibrationAdjustment ? (
                    <CustomTextField
                        value={bsc.settings.adjustment.adjustCalibration}
                        onChange={(e) => {
                            bsc.setSettings({ ...bsc.settings, adjustment: { ...bsc.settings.adjustment, adjustCalibration: Number(e.target.value) } })
                        }}
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
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={bsc.settings.adjustment.enableGeneralAdjustment}
                                onChange={(e) => {
                                    bsc.setSettings({ ...bsc.settings, adjustment: { ...bsc.settings.adjustment, enableGeneralAdjustment: e.target.checked } })
                                }}
                            />
                        }
                        label="Enable General Image Searching Adjustments"
                    />
                    <FormHelperText>Enable adjustment of tries for General.</FormHelperText>
                </FormGroup>

                {bsc.settings.adjustment.enableGeneralAdjustment ? (
                    <div>
                        <CustomTextField
                            value={bsc.settings.adjustment.adjustButtonSearchGeneral}
                            onChange={(e) => {
                                bsc.setSettings({ ...bsc.settings, adjustment: { ...bsc.settings.adjustment, adjustButtonSearchGeneral: Number(e.target.value) } })
                            }}
                            label="General Image Template Matching for Buttons"
                            helperText="Set the default number of tries for button template matching. This will be overwritten by the specific settings down below if applicable."
                        />
                        <CustomTextField
                            value={bsc.settings.adjustment.adjustHeaderSearchGeneral}
                            onChange={(e) => {
                                bsc.setSettings({ ...bsc.settings, adjustment: { ...bsc.settings.adjustment, adjustHeaderSearchGeneral: Number(e.target.value) } })
                            }}
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
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={bsc.settings.adjustment.enableSupportSummonSelectionScreenAdjustment}
                                onChange={(e) => {
                                    bsc.setSettings({ ...bsc.settings, adjustment: { ...bsc.settings.adjustment, enableSupportSummonSelectionScreenAdjustment: e.target.checked } })
                                }}
                            />
                        }
                        label="Enable Summon Selection Screen Adjustments"
                    />
                    <FormHelperText>Enable adjustment of tries for Support Summon Selection Screen.</FormHelperText>
                </FormGroup>

                {bsc.settings.adjustment.enableSupportSummonSelectionScreenAdjustment ? (
                    <CustomTextField
                        value={bsc.settings.adjustment.adjustSupportSummonSelectionScreen}
                        onChange={(e) => {
                            bsc.setSettings({ ...bsc.settings, adjustment: { ...bsc.settings.adjustment, adjustSupportSummonSelectionScreen: Number(e.target.value) } })
                        }}
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
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={bsc.settings.adjustment.enableCombatModeAdjustment}
                                onChange={(e) => {
                                    bsc.setSettings({ ...bsc.settings, adjustment: { ...bsc.settings.adjustment, enableCombatModeAdjustment: e.target.checked } })
                                }}
                            />
                        }
                        label="Enable Combat Mode Adjustments"
                    />
                    <FormHelperText>Enable adjustment of tries for Combat Mode Adjustments.</FormHelperText>
                </FormGroup>

                {bsc.settings.adjustment.enableCombatModeAdjustment ? (
                    <div>
                        <CustomTextField
                            value={bsc.settings.adjustment.adjustCombatStart}
                            onChange={(e) => {
                                bsc.setSettings({ ...bsc.settings, adjustment: { ...bsc.settings.adjustment, adjustCombatStart: Number(e.target.value) } })
                            }}
                            label="Arrival at Combat Screen"
                            helperText="Set the default number of tries for checking when the bot arrives at the Combat Screen."
                        />
                        <CustomTextField
                            value={bsc.settings.adjustment.adjustSkillUsage}
                            onChange={(e) => {
                                bsc.setSettings({ ...bsc.settings, adjustment: { ...bsc.settings.adjustment, adjustSkillUsage: Number(e.target.value) } })
                            }}
                            label="Skill Usage"
                            helperText="Set the default number of tries for checking when a skill is used."
                        />
                        <CustomTextField
                            value={bsc.settings.adjustment.adjustSummonUsage}
                            onChange={(e) => {
                                bsc.setSettings({ ...bsc.settings, adjustment: { ...bsc.settings.adjustment, adjustSummonUsage: Number(e.target.value) } })
                            }}
                            label="Summon Usage"
                            helperText="Set the default number of tries for checking when a Summon is used."
                        />
                        <CustomTextField
                            value={bsc.settings.adjustment.adjustWaitingForReload}
                            onChange={(e) => {
                                bsc.setSettings({ ...bsc.settings, adjustment: { ...bsc.settings.adjustment, adjustWaitingForReload: Number(e.target.value) } })
                            }}
                            label="Waiting for Reload"
                            helperText="Set the default number of tries for checking when a reload is finished, whether or not the bot ends up back at the Combat screen or the Loot Collection screen."
                        />
                        <CustomTextField
                            value={bsc.settings.adjustment.adjustWaitingForAttack}
                            onChange={(e) => {
                                bsc.setSettings({ ...bsc.settings, adjustment: { ...bsc.settings.adjustment, adjustWaitingForAttack: Number(e.target.value) } })
                            }}
                            label="Waiting for Attack"
                            helperText="Set the default number of tries for checking when an attack is finished when the Attack button is pressed."
                        />
                    </div>
                ) : null}
            </div>
        )
    }

    return (
        <Fade in={true}>
            <Box className="adjustmentsContainer">
                <Stack className="adjustmentsWrapper">
                    <div>
                        <Typography variant="h6" gutterBottom component="div" color="text.secondary" sx={{ marginBottom: "16px" }}>
                            Adjust the default number of tries for the following:
                        </Typography>
                    </div>

                    {renderStart()}

                    {renderGeneral()}

                    {renderSupportSummonSelection()}

                    {renderCombatMode()}
                </Stack>
            </Box>
        </Fade>
    )
}

export default Adjustments