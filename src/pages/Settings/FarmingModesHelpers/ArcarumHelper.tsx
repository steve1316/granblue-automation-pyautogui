import { FormGroup, FormControlLabel, Checkbox, FormHelperText } from "@mui/material"
import { useContext } from "react"
import { BotStateContext } from "../../../context/BotStateContext"

const ArcarumHelper = () => {
    const bsc = useContext(BotStateContext)

    if (bsc.settings.game.farmingMode === "Arcarum") {
        return (
            <FormGroup sx={{ paddingBottom: "16px" }} id="Arcarum">
                <FormControlLabel
                    control={
                        <Checkbox
                            checked={bsc.settings.arcarum.enableStopOnArcarumBoss}
                            onChange={(e) => bsc.setSettings({ ...bsc.settings, arcarum: { ...bsc.settings.arcarum, enableStopOnArcarumBoss: e.target.checked } })}
                        />
                    }
                    label="Enable Stop on Arcarum Boss"
                />
                <FormHelperText>Enable this option to have the bot stop upon encountering a Arcarum Boss (3-3, 6-3, 9-9).</FormHelperText>
            </FormGroup>
        )
    } else {
        return null
    }
}

export default ArcarumHelper
