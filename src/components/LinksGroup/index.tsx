import { useState, useEffect } from "react"
import { Group, Box, Collapse, ThemeIcon, Text, createStyles, ActionIcon } from "@mantine/core"
import { Icon } from "@iconify/react"
import { rem } from "@mantine/styles"

interface LinksGroupProps {
    label: string
    value: string
    frontIcon?: string
    initiallyOpened?: boolean
    links?: { label: string; link: string }[]
    active?: string
    setActive?: React.Dispatch<React.SetStateAction<string>>
}

const LinksGroup = ({ label, value, frontIcon = "material-symbols:home-outline", initiallyOpened, links, active = "Home", setActive = () => {} }: LinksGroupProps) => {
    const useStyles = createStyles((theme) => ({
        control: {
            fontWeight: 500,
            display: "block",
            width: "100%",
            height: "100%",
            padding: 5,
            color: theme.colorScheme === "dark" ? theme.colors.dark[0] : theme.black,
            fontSize: theme.fontSizes.sm,
            "&:hover": {
                backgroundColor: theme.colorScheme === "dark" ? theme.colors.dark[7] : theme.colors.gray[0],
                color: theme.colorScheme === "dark" ? theme.white : theme.black,
            },
        },

        linkActive: {
            "&, &:hover": {
                backgroundColor: theme.fn.variant({ variant: "light", color: theme.primaryColor }).background,
                color: theme.fn.variant({ variant: "light", color: theme.primaryColor }).color,
            },
        },

        link: {
            fontWeight: 500,
            display: "block",
            textDecoration: "none",
            padding: `${theme.spacing.xs} ${theme.spacing.md}`,
            paddingLeft: rem(30),
            marginLeft: rem(30),
            fontSize: theme.fontSizes.sm,
            color: theme.colorScheme === "dark" ? theme.colors.dark[0] : theme.colors.gray[7],
            borderLeft: `${rem(1)} solid ${theme.colorScheme === "dark" ? theme.colors.dark[4] : theme.colors.gray[3]}`,
            "&:hover": {
                backgroundColor: theme.colorScheme === "dark" ? theme.colors.dark[7] : theme.colors.gray[0],
                color: theme.colorScheme === "dark" ? theme.white : theme.black,
            },
        },

        chevron: {
            transition: "transform 200ms ease",
        },
    }))

    const { classes, theme, cx } = useStyles()
    const hasLinks = Array.isArray(links)
    const [opened, setOpened] = useState(initiallyOpened || false)
    const items = (hasLinks ? links : []).map((link) => (
        <Text<"a">
            component="a"
            className={classes.link}
            href={link.link}
            key={link.label}
            onClick={(e) => {
                e.preventDefault()

                // If there is an anchor, smooth scroll to that anchor on the new page after navigating to it.
                if (link.link.includes("#")) {
                    let id = link.link.split("#")[1]
                    document.getElementById(id)?.scrollIntoView({
                        behavior: "smooth",
                    })
                }
            }}
        >
            {link.label}
        </Text>
    ))

    const displayChevronIcon = () => {
        // Display and animate the chevron icon when the tab is made active when it has a list of links.
        if (hasLinks) {
            return theme.dir === "ltr" ? (
                <Icon
                    icon="material-symbols:chevron-right"
                    height={30}
                    width={30}
                    className={classes.chevron}
                    style={{
                        transform: opened ? `rotate(90deg)` : "none",
                    }}
                />
            ) : (
                <Icon
                    icon="material-symbols:chevron-left"
                    height={30}
                    width={30}
                    className={classes.chevron}
                    style={{
                        transform: opened ? `rotate(-90deg)` : "none",
                    }}
                />
            )
        } else {
            return null
        }
    }

    // Collapse the dropdown of links if another tab is selected.
    useEffect(() => {
        if ((label === "Extra Settings" && active !== "Extra Settings") || (label === "Adjustments" && active !== "Adjustments")) {
            setOpened(false)
        }
    }, [active])

    return (
        <Group sx={{ marginTop: 10 }}>
            <ActionIcon
                onClick={() => {
                    setActive(value)
                    setOpened(!opened)
                }}
                className={cx(classes.control, { [classes.linkActive]: active === label })}
            >
                <Group position="apart" spacing={0}>
                    <Box sx={{ display: "flex", alignItems: "center" }}>
                        <ThemeIcon variant="light" size={30}>
                            <Icon icon={frontIcon} width={20} height={20} />
                        </ThemeIcon>
                        <Box ml="md">{label}</Box>
                    </Box>

                    {displayChevronIcon()}
                </Group>
            </ActionIcon>
            {hasLinks ? <Collapse in={opened}>{items}</Collapse> : null}
        </Group>
    )
}

export default LinksGroup
