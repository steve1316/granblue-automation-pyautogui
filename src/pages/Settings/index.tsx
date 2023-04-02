import { Container, createStyles, Grid, Button, Modal, Group, Divider, FileInput, Stack } from "@mantine/core"
import { useContext, useState, useEffect } from "react"
import { CustomSelect, DataProps } from "../../components/CustomSelect"
import CustomSwitch from "../../components/CustomSwitch"
import CustomNumberInput from "../../components/CustomNumberInput"
import { BotStateContext } from "../../context/BotStateContext"
import data from "../../data/data.json"
import CustomTransferList from "../../components/CustomTransferList"
import { Icon } from "@iconify/react"
import { loadCombatScript, loadCombatScriptAlternative } from "../../helpers/CombatScriptHelper"
import ArcarumHelper from "../../helpers/FarmingModeHelpers/ArcarumHelper"
import ArcarumSandboxHelper from "../../helpers/FarmingModeHelpers/ArcarumSandboxHelper"
import EventHelper from "../../helpers/FarmingModeHelpers/EventHelper"
import GenericHelper from "../../helpers/FarmingModeHelpers/GenericHelper"
import GuildWarsHelper from "../../helpers/FarmingModeHelpers/GuildWarsHelper"
import ProvingGroundsHelper from "../../helpers/FarmingModeHelpers/ProvingGroundsHelper"
import ROTBHelper from "../../helpers/FarmingModeHelpers/ROTBHelper"
import XenoClashHelper from "../../helpers/FarmingModeHelpers/XenoClashHelper"

const Settings = () => {
    const farmingModes: DataProps[] = [
        {
            label: "Quest",
            value: "Quest",
        },
        {
            label: "Special",
            value: "Special",
        },
        {
            label: "Coop",
            value: "Coop",
        },
        {
            label: "Raid",
            value: "Raid",
        },
        {
            label: "Event",
            value: "Event",
        },
        {
            label: "Event (Token Drawboxes)",
            value: "Event (Token Drawboxes)",
        },
        {
            label: "Rise of the Beasts",
            value: "Rise of the Beasts",
        },
        {
            label: "Guild Wars",
            value: "Guild Wars",
        },
        {
            label: "Dread Barrage",
            value: "Dread Barrage",
        },
        {
            label: "Proving Grounds",
            value: "Proving Grounds",
        },
        {
            label: "Xeno Clash",
            value: "Xeno Clash",
        },
        {
            label: "Arcarum",
            value: "Arcarum",
        },
        {
            label: "Arcarum Sandbox",
            value: "Arcarum Sandbox",
        },
        {
            label: "Generic",
            value: "Generic",
        },
    ]

    const useStyles = createStyles((theme) => ({
        container: {
            width: "100%",
            height: "100%",
            padding: "10px 20px 10px 20px",
        },
    }))

    const { classes } = useStyles()

    const bsc = useContext(BotStateContext)
    const [itemList, setItemList] = useState<DataProps[]>([])
    const [missionList, setMissionList] = useState<DataProps[]>([])
    const [isModalOpen, setIsModalOpen] = useState<boolean>(false)

    // Populate the item list after selecting the Farming Mode.
    useEffect(() => {
        var newItemList: DataProps[] = []
        var fullItemList: DataProps[] = []

        if (
            bsc.settings.game.farmingMode === "Quest" ||
            bsc.settings.game.farmingMode === "Special" ||
            bsc.settings.game.farmingMode === "Coop" ||
            bsc.settings.game.farmingMode === "Raid" ||
            bsc.settings.game.farmingMode === "Event" ||
            bsc.settings.game.farmingMode === "Event (Token Drawboxes)" ||
            bsc.settings.game.farmingMode === "Rise of the Beasts" ||
            bsc.settings.game.farmingMode === "Guild Wars" ||
            bsc.settings.game.farmingMode === "Dread Barrage" ||
            bsc.settings.game.farmingMode === "Proving Grounds" ||
            bsc.settings.game.farmingMode === "Xeno Clash" ||
            bsc.settings.game.farmingMode === "Arcarum" ||
            bsc.settings.game.farmingMode === "Arcarum Sandbox" ||
            bsc.settings.game.farmingMode === "Generic"
        ) {
            if (bsc.settings.game.mission !== "") {
                // Filter items based on the mission selected.
                Object.entries(data[bsc.settings.game.farmingMode]).forEach((missionObj) => {
                    if (missionObj[0] === bsc.settings.game.mission) {
                        missionObj[1].items.forEach((item) => {
                            newItemList.push({
                                label: item,
                                value: item,
                            })
                        })
                    }
                })
            } else {
                // Display all items.
                Object.values(data[bsc.settings.game.farmingMode]).forEach((tempItems) => {
                    tempItems.items.forEach((item) => {
                        fullItemList.push({
                            label: item,
                            value: item,
                        })
                    })
                })
            }
        }

        if (newItemList !== itemList) {
            if (newItemList.length > 0) {
                let filteredNewItemList = newItemList.filter((value, index, self) => index === self.findIndex((t) => t.label === value.label))
                setItemList(filteredNewItemList)
            } else {
                let filteredFullItemList = fullItemList.filter((value, index, self) => index === self.findIndex((t) => t.label === value.label))
                setItemList(filteredFullItemList)
            }
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [bsc.settings.game.farmingMode, bsc.settings.game.mission])

    // Populate the mission list after selecting the item.
    useEffect(() => {
        var newMissionList: DataProps[] = []
        var fullMissionList: DataProps[] = []

        if (
            bsc.settings.game.farmingMode === "Quest" ||
            bsc.settings.game.farmingMode === "Special" ||
            bsc.settings.game.farmingMode === "Raid" ||
            bsc.settings.game.farmingMode === "Event" ||
            bsc.settings.game.farmingMode === "Event (Token Drawboxes)" ||
            bsc.settings.game.farmingMode === "Rise of the Beasts" ||
            bsc.settings.game.farmingMode === "Guild Wars" ||
            bsc.settings.game.farmingMode === "Dread Barrage" ||
            bsc.settings.game.farmingMode === "Proving Grounds" ||
            bsc.settings.game.farmingMode === "Xeno Clash" ||
            bsc.settings.game.farmingMode === "Arcarum" ||
            bsc.settings.game.farmingMode === "Arcarum Sandbox" ||
            bsc.settings.game.farmingMode === "Generic"
        ) {
            Object.entries(data[bsc.settings.game.farmingMode]).forEach((obj) => {
                if (obj[1].items.indexOf(bsc.settings.game.item) !== -1) {
                    newMissionList.push({
                        label: obj[0],
                        value: obj[0],
                    })
                } else {
                    fullMissionList.push({
                        label: obj[0],
                        value: obj[0],
                    })
                }
            })
        } else {
            Object.entries(data["Coop"]).forEach((obj) => {
                if (obj[1].items.indexOf(bsc.settings.game.item) !== -1) {
                    newMissionList.push({
                        label: obj[0],
                        value: obj[0],
                    })
                } else {
                    fullMissionList.push({
                        label: obj[0],
                        value: obj[0],
                    })
                }
            })
        }

        if (newMissionList !== missionList) {
            if (newMissionList.length > 0) {
                let filteredNewMissionList = newMissionList.filter((value, index, self) => index === self.findIndex((t) => t.label === value.label))
                setMissionList(filteredNewMissionList)
            } else {
                let filteredFullMissionList = fullMissionList.filter((value, index, self) => index === self.findIndex((t) => t.label === value.label))
                setMissionList(filteredFullMissionList)
            }
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [bsc.settings.game.item])

    // Fetch the map that corresponds to the selected mission if applicable. Not for Coop.
    useEffect(() => {
        if (
            bsc.settings.game.farmingMode === "Quest" ||
            bsc.settings.game.farmingMode === "Special" ||
            bsc.settings.game.farmingMode === "Raid" ||
            bsc.settings.game.farmingMode === "Event" ||
            bsc.settings.game.farmingMode === "Event (Token Drawboxes)" ||
            bsc.settings.game.farmingMode === "Rise of the Beasts" ||
            bsc.settings.game.farmingMode === "Guild Wars" ||
            bsc.settings.game.farmingMode === "Dread Barrage" ||
            bsc.settings.game.farmingMode === "Proving Grounds" ||
            bsc.settings.game.farmingMode === "Xeno Clash" ||
            bsc.settings.game.farmingMode === "Arcarum" ||
            bsc.settings.game.farmingMode === "Arcarum Sandbox" ||
            bsc.settings.game.farmingMode === "Generic"
        ) {
            Object.entries(data[bsc.settings.game.farmingMode]).every((obj) => {
                if (obj[0] === bsc.settings.game.mission) {
                    bsc.setSettings({ ...bsc.settings, game: { ...bsc.settings.game, map: obj[1].map } })
                    return false
                } else {
                    return true
                }
            })
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [bsc.settings.game.mission])

    const renderCombatScriptSetting = () => {
        if (!bsc.settings.misc.alternativeCombatScriptSelector) {
            return (
                <FileInput
                    placeholder="None Selected"
                    label="Combat Script"
                    description="Select a Combat Script text file."
                    value={bsc.combatScriptFile}
                    onChange={(file) => {
                        loadCombatScript(bsc, file)
                        if (file !== null) bsc.setCombatScriptFile(file)
                        else bsc.setCombatScriptFile(undefined)
                    }}
                    clearable
                />
            )
        } else {
            return (
                <FileInput
                    placeholder="None Selected"
                    label="Combat Script"
                    description="Select a Combat Script text file (alternative method)."
                    onChange={(file) => {
                        loadCombatScriptAlternative(bsc)
                        if (file !== null) bsc.setCombatScriptFile(file)
                        else bsc.setCombatScriptFile(undefined)
                    }}
                    clearable
                />
            )
        }
    }

    const renderFarmingModeSetting = () => {
        return (
            <Grid>
                <Grid.Col span={6}>
                    <CustomSelect
                        label="Farming Mode"
                        placeholder="Please select the Farming Mode"
                        data={farmingModes}
                        value={bsc.settings.game.farmingMode}
                        onChange={(value) => {
                            // In addition, also reset selected Item and Mission.
                            bsc.setSettings({
                                ...bsc.settings,
                                game: { ...bsc.settings.game, farmingMode: value, item: "", mission: "", map: "" },
                                nightmare: {
                                    ...bsc.settings.nightmare,
                                    enableNightmare: false,
                                    enableCustomNightmareSettings: false,
                                    nightmareCombatScriptName: "",
                                    nightmareCombatScript: [],
                                    nightmareSummons: [],
                                    nightmareSummonElements: [],
                                    nightmareGroupNumber: 1,
                                    nightmarePartyNumber: 1,
                                },
                                sandbox: {
                                    ...bsc.settings.sandbox,
                                    enableDefender: false,
                                    enableGoldChest: false,
                                    enableCustomDefenderSettings: false,
                                    numberOfDefenders: 1,
                                    defenderCombatScriptName: "",
                                    defenderCombatScript: [],
                                    defenderGroupNumber: 1,
                                    defenderPartyNumber: 1,
                                },
                            })
                        }}
                    />
                </Grid.Col>
                <Grid.Col span={6} />
                {bsc.settings.game.farmingMode === "Special" ||
                bsc.settings.game.farmingMode === "Event" ||
                bsc.settings.game.farmingMode === "Event (Token Drawboxes)" ||
                bsc.settings.game.farmingMode === "Rise of the Beasts" ||
                bsc.settings.game.farmingMode === "Xeno Clash" ? (
                    <>
                        <Grid.Col span={6} sx={{ marginLeft: 0 }}>
                            <CustomSwitch
                                label="Enable Nightmare Settings"
                                description="Enable additional settings to show up in the Extra Settings page."
                                checked={bsc.settings.nightmare.enableNightmare}
                                onChange={(value) => bsc.setSettings({ ...bsc.settings, nightmare: { ...bsc.settings.nightmare, enableNightmare: value } })}
                            />
                        </Grid.Col>
                        <Grid.Col span={6} />
                    </>
                ) : null}
                <Grid.Col span={6}>
                    {ArcarumHelper()}
                    {ArcarumSandboxHelper()}
                    {EventHelper()}
                    {GenericHelper()}
                    {GuildWarsHelper()}
                    {ProvingGroundsHelper()}
                    {ROTBHelper()}
                    {XenoClashHelper()}
                </Grid.Col>
                <Grid.Col span={6} />
            </Grid>
        )
    }

    const renderItemSetting = () => {
        return (
            <CustomSelect
                label="Select Item"
                placeholder="Please select/search the Item to farm"
                data={itemList}
                value={bsc.settings.game.item}
                disabled={bsc.settings.game.farmingMode === ""}
                onChange={(value) => {
                    var newItem = ""
                    if (value !== null) {
                        newItem = value
                    }

                    bsc.setSettings({ ...bsc.settings, game: { ...bsc.settings.game, item: newItem } })
                }}
            />
        )
    }

    const renderMissionSetting = () => {
        if (bsc.settings.game.farmingMode !== "Generic") {
            return (
                <CustomSelect
                    label="Select Mission"
                    placeholder="Please select the Mission"
                    data={missionList}
                    value={bsc.settings.game.mission}
                    disabled={bsc.settings.game.item === ""}
                    onChange={(value) => {
                        if (value === null) {
                            bsc.setSettings({ ...bsc.settings, game: { ...bsc.settings.game, mission: "", map: "" } })
                        } else {
                            bsc.setSettings({ ...bsc.settings, game: { ...bsc.settings.game, mission: value } })
                        }
                    }}
                />
            )
        } else return null
    }

    const renderItemAmountSetting = () => {
        return (
            <CustomNumberInput
                label="# of Items"
                placeholder="Please select the amount of Items to farm"
                value={bsc.settings.game.itemAmount}
                disabled={bsc.settings.game.item === ""}
                onChange={(value) => bsc.setSettings({ ...bsc.settings, game: { ...bsc.settings.game, itemAmount: value } })}
                min={1}
            />
        )
    }

    const renderSummonSetting = () => {
        return (
            <Container>
                <Group position="center">
                    <Button
                        disabled={bsc.settings.game.farmingMode === "Coop" || bsc.settings.game.farmingMode === "Arcarum" || bsc.settings.game.farmingMode === "Arcarum Sandbox"}
                        onClick={() => setIsModalOpen(!isModalOpen)}
                    >
                        Select Support Summons
                    </Button>
                </Group>
                <Modal opened={isModalOpen} onClose={() => setIsModalOpen(false)} title="Select your Support Summons" centered size="xl">
                    <CustomTransferList />
                </Modal>
            </Container>
        )
    }

    const renderGroupPartySettings = () => {
        if (bsc.settings.game.farmingMode !== "Generic") {
            return (
                <Grid justify="center" align="center">
                    <Grid.Col id="gridItemGroup" span={4}>
                        <CustomNumberInput
                            label="Group #"
                            description={`Set A: 1 to 7 -- Set B: 8 to 14`}
                            value={bsc.settings.game.groupNumber}
                            onChange={(value) => bsc.setSettings({ ...bsc.settings, game: { ...bsc.settings.game, groupNumber: value } })}
                            min={1}
                            max={14}
                        />
                    </Grid.Col>
                    <Grid.Col id="gridItemParty" span={4} offset={4}>
                        <CustomNumberInput
                            label="Party #"
                            description="From 1 to 6"
                            value={bsc.settings.game.partyNumber}
                            onChange={(value) => bsc.setSettings({ ...bsc.settings, game: { ...bsc.settings.game, partyNumber: value } })}
                            min={1}
                            max={6}
                        />
                    </Grid.Col>
                </Grid>
            )
        } else return null
    }

    return (
        <Container className={classes.container}>
            <Stack spacing="xs">
                {renderCombatScriptSetting()}

                <Divider my="xs" labelPosition="center" label={<Icon icon="material-symbols:settings" height={25} width={25} style={{ color: "purple" }} />} />

                {renderFarmingModeSetting()}
                {renderItemSetting()}
                {renderMissionSetting()}
                {renderItemAmountSetting()}
                {renderSummonSetting()}
                {renderGroupPartySettings()}

                <Divider my="xs" labelPosition="center" label={<Icon icon="material-symbols:settings" height={25} width={25} style={{ color: "purple" }} />} />

                <CustomSwitch
                    label="Enabled Debug Mode"
                    description="Enables debugging messages to show up in the log."
                    checked={bsc.settings.game.debugMode}
                    onChange={(checked) => bsc.setSettings({ ...bsc.settings, game: { ...bsc.settings.game, debugMode: checked } })}
                />
            </Stack>
        </Container>
    )
}

export default Settings
