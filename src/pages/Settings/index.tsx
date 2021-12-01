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

    const botStateContext = useContext(BotStateContext)

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
                            botStateContext.setSettings({
                                ...botStateContext.settings,
                                game: { ...botStateContext.settings.game, combatScriptName: filePath.replace(/^.*[\\/]/, ""), combatScript: newCombatScript },
                            })
                        })
                        .catch((err) => {
                            console.log(`Failed to read combat script via alternative method: ${err}\n\nReseting to default empty combat script...`)
                            botStateContext.setSettings({ ...botStateContext.settings, game: { ...botStateContext.settings.game, combatScriptName: "", combatScript: [] } })
                        })
                } else {
                    console.log(`No file selected.\n\nReseting to default empty combat script...`)
                    botStateContext.setSettings({ ...botStateContext.settings, game: { ...botStateContext.settings.game, combatScriptName: "", combatScript: [] } })
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
                botStateContext.setSettings({ ...botStateContext.settings, game: { ...botStateContext.settings.game, combatScriptName: "", combatScript: [] } })
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
                        botStateContext.setSettings({ ...botStateContext.settings, game: { ...botStateContext.settings.game, combatScriptName: selectedFile.name, combatScript: newCombatScript } })
                    } else {
                        console.log("Failed to read combat script. Reseting to default empty combat script...")
                        botStateContext.setSettings({ ...botStateContext.settings, game: { ...botStateContext.settings.game, combatScriptName: "", combatScript: [] } })
                    }
                }

                // Read the text contents of the file.
                reader.readAsText(selectedFile)
            }
        } else {
            console.log("No file selected. Reseting to default empty combat script...")
            botStateContext.setSettings({ ...botStateContext.settings, game: { ...botStateContext.settings.game, combatScriptName: "", combatScript: [] } })
        }
    }

    // Populate the item list after selecting the Farming Mode.
    useEffect(() => {
        var newItemList: string[] = []

        if (
            botStateContext.settings.game.farmingMode === "Quest" ||
            botStateContext.settings.game.farmingMode === "Special" ||
            botStateContext.settings.game.farmingMode === "Coop" ||
            botStateContext.settings.game.farmingMode === "Raid" ||
            botStateContext.settings.game.farmingMode === "Event" ||
            botStateContext.settings.game.farmingMode === "Event (Token Drawboxes)" ||
            botStateContext.settings.game.farmingMode === "Rise of the Beasts" ||
            botStateContext.settings.game.farmingMode === "Guild Wars" ||
            botStateContext.settings.game.farmingMode === "Dread Barrage" ||
            botStateContext.settings.game.farmingMode === "Proving Grounds" ||
            botStateContext.settings.game.farmingMode === "Xeno Clash" ||
            botStateContext.settings.game.farmingMode === "Arcarum"
        ) {
            Object.values(data[botStateContext.settings.game.farmingMode]).forEach((tempItems) => {
                newItemList = newItemList.concat(tempItems.items)
            })
        }

        const filteredNewItemList = Array.from(new Set(newItemList))
        setItemList(filteredNewItemList)
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [botStateContext.settings.game.farmingMode])

    // Populate the mission list after selecting the item.
    useEffect(() => {
        var newMissionList: string[] = []

        if (
            botStateContext.settings.game.farmingMode === "Quest" ||
            botStateContext.settings.game.farmingMode === "Special" ||
            botStateContext.settings.game.farmingMode === "Raid" ||
            botStateContext.settings.game.farmingMode === "Event" ||
            botStateContext.settings.game.farmingMode === "Event (Token Drawboxes)" ||
            botStateContext.settings.game.farmingMode === "Rise of the Beasts" ||
            botStateContext.settings.game.farmingMode === "Guild Wars" ||
            botStateContext.settings.game.farmingMode === "Dread Barrage" ||
            botStateContext.settings.game.farmingMode === "Proving Grounds" ||
            botStateContext.settings.game.farmingMode === "Xeno Clash" ||
            botStateContext.settings.game.farmingMode === "Arcarum"
        ) {
            Object.entries(data[botStateContext.settings.game.farmingMode]).forEach((obj) => {
                if (obj[1].items.indexOf(botStateContext.settings.game.item) !== -1) {
                    newMissionList = newMissionList.concat(obj[0])
                }
            })
        } else {
            Object.entries(data["Coop"]).forEach((obj) => {
                if (obj[1].items.indexOf(botStateContext.settings.game.item) !== -1) {
                    newMissionList = newMissionList.concat(obj[0])
                }
            })
        }

        const filteredNewMissionList = Array.from(new Set(newMissionList))
        setMissionList(filteredNewMissionList)
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [botStateContext.settings.game.item])

    // Fetch the map that corresponds to the selected mission if applicable.
    useEffect(() => {
        if (
            botStateContext.settings.game.farmingMode === "Quest" ||
            botStateContext.settings.game.farmingMode === "Special" ||
            botStateContext.settings.game.farmingMode === "Raid" ||
            botStateContext.settings.game.farmingMode === "Event" ||
            botStateContext.settings.game.farmingMode === "Event (Token Drawboxes)" ||
            botStateContext.settings.game.farmingMode === "Rise of the Beasts" ||
            botStateContext.settings.game.farmingMode === "Guild Wars" ||
            botStateContext.settings.game.farmingMode === "Dread Barrage" ||
            botStateContext.settings.game.farmingMode === "Proving Grounds" ||
            botStateContext.settings.game.farmingMode === "Xeno Clash" ||
            botStateContext.settings.game.farmingMode === "Arcarum"
        ) {
            Object.entries(data[botStateContext.settings.game.farmingMode]).every((obj) => {
                if (obj[0] === botStateContext.settings.game.mission) {
                    botStateContext.setSettings({ ...botStateContext.settings, game: { ...botStateContext.settings.game, map: obj[1].map } })
                    return false
                } else {
                    return true
                }
            })
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [botStateContext.settings.game.mission])

    // Show or hide the Support Summon Selection component.
    const handleModalOpen = () => setIsModalOpen(true)
    const handleModalClose = () => setIsModalOpen(false)

    return (
        <Fade in={true}>
            <Box className={botStateContext.settings.misc.guiLowPerformanceMode ? "settingsContainerLowPerformance" : "settingsContainer"} id="settingsContainer">
                <Stack spacing={2} className="settingsWrapper">
                    {/* Load Combat Script */}
                    <div>
                        {!botStateContext.settings.misc.alternativeCombatScriptSelector ? (
                            <div>
                                <Input ref={inputRef} accept=".txt" id="combat-script-loader" type="file" onChange={(e) => loadCombatScript(e)} />
                                <TextField
                                    variant="filled"
                                    label="Combat Script"
                                    value={botStateContext.settings.game.combatScriptName !== "" ? botStateContext.settings.game.combatScriptName : "None Selected"}
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
                                value={botStateContext.settings.game.combatScriptName !== "" ? botStateContext.settings.game.combatScriptName : "None Selected"}
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
                        value={botStateContext.settings.game.farmingMode}
                        onChange={(e) => {
                            // In addition, also reset selected Item and Mission.
                            botStateContext.setSettings({
                                ...botStateContext.settings,
                                game: { ...botStateContext.settings.game, farmingMode: e.target.value, item: "", mission: "", map: "" },
                                nightmare: {
                                    ...botStateContext.settings.nightmare,
                                    enableNightmare: false,
                                    enableCustomNightmareSettings: false,
                                    nightmareCombatScriptName: "",
                                    nightmareCombatScript: [],
                                    nightmareSummons: [],
                                    nightmareSummonElements: [],
                                    nightmareGroupNumber: 1,
                                    nightmarePartyNumber: 1,
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

                    {botStateContext.settings.game.farmingMode === "Special" ||
                    botStateContext.settings.game.farmingMode === "Event" ||
                    botStateContext.settings.game.farmingMode === "Event (Token Drawboxes)" ||
                    botStateContext.settings.game.farmingMode === "Rise of the Beasts" ||
                    botStateContext.settings.game.farmingMode === "Xeno Clash" ? (
                        <FormGroup sx={{ paddingBottom: "16px" }}>
                            <FormControlLabel
                                control={
                                    <Checkbox
                                        checked={botStateContext.settings.nightmare.enableNightmare}
                                        onChange={(e) =>
                                            botStateContext.setSettings({ ...botStateContext.settings, nightmare: { ...botStateContext.settings.nightmare, enableNightmare: e.target.checked } })
                                        }
                                    />
                                }
                                label="Enable Nightmare Settings"
                            />
                            <FormHelperText>Enable additional settings to show up in the Extra Settings page.</FormHelperText>
                        </FormGroup>
                    ) : (
                        ""
                    )}

                    {botStateContext.settings.game.farmingMode === "Arcarum" ? (
                        <FormGroup sx={{ paddingBottom: "16px" }}>
                            <FormControlLabel
                                control={
                                    <Checkbox
                                        checked={botStateContext.settings.arcarum.enableStopOnArcarumBoss}
                                        onChange={(e) =>
                                            botStateContext.setSettings({ ...botStateContext.settings, arcarum: { ...botStateContext.settings.arcarum, enableStopOnArcarumBoss: e.target.checked } })
                                        }
                                    />
                                }
                                label="Enable Stop on Arcarum Boss"
                            />
                            <FormHelperText>Enable this option to have the bot upon encountering a Arcarum Boss (3-3, 6-3, 9-9).</FormHelperText>
                        </FormGroup>
                    ) : (
                        ""
                    )}

                    {/* Select Item */}
                    <Autocomplete
                        options={itemList.map((element) => element)}
                        value={botStateContext.settings.game.item}
                        onChange={(_e, value) => {
                            var newItem = ""
                            if (value !== null) {
                                newItem = value
                            }

                            // In addition, also reset the selected Mission.
                            botStateContext.setSettings({ ...botStateContext.settings, game: { ...botStateContext.settings.game, item: newItem, mission: "", map: "" } })
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
                    <Autocomplete
                        options={missionList.map((element) => element)}
                        value={botStateContext.settings.game.mission}
                        onChange={(_e, value) => {
                            if (value === null) {
                                botStateContext.setSettings({ ...botStateContext.settings, game: { ...botStateContext.settings.game, mission: "", map: "" } })
                            } else {
                                botStateContext.setSettings({ ...botStateContext.settings, game: { ...botStateContext.settings.game, mission: value } })
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

                    {/* Select # of Items to farm */}
                    <TextField
                        label="# of Items"
                        type="number"
                        variant="filled"
                        value={botStateContext.settings.game.itemAmount}
                        onChange={(e) =>
                            botStateContext.setSettings({ ...botStateContext.settings, game: { ...botStateContext.settings.game, itemAmount: e.target.value === "" ? 1 : parseInt(e.target.value) } })
                        }
                        inputProps={{ min: 1 }}
                        helperText="Please select the amount of Items to farm"
                    />

                    {/* Select Summon(s) */}
                    <Button variant="contained" onClick={handleModalOpen} disabled={botStateContext.settings.game.farmingMode === "Coop" || botStateContext.settings.game.farmingMode === "Arcarum"}>
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
                    <Grid container justifyContent="center" alignItems="center">
                        <Grid item id="gridItemGroup" xs={4}>
                            <TextField
                                label="Group #"
                                variant="filled"
                                type="number"
                                error={botStateContext.settings.game.groupNumber < 1 || botStateContext.settings.game.groupNumber > 7}
                                value={botStateContext.settings.game.groupNumber}
                                inputProps={{ min: 1, max: 7 }}
                                onChange={(e) => botStateContext.setSettings({ ...botStateContext.settings, game: { ...botStateContext.settings.game, groupNumber: parseInt(e.target.value) } })}
                                helperText="From 1 to 7"
                                className="settingsTextfield"
                            />
                        </Grid>
                        <Grid item md></Grid>
                        <Grid item id="gridItemParty" xs={4}>
                            <TextField
                                label="Party #"
                                variant="filled"
                                type="number"
                                error={botStateContext.settings.game.partyNumber < 1 || botStateContext.settings.game.partyNumber > 6}
                                value={botStateContext.settings.game.partyNumber}
                                inputProps={{ min: 1, max: 6 }}
                                onChange={(e) => botStateContext.setSettings({ ...botStateContext.settings, game: { ...botStateContext.settings.game, partyNumber: parseInt(e.target.value) } })}
                                helperText="From 1 to 6"
                                className="settingsTextfield"
                            />
                        </Grid>
                    </Grid>

                    <Divider>
                        <Avatar sx={{ bgcolor: deepPurple[500] }}>
                            <SettingsIcon />
                        </Avatar>
                    </Divider>

                    {/* Debug Mode */}
                    <FormGroup>
                        <FormControlLabel
                            control={
                                <Checkbox
                                    onChange={(e) => botStateContext.setSettings({ ...botStateContext.settings, game: { ...botStateContext.settings.game, debugMode: e.target.checked } })}
                                    checked={botStateContext.settings.game.debugMode}
                                />
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
