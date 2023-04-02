import { Stack, Text } from "@mantine/core"
import CustomSwitch from "../../components/CustomSwitch"
import { useContext } from "react"
import { BotStateContext } from "../../context/BotStateContext"

const GenericHelper = () => {
    const bsc = useContext(BotStateContext)

    if (bsc.settings.game.farmingMode === "Generic") {
        return (
            <Stack>
                <Text>{`Selecting this will repeat the current mission on the screen until it finishes the required number of runs. Note that Generic does not provide any navigation.
                                
                                It is required that the bot starts on either the Combat screen with the "Attack" button visible, the Loot Collection screen with the "Play Again" button visible, or the Coop Room screen with the "Start" button visible and party already selected.`}</Text>

                <CustomSwitch
                    label="Enable Forcing Reload after Attack"
                    description="Enable this option to force Generic Farming Mode to reload after an attack. This does not take into account whether or not the current battle supports reloading after an
                    attack."
                    checked={bsc.settings.generic.enableForceReload}
                    onChange={(checked) => bsc.setSettings({ ...bsc.settings, generic: { ...bsc.settings.generic, enableForceReload: checked } })}
                />
            </Stack>
        )
    } else {
        return null
    }
}

export default GenericHelper
