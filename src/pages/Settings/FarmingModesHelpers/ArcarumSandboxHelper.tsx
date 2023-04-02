import { FormGroup, FormControlLabel, Checkbox, FormHelperText, Grid, TextField } from "@mui/material"
import { useContext } from "react"
import { BotStateContext } from "../../../context/BotStateContext"

const ArcarumSandboxHelper = () => {
    const bsc = useContext(BotStateContext)

    if (bsc.settings.game.farmingMode === "Arcarum Sandbox") {
        return (
            <div id="Arcarum Sandbox">
                <FormGroup sx={{ paddingBottom: "16px" }}>
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={bsc.settings.sandbox.enableDefender}
                                onChange={(e) => bsc.setSettings({ ...bsc.settings, sandbox: { ...bsc.settings.sandbox, enableDefender: e.target.checked } })}
                            />
                        }
                        label="Enable Defender settings"
                    />
                    <FormHelperText>Enable additional settings to show up in the Extra Settings page.</FormHelperText>
                </FormGroup>

                <FormGroup sx={{ paddingBottom: "16px" }}>
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={bsc.settings.sandbox.enableHerald}
                                onChange={(e) => bsc.setSettings({ ...bsc.settings, sandbox: { ...bsc.settings.sandbox, enableHerald: e.target.checked } })}
                            />
                        }
                        label="Enable Herald settings"
                    />
                    <FormHelperText>Experimental, it uses default party and the chosen script for combat.</FormHelperText>
                </FormGroup>

                {bsc.settings.sandbox.enableHerald ? (
                        <Grid container>
                        <Grid item xs={6}>
                            <TextField
                                label="How many times to run"
                                variant="filled"
                                type="number"
                                error={bsc.settings.sandbox.numberOfHeralds < 1}
                                value={bsc.settings.sandbox.numberOfHeralds}
                                inputProps={{ min: 1 }}
                                onChange={(e) => bsc.setSettings({ ...bsc.settings, sandbox: { ...bsc.settings.sandbox, numberOfHeralds: parseInt(e.target.value) } })}
                                className="textfield"
                            />
                        </Grid>
                        <Grid item xs />
                    </Grid>
                    ) : null}

                <FormGroup sx={{ paddingBottom: "16px" }}>
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={bsc.settings.sandbox.enableGoldChest}
                                onChange={(e) => bsc.setSettings({ ...bsc.settings, sandbox: { ...bsc.settings.sandbox, enableGoldChest: e.target.checked } })}
                            />
                        }
                        label="Enable gold chest opening"
                    />
                    <FormHelperText>Experimental, it uses default party and the chosen script for combat.</FormHelperText>
                </FormGroup>
            </div>
        )
    } else {
        return null
    }
}

export default ArcarumSandboxHelper
