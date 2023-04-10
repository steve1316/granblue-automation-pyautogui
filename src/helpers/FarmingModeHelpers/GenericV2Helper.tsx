import { Stack, Text } from "@mantine/core"
import { useContext } from "react"
import { BotStateContext } from "../../context/BotStateContext"

const GenericV2Helper = () => {
    const bsc = useContext(BotStateContext)

    if (bsc.settings.game.farmingMode === "GenericV2") {
        return (
            <Stack>
                <Text>This is pretty similar to Generic Farming Mode. It will redo the current mission on the screen.</Text>
                <Text>
                    The main differences are that it will use a secondary window if present to quickly claim rewards and it uses a different parsing method for Combat Scripts to allow for navigation
                    via URLs.
                </Text>
                <Text>Examples have been provided in the /scripts/ folder suffixed with "v2".</Text>
            </Stack>
        )
    } else {
        return null
    }
}

export default GenericV2Helper
