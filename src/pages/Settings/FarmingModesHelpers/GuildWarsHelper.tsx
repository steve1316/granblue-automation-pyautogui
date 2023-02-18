import { FormGroup, FormControlLabel, Checkbox, FormHelperText, TextField } from "@mui/material"
import { useContext } from "react"
import { BotStateContext } from "../../../context/BotStateContext"

const GuildWarsHelper = () => {
    const bsc = useContext(BotStateContext)

    if (bsc.settings.game.farmingMode === "Guild Wars") {
        return (
            <div id="Guild Wars">
                <FormGroup sx={{ paddingBottom: "16px" }}>
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={bsc.settings.guildWars.enableNewPosition}
                                onChange={(e) => bsc.setSettings({ ...bsc.settings, guildWars: { ...bsc.settings.guildWars, enableNewPosition: e.target.checked } })}
                            />
                        }
                        label="Enable if Guild Wars is in different position"
                    />
                    <FormHelperText>Enable this to properly select Guild Wars if it is not positioned first on the list of events in the Home Menu.</FormHelperText>
                </FormGroup>

                {bsc.settings.guildWars.enableNewPosition ? (
                    <TextField
                        label="New Position"
                        variant="filled"
                        type="number"
                        value={bsc.settings.guildWars.newPosition}
                        inputProps={{ min: 0, max: 5 }}
                        onChange={(e) => bsc.setSettings({ ...bsc.settings, guildWars: { ...bsc.settings.guildWars, newPosition: parseInt(e.target.value) } })}
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

export default GuildWarsHelper
