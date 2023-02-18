import { FormGroup, FormControlLabel, Checkbox, FormHelperText, TextField } from "@mui/material"
import { useContext } from "react"
import { BotStateContext } from "../../../context/BotStateContext"

const ROTBHelper = () => {
    const bsc = useContext(BotStateContext)

    if (bsc.settings.game.farmingMode === "Rise of the Beasts") {
        return (
            <div id="Rise of the Beasts">
                <FormGroup sx={{ paddingBottom: "16px" }}>
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={bsc.settings.rotb.enableNewPosition}
                                onChange={(e) => bsc.setSettings({ ...bsc.settings, rotb: { ...bsc.settings.rotb, enableNewPosition: e.target.checked } })}
                            />
                        }
                        label="Enable if ROTB is in different position"
                    />
                    <FormHelperText>Enable this to properly select ROTB if it is not positioned first on the list of events in the Home Menu.</FormHelperText>
                </FormGroup>

                {bsc.settings.rotb.enableNewPosition ? (
                    <TextField
                        label="New Position"
                        variant="filled"
                        type="number"
                        value={bsc.settings.rotb.newPosition}
                        inputProps={{ min: 0, max: 5 }}
                        onChange={(e) => bsc.setSettings({ ...bsc.settings, rotb: { ...bsc.settings.rotb, newPosition: parseInt(e.target.value) } })}
                        helperText={`Default is the first position or the value of 0`}
                        className="settingsTextfield"
                    />
                ) : null}
            </div>
        )
    } else {
        return null
    }
}

export default ROTBHelper
