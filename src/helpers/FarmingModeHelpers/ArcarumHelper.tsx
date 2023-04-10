import CustomSwitch from "../../components/CustomSwitch"
import { useContext } from "react"
import { BotStateContext } from "../../context/BotStateContext"
import { Stack } from "@mantine/core"

const ArcarumHelper = () => {
    const bsc = useContext(BotStateContext)

    if (bsc.settings.game.farmingMode === "Arcarum") {
        return (
            <Stack>
                <CustomSwitch
                    label="Enable Stop on Arcarum Boss"
                    description="Enable this option to have the bot stop upon encountering a Arcarum Boss (3-3, 6-3, 9-9)."
                    checked={bsc.settings.arcarum.enableStopOnArcarumBoss}
                    onChange={(checked) => bsc.setSettings({ ...bsc.settings, arcarum: { ...bsc.settings.arcarum, enableStopOnArcarumBoss: checked } })}
                />
            </Stack>
        )
    } else {
        return null
    }
}

export default ArcarumHelper
