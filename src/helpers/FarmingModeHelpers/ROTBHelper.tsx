import { Stack } from "@mantine/core"
import CustomSwitch from "../../components/CustomSwitch"
import CustomNumberInput from "../../components/CustomNumberInput"
import { useContext } from "react"
import { BotStateContext } from "../../context/BotStateContext"

const ROTBHelper = () => {
    const bsc = useContext(BotStateContext)

    if (bsc.settings.game.farmingMode === "Rise of the Beasts") {
        return (
            <Stack>
                <CustomSwitch
                    label="Enable if ROTB is in different position"
                    description="Enable this to properly select ROTB if it is not positioned first on the list of events in the Home Menu."
                    checked={bsc.settings.rotb.enableNewPosition}
                    onChange={(checked) => bsc.setSettings({ ...bsc.settings, rotb: { ...bsc.settings.rotb, enableNewPosition: checked } })}
                />
                {bsc.settings.rotb.enableNewPosition ? (
                    <CustomNumberInput
                        label="New Position"
                        value={bsc.settings.rotb.newPosition}
                        onChange={(value) => bsc.setSettings({ ...bsc.settings, rotb: { ...bsc.settings.rotb, newPosition: value } })}
                        min={0}
                        max={5}
                        description="Default is the first position or the value of 0"
                    />
                ) : null}
            </Stack>
        )
    } else {
        return null
    }
}

export default ROTBHelper
