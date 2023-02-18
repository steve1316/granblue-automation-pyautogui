import { FormGroup, FormControlLabel, Checkbox, FormHelperText, TextField } from "@mui/material"
import { useContext } from "react"
import { BotStateContext } from "../../../context/BotStateContext"

const ProvingGroundsHelper = () => {
    const bsc = useContext(BotStateContext)

    if (bsc.settings.game.farmingMode === "Proving Grounds") {
        return (
            <div id="Proving Grounds">
                <FormGroup sx={{ paddingBottom: "16px" }}>
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={bsc.settings.provingGrounds.enableNewPosition}
                                onChange={(e) => bsc.setSettings({ ...bsc.settings, provingGrounds: { ...bsc.settings.provingGrounds, enableNewPosition: e.target.checked } })}
                            />
                        }
                        label="Enable if Proving Grounds is in different position"
                    />
                    <FormHelperText>Enable this to properly select Proving Grounds if it is not positioned first on the list of events in the Home Menu.</FormHelperText>
                </FormGroup>

                {bsc.settings.provingGrounds.enableNewPosition ? (
                    <TextField
                        label="New Position"
                        variant="filled"
                        type="number"
                        value={bsc.settings.provingGrounds.newPosition}
                        inputProps={{ min: 0, max: 5 }}
                        onChange={(e) => bsc.setSettings({ ...bsc.settings, provingGrounds: { ...bsc.settings.provingGrounds, newPosition: parseInt(e.target.value) } })}
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

export default ProvingGroundsHelper
