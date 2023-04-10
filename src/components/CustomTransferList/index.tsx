import { useContext, useEffect, useState } from "react"
import { BotStateContext } from "../../context/BotStateContext"
import summonData from "../../data/summons.json"
import { Checkbox, Group, Avatar, Text, TransferList, TransferListData, TransferListItemComponent, TransferListItemComponentProps } from "@mantine/core"

const CustomTransferList = ({ isNightmare = false }: { isNightmare?: boolean }) => {
    const bsc = useContext(BotStateContext)

    const [data, setData] = useState<TransferListData>([[], []])

    interface SummonObj {
        name: string
        element: string
    }

    // Populate the Support Summon List.
    useEffect(() => {
        // Construct the list of selected summons.
        let selectedSummons: SummonObj[] = []
        bsc.settings.game.summons.forEach((summon, index) => {
            selectedSummons.push({
                name: summon,
                element: bsc.settings.game.summonElements[index],
            })
        })

        // Create an array of names of the selected summons.
        let filteredSelected = selectedSummons.map((summon) => {
            return summon.name
        })

        // Construct the full list of summons.
        let listOfSummons: SummonObj[] = []
        Object.entries(summonData).forEach((elementObj) => {
            elementObj[1].summons.forEach((summon) => {
                let comparedSummon: SummonObj = { name: summon, element: elementObj[0] }
                listOfSummons.push(comparedSummon)
            })
        })

        // Filter out the ones already selected.
        let filteredListOfSummons = listOfSummons.filter((summon) => !filteredSelected.includes(summon.name))

        // Now construct both objects as TransferListData.
        let newData: TransferListData = [[], []]
        filteredListOfSummons.forEach((summon) => {
            const fileName = summon.name.replaceAll(" ", "_").toLowerCase()
            newData[0].push({
                label: summon.name,
                value: summon.name,
                image: new URL(`../../images/summons/${fileName}.jpg`, import.meta.url).href,
                group: summon.element,
            })
        })
        selectedSummons.forEach((summon) => {
            const fileName = summon.name.replaceAll(" ", "_").toLowerCase()
            newData[1].push({
                label: summon.name,
                value: summon.name,
                image: new URL(`../../images/summons/${fileName}.jpg`, import.meta.url).href,
                group: summon.element,
            })
        })

        setData(newData)

        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])

    const saveSelectedSummons = (e: TransferListData) => {
        let selectedSummons: string[] = []
        let selectedSummonElements: string[] = []
        e[1].forEach((summon) => {
            selectedSummons.push(summon.value)
            Object.entries(summonData).map((elementObj) => {
                if (elementObj[1].summons.includes(summon.value)) {
                    selectedSummonElements.push(elementObj[0])
                    return
                }
            })
        })

        // Save selected summons to settings.
        if (!isNightmare) {
            bsc.setSettings({ ...bsc.settings, game: { ...bsc.settings.game, summons: selectedSummons, summonElements: selectedSummonElements } })
        } else {
            bsc.setSettings({ ...bsc.settings, nightmare: { ...bsc.settings.nightmare, nightmareSummons: selectedSummons, nightmareSummonElements: selectedSummonElements } })
        }
    }

    const ItemComponent: TransferListItemComponent = ({ data, selected }: TransferListItemComponentProps) => (
        <Group noWrap>
            <Avatar src={data.image} radius="xl" size="lg" />
            <div style={{ flex: 1 }}>
                <Text size="sm" weight={500}>
                    {data.label}
                </Text>
                <Text size="xs" color="dimmed" weight={400}>
                    {data.description}
                </Text>
            </div>
            <Checkbox checked={selected} onChange={() => {}} tabIndex={-1} sx={{ pointerEvents: "none" }} />
        </Group>
    )

    return (
        <TransferList
            value={data}
            onChange={(e) => {
                setData(e)
                saveSelectedSummons(e)
            }}
            searchPlaceholder="Search summons..."
            nothingFound="No matches found"
            titles={["Available Support Summons", "Selected Support Summons"]}
            listHeight={300}
            breakpoint="sm"
            itemComponent={ItemComponent}
            filter={(query, item) => item.label?.toLowerCase().includes(query.toLowerCase().trim()) || item.description?.toLowerCase().includes(query.toLowerCase().trim())}
        />
    )
}

export default CustomTransferList
