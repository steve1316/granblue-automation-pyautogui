import { Settings as SettingsIcon } from "@mui/icons-material"
import { Autocomplete, Avatar, Button, Checkbox, Divider, Fade, FormControlLabel, FormGroup, FormHelperText, Grid, MenuItem, Modal, Stack, TextField, Typography } from "@mui/material"
import { deepPurple } from "@mui/material/colors"
import { Box, styled } from "@mui/system"
import match from "autosuggest-highlight/match"
import parse from "autosuggest-highlight/parse"
import { useContext, useEffect, useRef, useState } from "react"
import TransferList from "../../components/TransferList"
import { BotStateContext } from "../../context/BotStateContext"
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

    // Load the selected combat script text file.
    const loadCombatScript = (event: React.ChangeEvent<HTMLInputElement>) => {
        var files = event.currentTarget.files
        if (files != null) {
            var file = files[0]
            if (file == null) {
                // Reset the combat script selected if none was selected from the file picker dialog.
                botStateContext.setCombatScriptName("")
                botStateContext.setCombatScript([])
            } else {
                botStateContext.setCombatScriptName(file.name)

                // Create the FileReader object and setup the function that will run after the FileReader reads the text file.
                var reader = new FileReader()
                reader.onload = function (loadedEvent) {
                    if (loadedEvent.target?.result != null) {
                        console.log("Loaded Combat Script: ", loadedEvent.target?.result)
                        const newCombatScript: string[] = (loadedEvent.target?.result).toString().split("\r\n")
                        botStateContext.setCombatScript(newCombatScript)
                    } else {
                        console.log("Failed to read combat script. Reseting to default empty combat script...")
                        botStateContext.setCombatScriptName("")
                        botStateContext.setCombatScript([])
                    }
                }

                // Read the text contents of the file.
                reader.readAsText(file)
            }
        }
    }

    // Populate the item list after selecting the Farming Mode.
    useEffect(() => {
        var newItemList: string[] = []

        if (
            botStateContext?.farmingMode === "Quest" ||
            botStateContext?.farmingMode === "Special" ||
            botStateContext?.farmingMode === "Coop" ||
            botStateContext?.farmingMode === "Raid" ||
            botStateContext?.farmingMode === "Event" ||
            botStateContext?.farmingMode === "Event (Token Drawboxes)" ||
            botStateContext?.farmingMode === "Rise of the Beasts" ||
            botStateContext?.farmingMode === "Guild Wars" ||
            botStateContext?.farmingMode === "Dread Barrage" ||
            botStateContext?.farmingMode === "Proving Grounds" ||
            botStateContext?.farmingMode === "Xeno Clash" ||
            botStateContext?.farmingMode === "Arcarum"
        ) {
            Object.values(data[botStateContext?.farmingMode]).forEach((tempItems) => {
                newItemList = newItemList.concat(tempItems.items)
            })
        }

        const filteredNewItemList = Array.from(new Set(newItemList))
        setItemList(filteredNewItemList)
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [botStateContext?.farmingMode])

    // Populate the mission list after selecting the item.
    useEffect(() => {
        var newMissionList: string[] = []

        if (
            botStateContext?.farmingMode === "Quest" ||
            botStateContext?.farmingMode === "Special" ||
            botStateContext?.farmingMode === "Raid" ||
            botStateContext?.farmingMode === "Event" ||
            botStateContext?.farmingMode === "Event (Token Drawboxes)" ||
            botStateContext?.farmingMode === "Rise of the Beasts" ||
            botStateContext?.farmingMode === "Guild Wars" ||
            botStateContext?.farmingMode === "Dread Barrage" ||
            botStateContext?.farmingMode === "Proving Grounds" ||
            botStateContext?.farmingMode === "Xeno Clash" ||
            botStateContext?.farmingMode === "Arcarum"
        ) {
            Object.entries(data[botStateContext?.farmingMode]).forEach((obj) => {
                if (obj[1].items.indexOf(botStateContext?.item) !== -1) {
                    newMissionList = newMissionList.concat(obj[0])
                }
            })
        } else {
            Object.entries(data["Coop"]).forEach((obj) => {
                if (obj[1].items.indexOf(botStateContext?.item) !== -1) {
                    newMissionList = newMissionList.concat(obj[0])
                }
            })
        }

        const filteredNewMissionList = Array.from(new Set(newMissionList))
        setMissionList(filteredNewMissionList)
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [botStateContext?.item])

    // Reset Nightmare settings.
    const resetNightmareSettings = () => {
        botStateContext?.setEnableNightmare(false)
        botStateContext?.setEnableCustomNightmareSettings(false)
        botStateContext?.setNightmareSummons([])
        botStateContext?.setNightmareSummonElements([])
        botStateContext?.setNightmareGroupNumber(1)
        botStateContext?.setNightmarePartyNumber(1)
    }

    // Show or hide the Support Summon Selection component.
    const handleModalOpen = () => setIsModalOpen(true)
    const handleModalClose = () => setIsModalOpen(false)

    return (
        <Fade in={true}>
            <Box className="settingsContainer" id="settingsContainer">
                <Stack spacing={2} className="settingsWrapper">
                    {/* Load Combat Script */}
                    <div>
                        <Input ref={inputRef} accept=".txt" id="combat-script-loader" type="file" onChange={(e) => loadCombatScript(e)} />
                        <TextField
                            variant="filled"
                            label="Combat Script"
                            value={botStateContext.combatScriptName !== "" ? botStateContext.combatScriptName : "None Selected"}
                            inputProps={{ readOnly: true }}
                            InputLabelProps={{ shrink: true }}
                            helperText="Select a Combat Script"
                            onClick={() => inputRef.current?.click()}
                            fullWidth
                        />
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
                        value={botStateContext?.farmingMode}
                        onChange={(e) => {
                            botStateContext?.setFarmingMode(e.target.value)

                            resetNightmareSettings()

                            // Reset selected Item and Mission.
                            botStateContext?.setItem("")
                            botStateContext?.setMission("")
                            botStateContext?.setMap("")
                        }}
                        helperText="Please select the Farming Mode"
                    >
                        {farmingModes.map((mode) => (
                            <MenuItem key={mode} value={mode}>
                                {mode}
                            </MenuItem>
                        ))}
                    </TextField>

                    {botStateContext.farmingMode === "Special" ||
                    botStateContext.farmingMode === "Event" ||
                    botStateContext.farmingMode === "Event (Token Drawboxes)" ||
                    botStateContext.farmingMode === "Rise of the Beasts" ||
                    botStateContext.farmingMode === "Xeno Clash" ? (
                        <FormGroup sx={{ paddingBottom: "16px" }}>
                            <FormControlLabel
                                control={<Checkbox checked={botStateContext.enableNightmare} onChange={(e) => botStateContext.setEnableNightmare(e.target.checked)} />}
                                label="Enable Nightmare Settings"
                            />
                            <FormHelperText>Enable additional settings to show up in the Extra Settings page.</FormHelperText>
                        </FormGroup>
                    ) : (
                        ""
                    )}

                    {/* Select Item */}
                    <Autocomplete
                        options={itemList.map((element) => element)}
                        value={botStateContext?.item}
                        onChange={(_e, value) => {
                            if (value === null) {
                                botStateContext?.setItem("")
                            } else {
                                botStateContext?.setItem(value)
                            }

                            // Reset selected Mission.
                            botStateContext?.setMission("")
                            botStateContext?.setMap("")
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
                        value={botStateContext?.mission}
                        onChange={(_e, value) => {
                            if (value === null) {
                                botStateContext?.setMission("")
                            } else {
                                botStateContext?.setMission(value)
                                if (
                                    botStateContext?.farmingMode === "Quest" ||
                                    botStateContext?.farmingMode === "Special" ||
                                    botStateContext?.farmingMode === "Raid" ||
                                    botStateContext?.farmingMode === "Event" ||
                                    botStateContext?.farmingMode === "Event (Token Drawboxes)" ||
                                    botStateContext?.farmingMode === "Rise of the Beasts" ||
                                    botStateContext?.farmingMode === "Guild Wars" ||
                                    botStateContext?.farmingMode === "Dread Barrage" ||
                                    botStateContext?.farmingMode === "Proving Grounds" ||
                                    botStateContext?.farmingMode === "Xeno Clash" ||
                                    botStateContext?.farmingMode === "Arcarum"
                                ) {
                                    Object.entries(data[botStateContext?.farmingMode]).every((obj) => {
                                        if (obj[0] === value) {
                                            botStateContext?.setMap(obj[1].map)
                                            return false
                                        } else {
                                            return true
                                        }
                                    })
                                }
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
                        value={botStateContext?.itemAmount}
                        onChange={(e) => botStateContext?.setItemAmount(e.target.value === "" ? 1 : parseInt(e.target.value))}
                        inputProps={{ min: 1 }}
                        helperText="Please select the amount of Items to farm"
                    />

                    {/* Select Summon(s) */}
                    <Button variant="contained" onClick={handleModalOpen} disabled={botStateContext?.farmingMode === "Coop" || botStateContext?.farmingMode === "Arcarum"}>
                        Select Summons
                    </Button>
                    <Modal className="modal" open={isModalOpen} onClose={handleModalClose}>
                        <div>
                            <Typography>Select Support Summon(s)</Typography>
                            <Box id="modalContainer" className="box">
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
                                error={botStateContext?.groupNumber < 1 || botStateContext?.groupNumber > 7}
                                value={botStateContext?.groupNumber}
                                inputProps={{ min: 1, max: 7 }}
                                onChange={(e) => botStateContext?.setGroupNumber(parseInt(e.target.value))}
                                helperText="From 1 to 7"
                                className="textfield"
                            />
                        </Grid>
                        <Grid item md></Grid>
                        <Grid item id="gridItemParty" xs={4}>
                            <TextField
                                label="Party #"
                                variant="filled"
                                type="number"
                                error={botStateContext?.partyNumber < 1 || botStateContext?.partyNumber > 6}
                                value={botStateContext?.partyNumber}
                                inputProps={{ min: 1, max: 6 }}
                                onChange={(e) => botStateContext?.setPartyNumber(parseInt(e.target.value))}
                                helperText="From 1 to 6"
                                className="textfield"
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
                                    onChange={(e) => {
                                        botStateContext?.setDebugMode(e.target.checked)
                                    }}
                                    checked={botStateContext?.debugMode}
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
