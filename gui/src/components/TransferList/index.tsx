import { useState } from "react"
import { Card, CardActionArea, CardMedia, Divider, Grid, Grow, List, ListItem, ListItemText, Paper, Tooltip, Typography, Zoom } from "@mui/material"
import "./index.scss"

const TransferList = () => {
    const [leftList, setLeftList] = useState<number[]>([1, 2, 31, 2, 31, 2, 3])
    const [rightList, setRightList] = useState<number[]>([4])

    const handleChecked = (value: number, isLeftList: boolean) => () => {
        if (isLeftList) {
            // Handle the left list.
            const index = leftList.indexOf(value)
            const newLeftList = [...leftList]
            newLeftList.splice(index, 1)
            setLeftList(newLeftList)

            // Move the element to the right list.
            const newRightList = [...rightList, value]
            setRightList(newRightList)
        } else {
            // Handle the right list
            const index = rightList.indexOf(value)
            const newRightList = [...rightList]
            newRightList.splice(index, 1)
            setRightList(newRightList)

            // Move the element to the left list.
            const newLeftList = [...leftList, value]
            setLeftList(newLeftList)
        }
    }

    const customList = (items: number[], isLeftList: boolean) => (
        <Card className="card">
            <Paper elevation={2}>
                <Typography variant="h5" component="div" className="cardHeader">
                    {isLeftList ? "Available Support Summons" : "Selected Support Summons"}
                </Typography>
            </Paper>

            <Divider />
            <List
                dense
                component="div"
                sx={{
                    width: "100%",
                    height: 200,
                    overflow: "auto",
                }}
            >
                {items.map((value: number) => {
                    const name = `test-${value}`
                    return (
                        <Tooltip title={name} placement="left" arrow TransitionComponent={Zoom} TransitionProps={{ timeout: 200 }}>
                            <Grow in={true}>
                                <ListItem key={value} button onClick={handleChecked(value, isLeftList)}>
                                    <Card className="supportSummonCard">
                                        <CardActionArea>
                                            <CardMedia component="img" image={require("../../images/agni.png").default} />
                                        </CardActionArea>
                                    </Card>
                                    <ListItemText className="listItemText" primary={value} />
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
