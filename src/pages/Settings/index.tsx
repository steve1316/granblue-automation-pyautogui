import { Settings as SettingsIcon } from "@mui/icons-material"
import { Autocomplete, Avatar, Button, Checkbox, Divider, Fade, FormControlLabel, FormGroup, FormHelperText, Grid, MenuItem, Modal, Stack, styled, TextField, Typography } from "@mui/material"
import { deepPurple } from "@mui/material/colors"
import { Box } from "@mui/system"
import match from "autosuggest-highlight/match"
import parse from "autosuggest-highlight/parse"
import { useContext, useEffect, useRef, useState } from "react"
import TransferList from "../../components/TransferList"
import { BotStateContext } from "../../context/BotStateContext"
import { readTextFile } from "@tauri-apps/api/fs"
import { open, DialogFilter } from "@tauri-apps/api/dialog"
import data from "../../data/data.json"
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

    return (
        <Fade in={true}>
            <Box className={bsc.settings.misc.guiLowPerformanceMode ? "settingsContainerLowPerformance" : "settingsContainer"} id="settingsContainer">
                <Stack spacing={2} className="settingsWrapper">
                    {/* Load Combat Script */}
                    <div>
                        {!bsc.settings.misc.alternativeCombatScriptSelector ? (
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
                        ) : (
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
                        )}
                    </div>

                    <Divider>
                        <Avatar sx={{ bgcolor: deepPurple[500] }}>
                            <SettingsIcon />
                        </Avatar>
                    </Divider>

                    {/* Select Farming Mode */}
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
                    >
                        {farmingModes.map((mode) => (
                            <MenuItem key={mode} value={mode}>
                                {mode}
                            </MenuItem>
                        ))}
                    </TextField>

                    {bsc.settings.game.farmingMode === "Generic" ? (
                        <div>
                            <Divider />
                            <Typography variant="subtitle2" component="p" color="text.secondary">
                                {`Selecting this will repeat the current mission on the screen until it finishes the required number of runs. Note that Generic does not provide any navigation.
                                
                                It is required that the bot starts on either the Combat screen with the "Attack" button visible, the Loot Collection screen with the "Play Again" button visible, or the Coop Room screen with the "Start" button visible and party already selected.`}
                            </Typography>
                            <Divider />
                        </div>
                    ) : null}

                    {bsc.settings.game.farmingMode === "Event" ? (
                        <FormGroup sx={{ paddingBottom: "16px" }}>
                            <FormControlLabel
                                control={
                                    <Checkbox
                                        checked={bsc.settings.event.enableLocationIncrementByOne}
                                        onChange={(e) => bsc.setSettings({ ...bsc.settings, event: { ...bsc.settings.event, enableLocationIncrementByOne: e.target.checked } })}
                                    />
                                }
                                label="Enable Incrementation of Location by 1"
                            />
                            <FormHelperText>
                                Enable this if the event has its N/H missions at the very top so the bot can correctly select the correct quest. Or in otherwords, enable this if the Event tab in the
                                Special page has 3 "Select" buttons instead of 2.
                            </FormHelperText>
                        </FormGroup>
                    ) : null}

                    {bsc.settings.game.farmingMode === "Event" || bsc.settings.game.farmingMode === "Event (Token Drawboxes)" ? (
                        <FormGroup sx={{ paddingBottom: "16px" }}>
                            <FormControlLabel
                                control={
                                    <Checkbox
                                        checked={bsc.settings.event.enableSecondPosition}
                                        onChange={(e) => bsc.setSettings({ ...bsc.settings, event: { ...bsc.settings.event, enableSecondPosition: e.target.checked } })}
                                    />
                                }
                                label="Enable if Event is in second position"
                            />
                            <FormHelperText>Enable this to properly select the Event if it is positioned second on the list of events in the Home Menu.</FormHelperText>
                        </FormGroup>
                    ) : null}

                    {bsc.settings.game.farmingMode === "Event" || bsc.settings.game.farmingMode === "Event (Token Drawboxes)" ? (
                        <FormGroup sx={{ paddingBottom: "16px" }}>
                            <FormControlLabel
                                control={
                                    <Checkbox
                                        checked={bsc.settings.event.enableThirdPosition}
                                        onChange={(e) => bsc.setSettings({ ...bsc.settings, event: { ...bsc.settings.event, enableThirdPosition: e.target.checked } })}
                                    />
                                }
                                label="Enable if Event is in third position"
                            />
                            <FormHelperText>Enable this to properly select the Event if it is positioned third on the list of events in the Home Menu.</FormHelperText>
                        </FormGroup>
                    ) : null}

                    {bsc.settings.game.farmingMode === "Arcarum Sandbox" ? (
                        <FormGroup sx={{ paddingBottom: "16px" }}>
                            <FormControlLabel
                                control={
                                    <Checkbox
                                        checked={bsc.settings.sandbox.enableDefender}
                                        onChange={(e) => bsc.setSettings({ ...bsc.settings, sandbox: { ...bsc.settings.sandbox, enableDefender: e.target.checked } })}
                                    />
                                }
                                label="Enable Defender settings"
                            />
                            <FormHelperText>Enable additional settings to show up in the Extra Settings page.</FormHelperText>
                        </FormGroup>
                    ) : null}

                    {bsc.settings.game.farmingMode === "Arcarum Sandbox" ? (
                        <FormGroup sx={{ paddingBottom: "16px" }}>
                            <FormControlLabel
                                control={
                                    <Checkbox
                                        checked={bsc.settings.sandbox.enableGoldChest}
                                        onChange={(e) => bsc.setSettings({ ...bsc.settings, sandbox: { ...bsc.settings.sandbox, enableGoldChest: e.target.checked } })}
                                    />
                                }
                                label="Enable gold chest opening"
                            />
                            <FormHelperText>Experimental, it uses default party and the chosen script for combat.</FormHelperText>
                        </FormGroup>
                    ) : null}

                    {bsc.settings.game.farmingMode === "Arcarum" ? (
                        <FormGroup sx={{ paddingBottom: "16px" }}>
                            <FormControlLabel
                                control={
                                    <Checkbox
                                        checked={bsc.settings.arcarum.enableStopOnArcarumBoss}
                                        onChange={(e) => bsc.setSettings({ ...bsc.settings, arcarum: { ...bsc.settings.arcarum, enableStopOnArcarumBoss: e.target.checked } })}
                                    />
                                }
                                label="Enable Stop on Arcarum Boss"
                            />
                            <FormHelperText>Enable this option to have the bot stop upon encountering a Arcarum Boss (3-3, 6-3, 9-9).</FormHelperText>
                        </FormGroup>
                    ) : null}

                    {bsc.settings.game.farmingMode === "Xeno Clash" ? (
                        <FormGroup sx={{ paddingBottom: "16px" }}>
                            <FormControlLabel
                                control={
                                    <Checkbox
                                        checked={bsc.settings.xenoClash.selectTopOption}
                                        onChange={(e) => bsc.setSettings({ ...bsc.settings, xenoClash: { ...bsc.settings.xenoClash, selectTopOption: e.target.checked } })}
                                    />
                                }
                                label="Enable Selection of Bottom Option"
                            />
                            <FormHelperText>Enabling this will select the bottom Xeno Clash option. By default, it selects the top option.</FormHelperText>
                        </FormGroup>
                    ) : null}

                    {bsc.settings.game.farmingMode === "Xeno Clash" ? (
                        <FormGroup sx={{ paddingBottom: "16px" }}>
                            <FormControlLabel
                                control={
                                    <Checkbox
                                        checked={bsc.settings.xenoClash.enableSecondPosition}
                                        onChange={(e) => bsc.setSettings({ ...bsc.settings, xenoClash: { ...bsc.settings.xenoClash, enableSecondPosition: e.target.checked } })}
                                    />
                                }
                                label="Enable if Xeno Clash is in second position"
                            />
                            <FormHelperText>Enable this to properly select Xeno Clash if it is positioned second on the list of events in the Home Menu.</FormHelperText>
                        </FormGroup>
                    ) : null}

                    {bsc.settings.game.farmingMode === "Xeno Clash" ? (
                        <FormGroup sx={{ paddingBottom: "16px" }}>
                            <FormControlLabel
                                control={
                                    <Checkbox
                                        checked={bsc.settings.xenoClash.enableThirdPosition}
                                        onChange={(e) => bsc.setSettings({ ...bsc.settings, xenoClash: { ...bsc.settings.xenoClash, enableThirdPosition: e.target.checked } })}
                                    />
                                }
                                label="Enable if Xeno Clash is in third position"
                            />
                            <FormHelperText>Enable this to properly select Xeno Clash if it is positioned third on the list of events in the Home Menu.</FormHelperText>
                        </FormGroup>
                    ) : null}

                    {bsc.settings.game.farmingMode === "Proving Grounds" ? (
                        <FormGroup sx={{ paddingBottom: "16px" }}>
                            <FormControlLabel
                                control={
                                    <Checkbox
                                        checked={bsc.settings.provingGrounds.enableSecondPosition}
                                        onChange={(e) => bsc.setSettings({ ...bsc.settings, provingGrounds: { ...bsc.settings.provingGrounds, enableSecondPosition: e.target.checked } })}
                                    />
                                }
                                label="Enable if Proving Grounds is in second position"
                            />
                            <FormHelperText>Enable this to properly select Proving Grounds if it is positioned second on the list of events in the Home Menu.</FormHelperText>
                        </FormGroup>
                    ) : null}

                    {bsc.settings.game.farmingMode === "Proving Grounds" ? (
                        <FormGroup sx={{ paddingBottom: "16px" }}>
                            <FormControlLabel
                                control={
                                    <Checkbox
                                        checked={bsc.settings.provingGrounds.enableThirdPosition}
                                        onChange={(e) => bsc.setSettings({ ...bsc.settings, provingGrounds: { ...bsc.settings.provingGrounds, enableThirdPosition: e.target.checked } })}
                                    />
                                }
                                label="Enable if Proving Grounds is in third position"
                            />
                            <FormHelperText>Enable this to properly select Proving Grounds if it is positioned third on the list of events in the Home Menu.</FormHelperText>
                        </FormGroup>
                    ) : null}

                    {bsc.settings.game.farmingMode === "Generic" ? (
                        <FormGroup sx={{ paddingBottom: "16px" }}>
                            <FormControlLabel
                                control={
                                    <Checkbox
                                        checked={bsc.settings.generic.enableForceReload}
                                        onChange={(e) => bsc.setSettings({ ...bsc.settings, generic: { ...bsc.settings.generic, enableForceReload: e.target.checked } })}
                                    />
                                }
                                label="Enable Forcing Reload after Attack"
                            />
                            <FormHelperText>
                                Enable this option to force Generic Farming Mode to reload after an attack. This does not take into account whether or not the current battle supports reloading after
                                an attack.
                            </FormHelperText>
                        </FormGroup>
                    ) : null}

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

                    {bsc.settings.game.farmingMode === "Event (Token Drawboxes)" ? (
                        <FormGroup sx={{ paddingBottom: "16px" }}>
                            <FormControlLabel
                                control={
                                    <Checkbox
                                        checked={bsc.settings.event.selectBottomCategory}
                                        onChange={(e) => bsc.setSettings({ ...bsc.settings, event: { ...bsc.settings.event, selectBottomCategory: e.target.checked } })}
                                    />
                                }
                                label="Enable Selecting the Bottom Category"
                            />
                            <FormHelperText>
                                In the event of the raids being split between 2 categories, the bot selects the top category by default. Enable this to select the bottom category instead.
                            </FormHelperText>
                        </FormGroup>
                    ) : null}

                    {/* Select Item */}
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

                    {/* Select Mission */}
                    {bsc.settings.game.farmingMode !== "Generic" ? (
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
                    ) : null}

                    {/* Select # of Items to farm */}
                    <TextField
                        label="# of Items"
                        type="number"
                        variant="filled"
                        value={bsc.settings.game.itemAmount}
                        onChange={(e) => bsc.setSettings({ ...bsc.settings, game: { ...bsc.settings.game, itemAmount: e.target.value === "" ? 1 : parseInt(e.target.value) } })}
                        inputProps={{ min: 1 }}
                        helperText="Please select the amount of Items to farm"
                    />

                    {/* Select Summon(s) */}
                    <Button
                        variant="contained"
                        onClick={handleModalOpen}
                        disabled={bsc.settings.game.farmingMode === "Coop" || bsc.settings.game.farmingMode === "Arcarum" || bsc.settings.game.farmingMode === "Arcarum Sandbox"}
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

                    {/* Select Group and Party */}
                    {bsc.settings.game.farmingMode !== "Generic" ? (
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
                    ) : null}

                    <Divider>
                        <Avatar sx={{ bgcolor: deepPurple[500] }}>
                            <SettingsIcon />
                        </Avatar>
                    </Divider>

                    {/* Debug Mode */}
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
