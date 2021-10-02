import { useState } from "react"
import { Autocomplete, Box, Button, Fade, Grid, MenuItem, Stack, TextField } from "@mui/material"
import { styled } from "@mui/system"
import "./index.scss"

const Input = styled("input")({
    display: "none",
})

const Settings = () => {
    const [fileName, setFileName] = useState("")
    const [farmingMode, setFarmingMode] = useState("")
    const [item, setItem] = useState("")
    const [mission, setMission] = useState("")
    const [itemAmount, setItemAmount] = useState(0)

    const loadCombatScript = (event: React.ChangeEvent<HTMLInputElement>) => {
        var files = event.currentTarget.files
        if (files != null) {
            var file = files[0]
            setFileName(file.name)

            // Create the FileReader object and setup the function that will run after the FileReader reads the text file.
            var reader = new FileReader()
            reader.onload = function (loadedEvent) {
                console.log(loadedEvent.target?.result)
            }

            // Read the text contents of the file.
            reader.readAsText(file)
        }
    }

    const farmingModes = ["Quest", "Special"]
    const itemsForQuest = ["Satin Feather", "Zephyr Feather", "Flying Sprout"]
    const missionsForQuest = ["test1"]

    return (
        <Fade in={true}>
            <Box className="container">
                <Stack spacing={2}>
                    <Grid container spacing={4} justifyContent="center" alignItems="center">
                        {/* Load Combat Script */}
                        <Grid item md>
                            <TextField variant="filled" label="Combat Script" value={fileName} inputProps={{ readOnly: true }} helperText="Selected Combat Script" />
                        </Grid>
                        <Grid item xs>
                            <label htmlFor="combat-script-loader">
                                <Input accept=".txt" id="combat-script-loader" type="file" onChange={(e) => loadCombatScript(e)} />
                                <Button variant="contained" component="span">
                                    Load Combat Script
                                </Button>
                            </label>
                        </Grid>
                    </Grid>

                    {/* Select Farming Mode */}
                    <TextField select label="Farming Mode" value={farmingMode} onChange={(e) => setFarmingMode(e.target.value)} helperText="Please select the Farming Mode">
                        {farmingModes.map((mode) => (
                            <MenuItem key={mode} value={mode}>
                                {mode}
                            </MenuItem>
                        ))}
                    </TextField>

                    {/* Select Item */}
                    <Autocomplete
                        freeSolo
                        disableClearable
                        options={itemsForQuest.map((element) => element)}
                        renderInput={(params) => (
                            <TextField
                                {...params}
                                label="Select Item"
                                InputProps={{
                                    ...params.InputProps,
                                    type: "search",
                                }}
                                onChange={(e) => setItem(e.target.value)}
                                helperText="Please select/search the Item to farm"
                            />
                        )}
                    />

                    {/* Select Mission */}
                    <TextField select label="Mission" value={mission} onChange={(e) => setMission(e.target.value)} helperText="Please select the Mission">
                        {missionsForQuest.map((mode) => (
                            <MenuItem key={mode} value={mode}>
                                {mode}
                            </MenuItem>
                        ))}
                    </TextField>

                    {/* Select # of Items to farm */}
                    <TextField
                        label="# of Items"
                        type="number"
                        value={itemAmount}
                        onChange={(e) => setItemAmount(e.target.value === "" ? 0 : parseInt(e.target.value))}
                        inputProps={{ min: 0 }}
                        helperText="Please select the amount of Items to farm"
                    />
                </Stack>
            </Box>
        </Fade>
    )
}

export default Settings