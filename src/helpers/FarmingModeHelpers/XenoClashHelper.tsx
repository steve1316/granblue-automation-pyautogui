import { Stack } from "@mantine/core"
import CustomSwitch from "../../components/CustomSwitch"
import CustomNumberInput from "../../components/CustomNumberInput"
import { useContext } from "react"
import { BotStateContext } from "../../context/BotStateContext"

const XenoClashHelper = () => {
    const bsc = useContext(BotStateContext)

    if (bsc.settings.game.farmingMode === "Xeno Clash") {
        return (
            <Stack>
                <CustomSwitch
                    label="Enable Selection of Bottom Option"
                    description="Enabling this will select the bottom Xeno Clash option. By default, it selects the top option."
                    checked={bsc.settings.xenoClash.selectTopOption}
                    onChange={(checked) => bsc.setSettings({ ...bsc.settings, xenoClash: { ...bsc.settings.xenoClash, enableNewPosition: checked } })}
                />
                <CustomSwitch
                    label="Enable if Xeno Clash is in different position"
                    description="Enable this to properly select Xeno Clash if it is not positioned first on the list of events in the Home Menu."
                    checked={bsc.settings.xenoClash.selectTopOption}
                    onChange={(checked) => bsc.setSettings({ ...bsc.settings, xenoClash: { ...bsc.settings.xenoClash, enableNewPosition: checked } })}
                />

                {bsc.settings.xenoClash.enableNewPosition ? (
                    <CustomNumberInput
                        label="New Position"
                        value={bsc.settings.xenoClash.newPosition}
                        onChange={(value) => bsc.setSettings({ ...bsc.settings, xenoClash: { ...bsc.settings.xenoClash, newPosition: value } })}
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

export default XenoClashHelper
