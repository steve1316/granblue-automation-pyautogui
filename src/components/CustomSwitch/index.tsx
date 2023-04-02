import { Switch, Group, useMantineTheme } from "@mantine/core"
import { Icon } from "@iconify/react"

interface CustomSwitchProps {
    label: string
    description?: string
    checked: boolean
    onChange: (checked: boolean) => void
}

const CustomSwitch = ({ label, description = "", checked, onChange }: CustomSwitchProps) => {
    const theme = useMantineTheme()

    return (
        <Switch
            checked={checked}
            onChange={(event) => onChange(event.currentTarget.checked)}
            color="teal"
            size="md"
            label={label}
            description={description}
            thumbIcon={
                checked ? (
                    <Icon icon="material-symbols:check" width="0.8rem" height="0.8rem" color={theme.colors.teal[theme.fn.primaryShade()]} stroke={"3"} />
                ) : (
                    <Icon icon="ph:x-bold" width="0.8rem" height="0.8rem" color={theme.colors.red[theme.fn.primaryShade()]} stroke={"3"} />
                )
            }
            styles={{
                track: {
                    // This forces the track to stay the same width regardless of the length of the description to maintain visual consistency.
                    width: "1rem",
                },
            }}
        />
    )
}

export default CustomSwitch
