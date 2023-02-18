import ArcarumHelper from "./FarmingModesHelpers/ArcarumHelper"
import ArcarumSandboxHelper from "./FarmingModesHelpers/ArcarumSandboxHelper"
import data from "../../data/data.json"
import EventHelper from "./FarmingModesHelpers/EventHelper"
import GenericHelper from "./FarmingModesHelpers/GenericHelper"
import GuildWarsHelper from "./FarmingModesHelpers/GuildWarsHelper"
import match from "autosuggest-highlight/match"
import parse from "autosuggest-highlight/parse"
import ProvingGroundsHelper from "./FarmingModesHelpers/ProvingGroundsHelper"
import ROTBHelper from "./FarmingModesHelpers/ROTBHelper"
import TransferList from "../../components/TransferList"
import XenoClashHelper from "./FarmingModesHelpers/XenoClashHelper"
import { Autocomplete, Avatar, Button, Checkbox, Divider, Fade, FormControlLabel, FormGroup, FormHelperText, Grid, MenuItem, Modal, Stack, styled, TextField, Typography } from "@mui/material"
import { BotStateContext } from "../../context/BotStateContext"
import { Box } from "@mui/system"
import { deepPurple } from "@mui/material/colors"
import { DialogFilter, open } from "@tauri-apps/api/dialog"
import { readTextFile } from "@tauri-apps/api/fs"
import { Settings as SettingsIcon } from "@mui/icons-material"
import { useContext, useEffect, useRef, useState } from "react"
import "./index.scss"

// Custom input component for combat script file selection.
const Input = styled("input")({
    display: "none",
})

const Settings = () => {
    const [itemList, setItemList] = useState<string[]>([])
    const [missionList, setMissionList] = useState<string[]>([])
    const [isModalOpen, setIsModalOpen] = useState<boolean>(false)

    const bsc = useContext(BotStateContext)

    const inputRef = useRef<HTMLInputElement>(null)

    const farmingModes: string[] = [
        "Quest",
        "Special",
        "Coop",
        "Raid",
        "Event",
        "Event (Token Drawboxes)",
        "Rise of the Beasts",
        "Guild Wars",
        "Dread Barrage",
        "Proving Grounds",
        "Xeno Clash",
        "Arcarum",
        "Arcarum Sandbox",
        "Generic",
    ]

    const loadCombatScriptAlternative = () => {
        // Use an alternative file picker for selecting the combat script.
        let filter: DialogFilter = {
            extensions: ["txt"],
            name: "Combat Script filter",
        }

        open({ defaultPath: undefined, filters: [filter], multiple: false })
            .then((filePath) => {
                if (typeof filePath === "string") {
                    readTextFile(filePath)
                        .then((data) => {
                            console.log("Loaded Combat Script via alternative method: ", data)
                            const newCombatScript: string[] = data
                                .toString()
                                .replace(/\r\n/g, "\n") // Replace LF with CRLF.
                                .replace(/[\r\n]/g, "\n")
                                .replace("\t", "") // Replace tab characters.
                                .replace(/\t/g, "")
                                .split("\n")
                            bsc.setSettings({
                                ...bsc.settings,
                                game: { ...bsc.settings.game, combatScriptName: filePath.replace(/^.*[\\/]/, ""), combatScript: newCombatScript },
                            })
                        })
                        .catch((err) => {
                            console.log(`Failed to read combat script via alternative method: ${err}\n\nReseting to default empty combat script...`)
                            bsc.setSettings({ ...bsc.settings, game: { ...bsc.settings.game, combatScriptName: "", combatScript: [] } })
                        })
                } else {
                    console.log(`No file selected.\n\nReseting to default empty combat script...`)
                    bsc.setSettings({ ...bsc.settings, game: { ...bsc.settings.game, combatScriptName: "", combatScript: [] } })
                }
            })
            .catch((e) => {
                console.log("Error while resolving the path to the combat script: ", e)
            })
    }

    // Load the selected combat script text file.
    const loadCombatScript = (event: React.ChangeEvent<HTMLInputElement>) => {
        var files = event.currentTarget.files
        if (files !== null && files.length !== 0) {
            var selectedFile = files[0]
            if (selectedFile === null || selectedFile === undefined) {
                // Reset the combat script selected if none was selected from the file picker dialog.
                bsc.setSettings({ ...bsc.settings, game: { ...bsc.settings.game, combatScriptName: "", combatScript: [] } })
            } else {
                // Create the FileReader object and setup the function that will run after the FileReader reads the text file.
                const reader = new FileReader()
                reader.onload = function (loadedEvent) {
                    if (loadedEvent.target?.result !== null && loadedEvent.target?.result !== undefined) {
                        console.log("Loaded Combat Script: ", loadedEvent.target.result)
                        const newCombatScript: string[] = loadedEvent.target.result
                            .toString()
                            .replace(/\r\n/g, "\n") // Replace LF with CRLF.
                            .replace(/[\r\n]/g, "\n")
                            .replace("\t", "") // Replace tab characters.
                            .replace(/\t/g, "")
                            .split("\n")
                        bsc.setSettings({ ...bsc.settings, game: { ...bsc.settings.game, combatScriptName: selectedFile.name, combatScript: newCombatScript } })
                    } else {
                        console.log("Failed to read combat script. Reseting to default empty combat script...")
                        bsc.setSettings({ ...bsc.settings, game: { ...bsc.settings.game, combatScriptName: "", combatScript: [] } })
                    }
                }

                // Read the text contents of the file.
                reader.readAsText(selectedFile)
            }
        } else {
            console.log("No file selected. Reseting to default empty combat script...")
            bsc.setSettings({ ...bsc.settings, game: { ...bsc.settings.game, combatScriptName: "", combatScript: [] } })
        }
    }

    // Populate the item list after selecting the Farming Mode.
    useEffect(() => {
        var newItemList: string[] = []
        var fullItemList: string[] = []

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
                        newItemList = newItemList.concat(missionObj[1].items)
                    }
                })
            } else {
                // Display all items.
                Object.values(data[bsc.settings.game.farmingMode]).forEach((tempItems) => {
                    fullItemList = fullItemList.concat(tempItems.items)
                })
            }
        }

        if (newItemList !== itemList) {
            if (newItemList.length > 0) {
                const filteredNewItemList = Array.from(new Set(newItemList))
                setItemList(filteredNewItemList)
            } else {
                const filteredFullItemList = Array.from(new Set(fullItemList))
                setItemList(filteredFullItemList)
            }
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [bsc.settings.game.farmingMode, bsc.settings.game.mission])

    // Populate the mission list after selecting the item.
    useEffect(() => {
        var newMissionList: string[] = []
        var fullMissionList: string[] = []

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
                    newMissionList = newMissionList.concat(obj[0])
                } else {
                    fullMissionList = fullMissionList.concat(obj[0])
                }
            })
        } else {
            Object.entries(data["Coop"]).forEach((obj) => {
                if (obj[1].items.indexOf(bsc.settings.game.item) !== -1) {
                    newMissionList = newMissionList.concat(obj[0])
                } else {
                    fullMissionList = fullMissionList.concat(obj[0])
                }
            })
        }

        if (newMissionList !== missionList) {
            if (newMissionList.length > 0) {
                const filteredNewMissionList = Array.from(new Set(newMissionList))
                setMissionList(filteredNewMissionList)
            } else {
                const filteredFullMissionList = Array.from(new Set(fullMissionList))
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

    // Show or hide the Support Summon Selection component.
    const handleModalOpen = () => setIsModalOpen(true)
    const handleModalClose = () => setIsModalOpen(false)

    const renderCombatScriptSetting = () => {
        if (!bsc.settings.misc.alternativeCombatScriptSelector) {
            return (
                <div>
                    <Input ref={inputRef} accept=".txt" id="combat-script-loader" type="file" onChange={(e) => loadCombatScript(e)} />
                    <TextField
                        variant="filled"
                        label="Combat Script"
                        value={bsc.settings.game.combatScriptName !== "" ? bsc.settings.game.combatScriptName : "None Selected"}
                        inputProps={{ readOnly: true }}
                        InputLabelProps={{ shrink: true }}
                        helperText="Select a Combat Script"
                        onClick={() => inputRef.current?.click()}
                        fullWidth
                    />
                </div>
            )
        } else {
            return (
                <TextField
                    variant="filled"
                    label="Combat Script"
                    value={bsc.settings.game.combatScriptName !== "" ? bsc.settings.game.combatScriptName : "None Selected"}
                    inputProps={{ readOnly: true }}
                    InputLabelProps={{ shrink: true }}
                    helperText="Select a Combat Script (alternative method)"
                    onClick={() => loadCombatScriptAlternative()}
                    fullWidth
                />
            )
        }
    }

    const renderFarmingModeSetting = () => {
        return (
            <div>
                <TextField
                    select
                    label="Farming Mode"
                    variant="filled"
                    value={bsc.settings.game.farmingMode}
                    onChange={(e) => {
                        // In addition, also reset selected Item and Mission.
                        bsc.setSettings({
                            ...bsc.settings,
                            game: { ...bsc.settings.game, farmingMode: e.target.value, item: "", mission: "", map: "" },
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
                    helperText="Please select the Farming Mode"
                    style={{ width: "100%" }}
                >
                    {farmingModes.map((mode) => (
                        <MenuItem key={mode} value={mode}>
                            {mode}
                        </MenuItem>
                    ))}
                </TextField>

                {bsc.settings.game.farmingMode === "Special" ||
                bsc.settings.game.farmingMode === "Event" ||
                bsc.settings.game.farmingMode === "Event (Token Drawboxes)" ||
                bsc.settings.game.farmingMode === "Rise of the Beasts" ||
                bsc.settings.game.farmingMode === "Xeno Clash" ? (
                    <FormGroup sx={{ paddingBottom: "16px" }}>
                        <FormControlLabel
                            control={
                                <Checkbox
                                    checked={bsc.settings.nightmare.enableNightmare}
                                    onChange={(e) => bsc.setSettings({ ...bsc.settings, nightmare: { ...bsc.settings.nightmare, enableNightmare: e.target.checked } })}
                                />
                            }
                            label="Enable Nightmare Settings"
                        />
                        <FormHelperText>Enable additional settings to show up in the Extra Settings page.</FormHelperText>
                    </FormGroup>
                ) : null}

                {ArcarumHelper()}
                {ArcarumSandboxHelper()}
                {EventHelper()}
                {GenericHelper()}
                {GuildWarsHelper()}
                {ProvingGroundsHelper()}
                {ROTBHelper()}
                {XenoClashHelper()}
            </div>
        )
    }

    const renderItemSetting = () => {
        return (
            <Autocomplete
                options={itemList.map((element) => element)}
                value={bsc.settings.game.item}
                onChange={(_e, value) => {
                    var newItem = ""
                    if (value !== null) {
                        newItem = value
                    }

                    bsc.setSettings({ ...bsc.settings, game: { ...bsc.settings.game, item: newItem } })
                }}
                getOptionLabel={(option) => option}
                isOptionEqualToValue={(option) => option !== ""}
                renderInput={(params) => <TextField {...params} label="Select Item" variant="filled" helperText="Please select/search the Item to farm" />}
                renderOption={(props, option, { inputValue }) => {
                    const matches = match(option, inputValue)
                    const parts = parse(option, matches)

                    return (
                        <li {...props}>
                            <div>
                                {parts.map((part, index) => (
                                    <span key={index} style={{ fontWeight: part.highlight ? 1000 : 400 }}>
                                        {part.text}
                                    </span>
                                ))}
                            </div>
                        </li>
                    )
                }}
            />
        )
    }

    const renderMissionSetting = () => {
        if (bsc.settings.game.farmingMode !== "Generic") {
            return (
                <Autocomplete
                    options={missionList.map((element) => element)}
                    value={bsc.settings.game.mission}
                    onChange={(_e, value) => {
                        if (value === null) {
                            bsc.setSettings({ ...bsc.settings, game: { ...bsc.settings.game, mission: "", map: "" } })
                        } else {
                            bsc.setSettings({ ...bsc.settings, game: { ...bsc.settings.game, mission: value } })
                        }
                    }}
                    getOptionLabel={(option) => option}
                    isOptionEqualToValue={(option) => option !== ""}
                    renderInput={(params) => <TextField {...params} label="Select Mission" variant="filled" helperText="Please select the Mission" />}
                    renderOption={(props, option, { inputValue }) => {
                        const matches = match(option, inputValue)
                        const parts = parse(option, matches)

                        return (
                            <li {...props}>
                                <div>
                                    {parts.map((part, index) => (
                                        <span key={index} style={{ fontWeight: part.highlight ? 1000 : 400 }}>
                                            {part.text}
                                        </span>
                                    ))}
                                </div>
                            </li>
                        )
                    }}
                />
            )
        } else return null
    }

    const renderItemAmountSetting = () => {
        return (
            <TextField
                label="# of Items"
                type="number"
                variant="filled"
                value={bsc.settings.game.itemAmount}
                onChange={(e) => bsc.setSettings({ ...bsc.settings, game: { ...bsc.settings.game, itemAmount: e.target.value === "" ? 1 : parseInt(e.target.value) } })}
                inputProps={{ min: 1 }}
                helperText="Please select the amount of Items to farm"
            />
        )
    }

    const renderSummonSetting = () => {
        return (
            <div>
                <Button
                    variant="contained"
                    onClick={handleModalOpen}
                    disabled={bsc.settings.game.farmingMode === "Coop" || bsc.settings.game.farmingMode === "Arcarum" || bsc.settings.game.farmingMode === "Arcarum Sandbox"}
                    style={{ width: "100%" }}
                >
                    Select Summons
                </Button>
                <Modal className="supportSummonModal" open={isModalOpen} onClose={handleModalClose}>
                    <div>
                        <Typography>Select Support Summon(s)</Typography>
                        <Box id="supportSummonContainer" className="supportSummonContainer">
                            <TransferList isNightmare={false} />
                        </Box>
                    </div>
                </Modal>
            </div>
        )
    }

    const renderGroupPartySettings = () => {
        if (bsc.settings.game.farmingMode !== "Generic") {
            return (
                <Grid container justifyContent="center" alignItems="center">
                    <Grid item id="gridItemGroup" xs={4}>
                        <TextField
                            label="Group #"
                            variant="filled"
                            type="number"
                            error={bsc.settings.game.groupNumber < 1 || bsc.settings.game.groupNumber > 14}
                            value={bsc.settings.game.groupNumber}
                            inputProps={{ min: 1, max: 14 }}
                            onChange={(e) => bsc.setSettings({ ...bsc.settings, game: { ...bsc.settings.game, groupNumber: parseInt(e.target.value) } })}
                            helperText={`Set A: 1 to 7\nSet B: 8 to 14`}
                            className="settingsTextfield"
                        />
                    </Grid>
                    <Grid item md></Grid>
                    <Grid item id="gridItemParty" xs={4}>
                        <TextField
                            label="Party #"
                            variant="filled"
                            type="number"
                            error={bsc.settings.game.partyNumber < 1 || bsc.settings.game.partyNumber > 6}
                            value={bsc.settings.game.partyNumber}
                            inputProps={{ min: 1, max: 6 }}
                            onChange={(e) => bsc.setSettings({ ...bsc.settings, game: { ...bsc.settings.game, partyNumber: parseInt(e.target.value) } })}
                            helperText="From 1 to 6"
                            className="settingsTextfield"
                        />
                    </Grid>
                </Grid>
            )
        } else return null
    }

    return (
        <Fade in={true}>
            <Box className={bsc.settings.misc.guiLowPerformanceMode ? "settingsContainerLowPerformance" : "settingsContainer"} id="settingsContainer">
                <Stack spacing={2} className="settingsWrapper">
                    {renderCombatScriptSetting()}

                    <Divider>
                        <Avatar sx={{ bgcolor: deepPurple[500] }}>
                            <SettingsIcon />
                        </Avatar>
                    </Divider>

                    {renderFarmingModeSetting()}

                    {renderItemSetting()}

                    {renderMissionSetting()}

                    {renderItemAmountSetting()}

                    {renderSummonSetting()}

                    {renderGroupPartySettings()}

                    <Divider>
                        <Avatar sx={{ bgcolor: deepPurple[500] }}>
                            <SettingsIcon />
                        </Avatar>
                    </Divider>

                    <FormGroup>
                        <FormControlLabel
                            control={
                                <Checkbox onChange={(e) => bsc.setSettings({ ...bsc.settings, game: { ...bsc.settings.game, debugMode: e.target.checked } })} checked={bsc.settings.game.debugMode} />
                            }
                            label="Enable Debug Mode"
                        />
                        <FormHelperText>Enables debugging messages to show up in the log</FormHelperText>
                    </FormGroup>
                </Stack>
            </Box>
        </Fade>
    )
}

export default Settings
