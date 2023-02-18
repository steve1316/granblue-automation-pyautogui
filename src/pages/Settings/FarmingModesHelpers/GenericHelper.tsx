import { Divider, Typography, FormGroup, FormControlLabel, Checkbox, FormHelperText } from "@mui/material"
import { useContext } from "react"
import { BotStateContext } from "../../../context/BotStateContext"

const GenericHelper = () => {
    const bsc = useContext(BotStateContext)

    if (bsc.settings.game.farmingMode === "Generic") {
        return (
            <div id="Generic">
                <Divider />
                <Typography variant="subtitle2" component="p" color="text.secondary">
                    {`Selecting this will repeat the current mission on the screen until it finishes the required number of runs. Note that Generic does not provide any navigation.
                                
                                It is required that the bot starts on either the Combat screen with the "Attack" button visible, the Loot Collection screen with the "Play Again" button visible, or the Coop Room screen with the "Start" button visible and party already selected.`}
                </Typography>
                <Divider />

                <FormGroup sx={{ paddingBottom: "16px" }}>
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={bsc.settings.generic.enableForceReload}
                                onChange={(e) => bsc.setSettings({ ...bsc.settings, generic: { ...bsc.settings.generic, enableForceReload: e.target.checked } })}
                            />
                        }
                        label="Enable Forcing Reload after Attack"
                    />
                    <FormHelperText>
                        Enable this option to force Generic Farming Mode to reload after an attack. This does not take into account whether or not the current battle supports reloading after an
                        attack.
                    </FormHelperText>
                </FormGroup>
            </div>
        )
    } else {
        return null
    }
}

export default GenericHelper
