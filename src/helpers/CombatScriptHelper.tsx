import { IProviderProps } from "../context/BotStateContext"
import { DialogFilter, open } from "@tauri-apps/api/dialog"
import { readTextFile } from "@tauri-apps/api/fs"

// Load the selected combat script text file.
export const loadCombatScript = (bsc: IProviderProps, file: File | null, isNightmare: boolean = false, isDefender: boolean = false) => {
    if (file !== null) {
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

                if (isNightmare) {
                    bsc.setSettings({ ...bsc.settings, nightmare: { ...bsc.settings.nightmare, nightmareCombatScriptName: file.name, nightmareCombatScript: newCombatScript } })
                } else if (isDefender) {
                    bsc.setSettings({ ...bsc.settings, sandbox: { ...bsc.settings.sandbox, defenderCombatScriptName: file.name, defenderCombatScript: newCombatScript } })
                } else {
                    bsc.setSettings({ ...bsc.settings, game: { ...bsc.settings.game, combatScriptName: file.name, combatScript: newCombatScript } })
                }
            } else {
                console.log("Failed to read combat script. Reseting to default empty combat script...")
                if (isNightmare) {
                    bsc.setSettings({ ...bsc.settings, nightmare: { ...bsc.settings.nightmare, nightmareCombatScriptName: "", nightmareCombatScript: [] } })
                } else if (isDefender) {
                    bsc.setSettings({ ...bsc.settings, sandbox: { ...bsc.settings.sandbox, defenderCombatScriptName: "", defenderCombatScript: [] } })
                } else {
                    bsc.setSettings({ ...bsc.settings, game: { ...bsc.settings.game, combatScriptName: "", combatScript: [] } })
                }
            }
        }

        // Read the text contents of the file.
        reader.readAsText(file)
    } else {
        console.log("No file selected. Reseting to default empty combat script...")
        if (isNightmare) {
            bsc.setSettings({ ...bsc.settings, nightmare: { ...bsc.settings.nightmare, nightmareCombatScriptName: "", nightmareCombatScript: [] } })
        } else if (isDefender) {
            bsc.setSettings({ ...bsc.settings, sandbox: { ...bsc.settings.sandbox, defenderCombatScriptName: "", defenderCombatScript: [] } })
        } else {
            bsc.setSettings({ ...bsc.settings, game: { ...bsc.settings.game, combatScriptName: "", combatScript: [] } })
        }
    }
}

export const loadCombatScriptAlternative = (bsc: IProviderProps, isNightmare: boolean = false, isDefender: boolean = false) => {
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

                        if (isNightmare) {
                            bsc.setSettings({
                                ...bsc.settings,
                                nightmare: { ...bsc.settings.nightmare, nightmareCombatScriptName: filePath.replace(/^.*[\\/]/, ""), nightmareCombatScript: newCombatScript },
                            })
                        } else if (isDefender) {
                            bsc.setSettings({
                                ...bsc.settings,
                                sandbox: { ...bsc.settings.sandbox, defenderCombatScriptName: filePath.replace(/^.*[\\/]/, ""), defenderCombatScript: newCombatScript },
                            })
                        } else {
                            bsc.setSettings({ ...bsc.settings, game: { ...bsc.settings.game, combatScriptName: filePath.replace(/^.*[\\/]/, ""), combatScript: newCombatScript } })
                        }
                    })
                    .catch((err) => {
                        console.log(`Failed to read combat script via alternative method: ${err}\n\nReseting to default empty combat script...`)
                        if (isNightmare) {
                            bsc.setSettings({ ...bsc.settings, nightmare: { ...bsc.settings.nightmare, nightmareCombatScriptName: "", nightmareCombatScript: [] } })
                        } else if (isDefender) {
                            bsc.setSettings({ ...bsc.settings, sandbox: { ...bsc.settings.sandbox, defenderCombatScriptName: "", defenderCombatScript: [] } })
                        } else {
                            bsc.setSettings({ ...bsc.settings, game: { ...bsc.settings.game, combatScriptName: "", combatScript: [] } })
                        }
                    })
            } else {
                console.log(`No file selected.\n\nReseting to default empty combat script...`)
                if (isNightmare) {
                    bsc.setSettings({ ...bsc.settings, nightmare: { ...bsc.settings.nightmare, nightmareCombatScriptName: "", nightmareCombatScript: [] } })
                } else if (isDefender) {
                    bsc.setSettings({ ...bsc.settings, sandbox: { ...bsc.settings.sandbox, defenderCombatScriptName: "", defenderCombatScript: [] } })
                } else {
                    bsc.setSettings({ ...bsc.settings, game: { ...bsc.settings.game, combatScriptName: "", combatScript: [] } })
                }
            }
        })
        .catch((e) => {
            console.log("Error while resolving the path to the combat script: ", e)
        })
}
