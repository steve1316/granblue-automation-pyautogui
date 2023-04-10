import { Stack } from "@mantine/core"
import CustomSwitch from "../../components/CustomSwitch"
import { useContext } from "react"
import { BotStateContext } from "../../context/BotStateContext"

const ArcarumSandboxHelper = () => {
    const bsc = useContext(BotStateContext)

    if (bsc.settings.game.farmingMode === "Arcarum Sandbox") {
        return (
            <Stack>
                <CustomSwitch
                    label="Enable Defender settings"
                    description="Enable additional settings to show up in the Extra Settings page."
                    checked={bsc.settings.sandbox.enableDefender}
                    onChange={(checked) => bsc.setSettings({ ...bsc.settings, sandbox: { ...bsc.settings.sandbox, enableDefender: checked } })}
                />
                <CustomSwitch
                    label="Enable Gold Chest opening"
                    description="Experimental, it uses default party and the chosen script for combat."
                    checked={bsc.settings.sandbox.enableGoldChest}
                    onChange={(checked) => bsc.setSettings({ ...bsc.settings, sandbox: { ...bsc.settings.sandbox, enableGoldChest: checked } })}
                />
            </Stack>
        )
    } else {
        return null
    }
}

export default ArcarumSandboxHelper
