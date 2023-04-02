import { Stack } from "@mantine/core"
import CustomSwitch from "../../components/CustomSwitch"
import CustomNumberInput from "../../components/CustomNumberInput"
import { useContext } from "react"
import { BotStateContext } from "../../context/BotStateContext"

const EventHelper = () => {
    const bsc = useContext(BotStateContext)

    if (bsc.settings.game.farmingMode === "Event") {
        return (
            <CustomSwitch
                label="Enable Incrementation of Location by 1"
                description='Enable this if the event has its N/H missions at the very top so the bot can correctly select the correct quest. Or in otherwords, enable this if the Event tab in the Special page
                    has 3 "Select" buttons instead of 2.'
                checked={bsc.settings.event.enableLocationIncrementByOne}
                onChange={(checked) => bsc.setSettings({ ...bsc.settings, event: { ...bsc.settings.event, enableLocationIncrementByOne: checked } })}
            />
        )
    } else if (bsc.settings.game.farmingMode === "Event (Token Drawboxes)") {
        return (
            <Stack>
                <CustomSwitch
                    label="Enable if Event is in different position"
                    description="Enable this to properly select the Event if it is not positioned first on the list of events in the Home Menu."
                    checked={bsc.settings.event.enableNewPosition}
                    onChange={(checked) => bsc.setSettings({ ...bsc.settings, event: { ...bsc.settings.event, enableNewPosition: checked } })}
                />
                {bsc.settings.event.enableNewPosition ? (
                    <CustomNumberInput
                        label="New Position"
                        value={bsc.settings.event.newPosition}
                        onChange={(value) => bsc.setSettings({ ...bsc.settings, event: { ...bsc.settings.event, newPosition: value } })}
                        min={0}
                        max={5}
                        description="Default is the first position or the value of 0"
                    />
                ) : null}
                <CustomSwitch
                    label="Enable Selecting the Bottom Category"
                    description="In the event of the raids being split between 2 categories, the bot selects the top category by default. Enable this to select the bottom category instead."
                    checked={bsc.settings.event.selectBottomCategory}
                    onChange={(checked) => bsc.setSettings({ ...bsc.settings, event: { ...bsc.settings.event, selectBottomCategory: checked } })}
                />
            </Stack>
        )
    } else {
        return null
    }
}

export default EventHelper
