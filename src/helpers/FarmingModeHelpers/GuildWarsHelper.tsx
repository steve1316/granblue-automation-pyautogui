import { Stack } from "@mantine/core"
import CustomSwitch from "../../components/CustomSwitch"
import CustomNumberInput from "../../components/CustomNumberInput"
import { useContext } from "react"
import { BotStateContext } from "../../context/BotStateContext"

const GuildWarsHelper = () => {
    const bsc = useContext(BotStateContext)

    if (bsc.settings.game.farmingMode === "Guild Wars") {
        return (
            <Stack>
                <CustomSwitch
                    label="Enable if Guild Wars is in different position"
                    description="Enable this to properly select Guild Wars if it is not positioned first on the list of events in the Home Menu."
                    checked={bsc.settings.guildWars.enableNewPosition}
                    onChange={(checked) => bsc.setSettings({ ...bsc.settings, guildWars: { ...bsc.settings.guildWars, enableNewPosition: checked } })}
                />

                {bsc.settings.guildWars.enableNewPosition ? (
                    <CustomNumberInput
                        label="New Position"
                        value={bsc.settings.guildWars.newPosition}
                        onChange={(value) => bsc.setSettings({ ...bsc.settings, guildWars: { ...bsc.settings.guildWars, newPosition: value } })}
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

export default GuildWarsHelper
