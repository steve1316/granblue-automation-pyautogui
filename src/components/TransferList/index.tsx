import { Card, CardActionArea, CardMedia, Divider, Grid, Grow, List, ListItem, ListItemText, Paper, Tooltip, Typography, Zoom } from "@mui/material"
import { useContext, useEffect, useState } from "react"
import { BotStateContext, Settings } from "../../context/BotStateContext"
import summonData from "../../data/summons.json"
import "./index.scss"

const TransferList = ({ isNightmare }: { isNightmare: boolean }) => {
    const [leftList, setLeftList] = useState<string[]>([])
    const [rightList, setRightList] = useState<string[]>([])

    const botStateContext = useContext(BotStateContext)

    // Populate the Support Summon List.
    useEffect(() => {
        // Populate the left list.
        var oldLeftList: string[] = leftList

        Object.entries(summonData).forEach((key) => {
            key[1].summons.forEach((summon) => {
                oldLeftList = [...oldLeftList, summon]
            })
        })

        oldLeftList = Array.from(new Set(oldLeftList))

        // Populate the right list.
        var oldRightList: string[] = []
        if (!isNightmare) {
            oldRightList = botStateContext.settings.summons
        } else {
            oldRightList = botStateContext.settings.nightmareSummons
        }

        // Filter out summons from the left list that are already selected.
        const filteredList = oldLeftList.filter((summon) => !oldRightList.includes(summon))

        setLeftList(filteredList)
        setRightList(oldRightList)
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])

    const handleChecked = (value: string, isLeftList: boolean) => () => {
        var newRightList: string[] = []
        if (isLeftList) {
            // Handle the left list.
            const index = leftList.indexOf(value)
            const newLeftList = [...leftList]
            newLeftList.splice(index, 1)
            setLeftList(newLeftList)

            // Move the element to the right list.
            newRightList = [...rightList, value]
            setRightList(newRightList)
        } else {
            // Handle the right list
            const index = rightList.indexOf(value)
            newRightList = [...rightList]
            newRightList.splice(index, 1)
            setRightList(newRightList)

            // Move the element to the left list.
            const newLeftList = [...leftList, value]
            setLeftList(newLeftList)
        }

        // Save selected summons to settings.
        const localSettings: Settings = botStateContext.settings
        if (!isNightmare) {
            localSettings.summons = newRightList
            localSettings.summonElements = []
        } else {
            localSettings.nightmareSummons = newRightList
            localSettings.nightmareSummonElements = []
        }

        botStateContext.setSettings(localSettings)
    }

    const customList = (items: string[], isLeftList: boolean) => (
        <Card className="transferCard">
            <Paper elevation={2}>
                <Typography variant="h5" component="div" className="transferCardHeader">
                    {isLeftList ? "Available Support Summons" : "Selected Support Summons"}
                </Typography>
            </Paper>

            <Divider />
            <List
                dense
                component="div"
                sx={{
                    width: "100%",
                    height: "50vh",
                    overflow: "auto",
                }}
            >
                {items.map((value: string, index: number) => {
                    const fileName = value.replaceAll(" ", "_").toLowerCase()
                    return (
                        <Tooltip key={`${index}-${value}`} title={`${value}`} placement="left" arrow TransitionComponent={Zoom} TransitionProps={{ timeout: 200 }}>
                            <Grow in={true}>
                                <ListItem button onClick={handleChecked(value, isLeftList)}>
                                    <Card>
                                        <CardActionArea>
                                            <CardMedia component="img" image={require(`../../images/summons/${fileName}.png`).default} />
                                        </CardActionArea>
                                    </Card>
                                    <ListItemText className="transferListItemText" primary={value} />
                                </ListItem>
                            </Grow>
                        </Tooltip>
                    )
                })}
            </List>
        </Card>
    )

    return (
        <Grid id="supportSummonGrid" container justifyContent="center" alignItems="center">
            <Grid item id="gridItem1">
                {customList(leftList, true)}
            </Grid>
            <Grid item id="gridItem2">
                {customList(rightList, false)}
            </Grid>
        </Grid>
    )
}

export default TransferList
