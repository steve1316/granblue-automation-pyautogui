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

    return (
        <Fade in={true}>
            <Box className="container">
                <Grid container spacing={2} justifyContent="center" alignItems="center">
                    {/* Load Combat Script */}
                    <Grid item xs={4}>
                        <TextField variant="filled" value={fileName} disabled />
                    </Grid>
                    <Grid item xs={4}>
                        <label htmlFor="combat-script-loader">
                            <Input accept=".txt" id="combat-script-loader" type="file" onChange={(e) => loadCombatScript(e)} />
                            <Button variant="contained" component="span">
                                Load Combat Script
                            </Button>
                        </label>
                    </Grid>
                </Grid>
                <Stack spacing={2} sx={{ marginTop: "30px" }}>
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
                                helperText="Please select/search the Item to farm"
                            />
                        )}
                    />
                </Stack>
            </Box>
        </Fade>
    )
}

export default Settings
