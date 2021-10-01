import { useState } from "react"
import { Box, Button, Fade } from "@mui/material"
import { styled } from "@mui/system"
import "./index.scss"

const Input = styled("input")({
    display: "none",
})

const Settings = () => {
    const [fileName, setFileName] = useState("")

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

    return (
        <Fade in={true}>
            <Box className="container">
                {/* Load Combat Script */}
                <label htmlFor="combat-script-loader">
                    <Input accept=".txt" id="combat-script-loader" type="file" onChange={(e) => loadCombatScript(e)} />
                    <Button variant="contained" component="span">
                        Load Combat Script
                    </Button>
                </label>
            </Box>
        </Fade>
    )
}

export default Settings
