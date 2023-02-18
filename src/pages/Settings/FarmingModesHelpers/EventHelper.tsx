import { FormGroup, FormControlLabel, Checkbox, FormHelperText, TextField } from "@mui/material"
import { useContext } from "react"
import { BotStateContext } from "../../../context/BotStateContext"

const EventHelper = () => {
    const bsc = useContext(BotStateContext)

    if (bsc.settings.game.farmingMode === "Event") {
        return (
            <FormGroup sx={{ paddingBottom: "16px" }} id="Event">
                <FormControlLabel
                    control={
                        <Checkbox
                            checked={bsc.settings.event.enableLocationIncrementByOne}
                            onChange={(e) => bsc.setSettings({ ...bsc.settings, event: { ...bsc.settings.event, enableLocationIncrementByOne: e.target.checked } })}
                        />
                    }
                    label="Enable Incrementation of Location by 1"
                />
                <FormHelperText>
                    Enable this if the event has its N/H missions at the very top so the bot can correctly select the correct quest. Or in otherwords, enable this if the Event tab in the Special page
                    has 3 "Select" buttons instead of 2.
                </FormHelperText>
            </FormGroup>
        )
    } else if (bsc.settings.game.farmingMode === "Event (Token Drawboxes)") {
        return (
            <div id="Event (Token Drawboxes)">
                <FormGroup sx={{ paddingBottom: "16px" }}>
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={bsc.settings.event.enableNewPosition}
                                onChange={(e) => bsc.setSettings({ ...bsc.settings, event: { ...bsc.settings.event, enableNewPosition: e.target.checked } })}
                            />
                        }
                        label="Enable if Event is in different position"
                    />
                    <FormHelperText>Enable this to properly select the Event if it is not positioned first on the list of events in the Home Menu.</FormHelperText>
                </FormGroup>

                {bsc.settings.event.enableNewPosition ? (
                    <TextField
                        label="New Position"
                        variant="filled"
                        type="number"
                        value={bsc.settings.event.newPosition}
                        inputProps={{ min: 0, max: 5 }}
                        onChange={(e) => bsc.setSettings({ ...bsc.settings, event: { ...bsc.settings.event, newPosition: parseInt(e.target.value) } })}
                        helperText={`Default is the first position or the value of 0`}
                        className="settingsTextfield"
                    />
                ) : null}

                <FormGroup sx={{ paddingBottom: "16px" }}>
                    <FormControlLabel
                        control={
                            <Checkbox
                                checked={bsc.settings.event.selectBottomCategory}
                                onChange={(e) => bsc.setSettings({ ...bsc.settings, event: { ...bsc.settings.event, selectBottomCategory: e.target.checked } })}
                            />
                        }
                        label="Enable Selecting the Bottom Category"
                    />
                    <FormHelperText>
                        In the event of the raids being split between 2 categories, the bot selects the top category by default. Enable this to select the bottom category instead.
                    </FormHelperText>
                </FormGroup>
            </div>
        )
    } else {
        return null
    }
}

export default EventHelper
