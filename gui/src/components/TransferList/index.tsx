import { useState } from "react"
import { Grid, List, ListItem, ListItemText, Paper } from "@mui/material"

const TransferList = () => {
    const [leftList, setLeftList] = useState<number[]>([1, 2, 3])
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
        <Paper>
            <List dense component="div">
                {items.map((value: number) => {
                    const labelID = `list-item-${value}-label`
                    return (
                        <ListItem key={value} button onClick={handleChecked(value, isLeftList)}>
                            <ListItemText id={labelID} primary={value} />
                        </ListItem>
                    )
                })}
            </List>
        </Paper>
    )

    return (
        <Grid id="hello" container spacing={2} className="grid">
            <Grid item className="gridItem">
                {customList(leftList, true)}
            </Grid>
            <Grid item className="gridItem">
                {customList(rightList, false)}
            </Grid>
        </Grid>
    )
}

export default TransferList
