import { FormGroup, FormControlLabel, Checkbox, FormHelperText, TextField } from "@mui/material"
import { useContext } from "react"
import { BotStateContext } from "../../../context/BotStateContext"

const XenoClashHelper = () => {
    const bsc = useContext(BotStateContext)

    if (bsc.settings.game.farmingMode === "Xeno Clash") {
        return (
            <div id="Xeno Clash">
                <FormGroup sx={{ paddingBottom: "16px" }}>
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={bsc.settings.xenoClash.selectTopOption}
                                onChange={(e) => bsc.setSettings({ ...bsc.settings, xenoClash: { ...bsc.settings.xenoClash, selectTopOption: e.target.checked } })}
                            />
                        }
                        label="Enable Selection of Bottom Option"
                    />
                    <FormHelperText>Enabling this will select the bottom Xeno Clash option. By default, it selects the top option.</FormHelperText>
                </FormGroup>

                <FormGroup sx={{ paddingBottom: "16px" }}>
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={bsc.settings.xenoClash.enableNewPosition}
                                onChange={(e) => bsc.setSettings({ ...bsc.settings, xenoClash: { ...bsc.settings.xenoClash, enableNewPosition: e.target.checked } })}
                            />
                        }
                        label="Enable if Xeno Clash is in different position"
                    />
                    <FormHelperText>Enable this to properly select Xeno Clash if it is not positioned first on the list of events in the Home Menu.</FormHelperText>
                </FormGroup>

                {bsc.settings.xenoClash.enableNewPosition ? (
                    <TextField
                        label="New Position"
                        variant="filled"
                        type="number"
                        value={bsc.settings.xenoClash.newPosition}
                        inputProps={{ min: 0, max: 5 }}
                        onChange={(e) => bsc.setSettings({ ...bsc.settings, xenoClash: { ...bsc.settings.xenoClash, newPosition: parseInt(e.target.value) } })}
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

export default XenoClashHelper
