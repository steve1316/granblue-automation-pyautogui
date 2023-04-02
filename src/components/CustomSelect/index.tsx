import { forwardRef } from "react"
import { Group, Avatar, Text, Select } from "@mantine/core"

export interface DataProps {
    label: string
    value: string
    image?: string
    description?: string
}

interface SelectItemProps extends React.ComponentPropsWithoutRef<"div"> {
    label: string
    image?: string
    description?: string
}

interface CustomSelectProps {
    label: string
    placeholder?: string
    description?: string
    disabled?: boolean
    data: DataProps[]
    value: string
    onChange: (value: string) => void
}

const SelectItem = forwardRef<HTMLDivElement, SelectItemProps>(({ label, image = "", description = "", ...others }: SelectItemProps, ref) => (
    <div ref={ref} {...others}>
        <Group noWrap>
            {image !== "" && <Avatar src={image} />}
            <div>
                <Text size="sm">{label}</Text>
                {description !== "" && (
                    <Text size="xs" opacity={0.65}>
                        {description}
                    </Text>
                )}
            </div>
        </Group>
    </div>
))

export const CustomSelect = ({ label, placeholder = "", description = "", disabled = false, data, value, onChange }: CustomSelectProps) => {
    return (
        <Select
            label={label}
            placeholder={placeholder}
            description={description}
            itemComponent={SelectItem}
            data={data}
            searchable
            clearable
            disabled={disabled}
            maxDropdownHeight={400}
            nothingFound="No matches found"
            filter={(value, item) => {
                return item.label?.toLowerCase().includes(value.toLowerCase().trim()) || item.description?.toLowerCase().includes(value.toLowerCase().trim())
            }}
            value={value}
            onChange={onChange}
        />
    )
}
