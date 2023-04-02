import { NumberInput } from "@mantine/core"

interface CustomNumberInputProps {
    label: string
    value: number
    onChange: (value: number) => void
    description?: string
    placeholder?: string
    min?: number
    max?: number
    step?: number
    disabled?: boolean
}

const CustomNumberInput = ({ label, value, onChange, description = "", placeholder = "", min = 1, max = 100, step = 1, disabled = false }: CustomNumberInputProps) => {
    let tempStep = Number(step)
    if (tempStep !== Math.floor(tempStep)) {
        return <NumberInput label={label} value={value} onChange={onChange} description={description} placeholder={placeholder} min={min} max={max} step={step} precision={2} disabled={disabled} />
    } else {
        return <NumberInput label={label} value={value} onChange={onChange} description={description} placeholder={placeholder} min={min} max={max} step={step} disabled={disabled} />
    }
}

export default CustomNumberInput
