import { Container, createStyles, Grid, Button, Modal, Group, FileInput, Textarea, Stack, Divider } from "@mantine/core"
import { useContext, useState } from "react"
import CustomSwitch from "../../components/CustomSwitch"
import CustomNumberInput from "../../components/CustomNumberInput"
import { BotStateContext } from "../../context/BotStateContext"
import CustomTransferList from "../../components/CustomTransferList"
import { Icon } from "@iconify/react"
import { loadCombatScript, loadCombatScriptAlternative } from "../../helpers/CombatScriptHelper"
import { Text } from "@mantine/core"
import axios, { AxiosError } from "axios"
import { Command } from "@tauri-apps/api/shell"
import toast from "react-hot-toast"

const ExtraSettings = () => {
    const useStyles = createStyles((theme) => ({
        container: {
            width: "100%",
            height: "100%",
            padding: "10px 20px 10px 20px",
        },
        disabledText: {
            color: theme.colors.gray[7],
        },
    }))

    const { classes } = useStyles()

    const [testPID, setTestPID] = useState(0)
    const [isModalOpen, setIsModalOpen] = useState<boolean>(false)
    const [testInProgress, setTestInProgress] = useState<boolean>(false)

    const bsc = useContext(BotStateContext)

    const renderTwitterSettings = () => {
        return (
            <Grid>
                <Grid.Col span={12}>
                    <Text id="twitter">
                        Twitter Settings <Icon icon="akar-icons:twitter-fill" className="twitterTitleIcon" />
                    </Text>
                    <Text>Please visit the wiki on the GitHub page for instructions on how to get these keys and tokens.</Text>
                </Grid.Col>

                <Grid.Col span={12}>
                    <CustomSwitch
                        label="Enable if using Twitter API V2. Disable if using V1.1"
                        description="If enabled, then only the bearer token will be needed. No need for the consumer keys and such."
                        checked={bsc.settings.twitter.twitterUseVersion2}
                        onChange={(checked) => bsc.setSettings({ ...bsc.settings, twitter: { ...bsc.settings.twitter, twitterUseVersion2: checked } })}
                    />
                </Grid.Col>

                <Grid.Col span={12}>
                    <Grid grow sx={{ width: "100%" }}>
                        {!bsc.settings.twitter.twitterUseVersion2 ? (
                            <>
                                <Grid.Col span={6}>
                                    <Textarea
                                        label="API Key"
                                        placeholder="Insert API Key here"
                                        value={bsc.settings.twitter.twitterAPIKey}
                                        onChange={(e) => bsc.setSettings({ ...bsc.settings, twitter: { ...bsc.settings.twitter, twitterAPIKey: e.target.value } })}
                                        minRows={2}
                                    />
                                </Grid.Col>
                                <Grid.Col span={6}>
                                    <Textarea
                                        label="API Key Secret"
                                        placeholder="Insert API Key Secret here"
                                        value={bsc.settings.twitter.twitterAPIKeySecret}
                                        onChange={(e) => bsc.setSettings({ ...bsc.settings, twitter: { ...bsc.settings.twitter, twitterAPIKeySecret: e.target.value } })}
                                        minRows={2}
                                    />
                                </Grid.Col>
                                <Grid.Col span={6}>
                                    <Textarea
                                        label="Access Token"
                                        placeholder="Insert Access Token here"
                                        value={bsc.settings.twitter.twitterAccessToken}
                                        onChange={(e) => bsc.setSettings({ ...bsc.settings, twitter: { ...bsc.settings.twitter, twitterAccessToken: e.target.value } })}
                                        minRows={2}
                                    />
                                </Grid.Col>
                                <Grid.Col span={6}>
                                    <Textarea
                                        label="Access Token Secret"
                                        placeholder="Insert Access Token Secret here"
                                        value={bsc.settings.twitter.twitterAccessTokenSecret}
                                        onChange={(e) => bsc.setSettings({ ...bsc.settings, twitter: { ...bsc.settings.twitter, twitterAccessTokenSecret: e.target.value } })}
                                        minRows={2}
                                    />
                                </Grid.Col>
                            </>
                        ) : (
                            <Grid.Col span={12}>
                                <Textarea
                                    label="Bearer Token"
                                    placeholder="Insert Bearer Token here"
                                    value={bsc.settings.twitter.twitterBearerToken}
                                    onChange={(e) => bsc.setSettings({ ...bsc.settings, twitter: { ...bsc.settings.twitter, twitterBearerToken: e.target.value } })}
                                    minRows={2}
                                />
                            </Grid.Col>
                        )}

                        <Grid.Col span={4}>
                            <Button disabled={testInProgress} onClick={() => testTwitter()}>
                                Test Twitter API
                            </Button>
                        </Grid.Col>
                    </Grid>
                </Grid.Col>
            </Grid>
        )
    }

    const renderDiscordSettings = () => {
        return (
            <Grid>
                <Grid.Col span={12}>
                    <Text id="discord">
                        Discord Settings <Icon icon="akar-icons:discord-fill" className="discordTitleIcon" />
                    </Text>
                    <Text>Please visit the wiki on the GitHub page for instructions on how to get the token and user ID.</Text>
                </Grid.Col>

                <Grid.Col span={12}>
                    <CustomSwitch
                        label="Enable Discord Notifications"
                        description="Enable notifications of loot drops and errors encountered by the bot via Discord DMs."
                        checked={bsc.settings.discord.enableDiscordNotifications}
                        onChange={(checked) => bsc.setSettings({ ...bsc.settings, discord: { ...bsc.settings.discord, enableDiscordNotifications: checked } })}
                    />
                </Grid.Col>

                <Grid.Col span={12}>
                    <Grid grow sx={{ width: "100%" }}>
                        {bsc.settings.discord.enableDiscordNotifications ? (
                            <>
                                <Grid.Col span={6}>
                                    <Textarea
                                        label="Discord Token"
                                        placeholder="Insert Discord Token here"
                                        value={bsc.settings.discord.discordToken}
                                        onChange={(e) => bsc.setSettings({ ...bsc.settings, discord: { ...bsc.settings.discord, discordToken: e.target.value } })}
                                        minRows={2}
                                    />
                                </Grid.Col>
                                <Grid.Col span={6}>
                                    <Textarea
                                        label="User ID"
                                        placeholder="Insert User ID here"
                                        value={bsc.settings.discord.discordUserID}
                                        onChange={(e) => bsc.setSettings({ ...bsc.settings, discord: { ...bsc.settings.discord, discordUserID: e.target.value } })}
                                        minRows={2}
                                    />
                                </Grid.Col>
                                <Grid.Col span={4}>
                                    <Button disabled={testInProgress} onClick={() => testDiscord()}>
                                        Test Discord API
                                    </Button>
                                </Grid.Col>
                            </>
                        ) : null}
                    </Grid>
                </Grid.Col>
            </Grid>
        )
    }

    const renderConfigurationSettings = () => {
        return (
            <Grid>
                <Grid.Col span={12}>
                    <Text id="configuration">
                        Configuration Settings <Icon icon="icon-park-outline:setting-config" className="sectionTitleIcon" />
                    </Text>
                    <Text>
                        The following setting below is useful if you have a fast enough connection that pages load almost instantly. If the amount selected reduces the delay to the negatives, then it
                        will default back to its original delay. Beware that changing this setting may lead to unintended behavior as the bot will be going faster, depending on how much you reduce
                        each delay by.
                    </Text>
                </Grid.Col>

                <Grid.Col span={6}>
                    <CustomNumberInput
                        label="Reduce Delays by X Seconds"
                        value={bsc.settings.configuration.reduceDelaySeconds}
                        onChange={(value) => bsc.setSettings({ ...bsc.settings, configuration: { ...bsc.settings.configuration, reduceDelaySeconds: value } })}
                        min={0}
                        step={0.01}
                        description="Reduces each delay across the whole application by X amount of seconds."
                    />
                </Grid.Col>
                <Grid.Col span={6} />

                <Grid.Col span={12}>
                    <Grid>
                        <Grid.Col span={6}>
                            <CustomSwitch
                                label="Enable Bezier Curve Mouse Movement"
                                description="Enable this option to have slow but human-like mouse movement. Disable this for fast but bot-like mouse movement. Note that enabling this will disable the Mouse Speed setting."
                                checked={bsc.settings.configuration.enableBezierCurveMouseMovement}
                                onChange={(checked) => bsc.setSettings({ ...bsc.settings, configuration: { ...bsc.settings.configuration, enableBezierCurveMouseMovement: checked } })}
                            />
                        </Grid.Col>
                        <Grid.Col span={6}>
                            {!bsc.settings.configuration.enableBezierCurveMouseMovement ? (
                                <CustomNumberInput
                                    label="Mouse Speed"
                                    value={bsc.settings.configuration.mouseSpeed}
                                    onChange={(value) => bsc.setSettings({ ...bsc.settings, configuration: { ...bsc.settings.configuration, mouseSpeed: value } })}
                                    min={0}
                                    step={0.01}
                                    description="Set how fast a mouse operation finishes."
                                />
                            ) : null}
                        </Grid.Col>

                        <Grid.Col span={6}>
                            <CustomSwitch
                                label="Enable Delay Between Runs"
                                description="Enable delay in seconds between runs to serve as a resting period."
                                checked={bsc.settings.configuration.enableDelayBetweenRuns}
                                onChange={(checked) => {
                                    if (checked && bsc.settings.configuration.enableRandomizedDelayBetweenRuns) {
                                        bsc.setSettings({ ...bsc.settings, configuration: { ...bsc.settings.configuration, enableDelayBetweenRuns: true, enableRandomizedDelayBetweenRuns: false } })
                                    } else {
                                        bsc.setSettings({ ...bsc.settings, configuration: { ...bsc.settings.configuration, enableDelayBetweenRuns: checked } })
                                    }
                                }}
                            />
                        </Grid.Col>
                        <Grid.Col span={6}>
                            {bsc.settings.configuration.enableDelayBetweenRuns && !bsc.settings.configuration.enableRandomizedDelayBetweenRuns ? (
                                <CustomNumberInput
                                    label="Delay In Seconds"
                                    value={bsc.settings.configuration.delayBetweenRuns}
                                    onChange={(value) => bsc.setSettings({ ...bsc.settings, configuration: { ...bsc.settings.configuration, delayBetweenRuns: value } })}
                                    min={0}
                                    step={0.01}
                                    description="Set the delay in seconds for the resting period."
                                />
                            ) : null}
                        </Grid.Col>

                        <Grid.Col span={6}>
                            <CustomSwitch
                                label="Enable Randomized Delay Between Runs"
                                description="Enable randomized delay in seconds between runs to serve as a resting period."
                                checked={bsc.settings.configuration.enableRandomizedDelayBetweenRuns}
                                onChange={(checked) => {
                                    if (checked && bsc.settings.configuration.enableDelayBetweenRuns) {
                                        bsc.setSettings({ ...bsc.settings, configuration: { ...bsc.settings.configuration, enableDelayBetweenRuns: false, enableRandomizedDelayBetweenRuns: true } })
                                    } else {
                                        bsc.setSettings({ ...bsc.settings, configuration: { ...bsc.settings.configuration, enableRandomizedDelayBetweenRuns: checked } })
                                    }
                                }}
                            />
                        </Grid.Col>
                        <Grid.Col span={12}>
                            {!bsc.settings.configuration.enableDelayBetweenRuns && bsc.settings.configuration.enableRandomizedDelayBetweenRuns ? (
                                <Grid sx={{ width: "100%" }}>
                                    <Grid.Col span={6}>
                                        <CustomNumberInput
                                            label="Delay In Seconds Lower Bound"
                                            value={bsc.settings.configuration.delayBetweenRunsLowerBound}
                                            onChange={(value) => {
                                                // Perform validation so that the value does not violate the opposing bound.
                                                if (value > bsc.settings.configuration.delayBetweenRunsUpperBound) {
                                                    bsc.setSettings({
                                                        ...bsc.settings,
                                                        configuration: { ...bsc.settings.configuration, delayBetweenRunsLowerBound: bsc.settings.configuration.delayBetweenRunsUpperBound },
                                                    })
                                                } else {
                                                    bsc.setSettings({ ...bsc.settings, configuration: { ...bsc.settings.configuration, delayBetweenRunsLowerBound: value } })
                                                }
                                            }}
                                            min={1}
                                            step={0.01}
                                            description="Set the Lower Bound for the resting period."
                                        />
                                    </Grid.Col>
                                    <Grid.Col span={6}>
                                        <CustomNumberInput
                                            label="Delay In Seconds Upper Bound"
                                            value={bsc.settings.configuration.delayBetweenRunsUpperBound}
                                            onChange={(value) => {
                                                // Perform validation so that the value does not violate the opposing bound.
                                                if (value < bsc.settings.configuration.delayBetweenRunsLowerBound) {
                                                    bsc.setSettings({
                                                        ...bsc.settings,
                                                        configuration: { ...bsc.settings.configuration, delayBetweenRunsUpperBound: bsc.settings.configuration.delayBetweenRunsLowerBound },
                                                    })
                                                } else {
                                                    bsc.setSettings({ ...bsc.settings, configuration: { ...bsc.settings.configuration, delayBetweenRunsUpperBound: value } })
                                                }
                                            }}
                                            min={1}
                                            step={0.01}
                                            description="Set the Upper Bound for the resting period."
                                        />
                                    </Grid.Col>
                                </Grid>
                            ) : null}
                        </Grid.Col>

                        <Grid.Col span={6}>
                            <CustomSwitch
                                label="Enable Auto Exiting Raids"
                                description="Enables backing out of a Raid without retreating while under Semi/Full Auto after a certain period of time has passed."
                                checked={bsc.settings.raid.enableAutoExitRaid}
                                onChange={(checked) => {
                                    bsc.setSettings({ ...bsc.settings, raid: { ...bsc.settings.raid, enableAutoExitRaid: checked } })
                                }}
                            />
                        </Grid.Col>
                        <Grid.Col span={6}>
                            {bsc.settings.raid.enableAutoExitRaid ? (
                                <CustomNumberInput
                                    label="Max Time Allowed for Semi/Full Auto"
                                    value={bsc.settings.raid.timeAllowedUntilAutoExitRaid}
                                    onChange={(value) => bsc.setSettings({ ...bsc.settings, raid: { ...bsc.settings.raid, timeAllowedUntilAutoExitRaid: value } })}
                                    min={1}
                                    max={15}
                                    description="Set the maximum amount of minutes to be in a Raid while under Semi/Full Auto before moving on to the next Raid."
                                />
                            ) : null}
                        </Grid.Col>

                        <Grid.Col span={6}>
                            <CustomSwitch
                                label="Enable No Timeout"
                                description="Enable no timeouts when attempting to farm Raids that appear infrequently."
                                checked={bsc.settings.raid.enableNoTimeout}
                                onChange={(checked) => bsc.setSettings({ ...bsc.settings, raid: { ...bsc.settings.raid, enableNoTimeout: checked } })}
                            />
                        </Grid.Col>
                        <Grid.Col span={6}>
                            <CustomSwitch
                                label="Enable Refreshing during Combat"
                                description="Enables the ability to refresh to speed up Combat Mode whenever the Attack button disappears when it is pressed or during Full/Semi Auto. This option takes precedence above any
                        other related setting to reloading during combat except via the reload command in a script."
                                checked={bsc.settings.configuration.enableRefreshDuringCombat}
                                onChange={(checked) => bsc.setSettings({ ...bsc.settings, configuration: { ...bsc.settings.configuration, enableRefreshDuringCombat: checked } })}
                            />
                        </Grid.Col>

                        <Grid.Col span={6}>
                            <CustomSwitch
                                label="Enable Automatic Quick Summon during Full/Semi Auto"
                                description='Enables the ability to automatically use Quick Summon during Full/Semi Auto. Note that this option only takes into effect when "Enable Refreshing during Combat" is turned on
                        and that the bot is fighting a battle that is compatible with refreshing during combat.'
                                checked={bsc.settings.configuration.enableAutoQuickSummon}
                                onChange={(checked) => bsc.setSettings({ ...bsc.settings, configuration: { ...bsc.settings.configuration, enableAutoQuickSummon: checked } })}
                            />
                        </Grid.Col>
                        <Grid.Col span={6}>
                            <CustomSwitch
                                label="Enable Bypassing Reset Summon Procedure"
                                description="Enables bypassing the bot resetting Summons if there are none of your chosen found during Summon Selection. The bot will reload the page and select the very first summon at the
                        top of the list."
                                checked={bsc.settings.configuration.enableBypassResetSummon}
                                onChange={(checked) => bsc.setSettings({ ...bsc.settings, configuration: { ...bsc.settings.configuration, enableBypassResetSummon: checked } })}
                            />
                        </Grid.Col>

                        <Grid.Col span={6}>
                            <CustomSwitch
                                label="Enable static window calibration"
                                description="Enable calibration of game window to be static. This will assume that you do not move the game window around during the bot process. Otherwise, the bot will not see where to go
                        next. Disable to have the whole computer screen act as the game window and you can move around the window during the bot process as you wish."
                                checked={bsc.settings.configuration.staticWindow}
                                onChange={(checked) => bsc.setSettings({ ...bsc.settings, configuration: { ...bsc.settings.configuration, staticWindow: checked } })}
                            />
                        </Grid.Col>
                        <Grid.Col span={6}>
                            <CustomSwitch
                                label="Enable attempt at bypassing possible bot detection via mouse"
                                description="Enable attempt at bypassing possible bot detection via mouse. What this does is moves the mouse off of the game window after every run and waits several seconds there before
                        resuming bot operations. Additionally, this also makes it so that the same thing happens at the very end of operations before shutting down."
                                checked={bsc.settings.configuration.enableMouseSecurityAttemptBypass}
                                onChange={(checked) => bsc.setSettings({ ...bsc.settings, configuration: { ...bsc.settings.configuration, enableMouseSecurityAttemptBypass: checked } })}
                            />
                        </Grid.Col>
                    </Grid>
                </Grid.Col>
            </Grid>
        )
    }

    const renderNightmareSettings = () => {
        if (
            bsc.settings.nightmare.enableNightmare &&
            (bsc.settings.game.farmingMode === "Special" ||
                bsc.settings.game.farmingMode === "Event" ||
                bsc.settings.game.farmingMode === "Event (Token Drawboxes)" ||
                bsc.settings.game.farmingMode === "Xeno Clash" ||
                bsc.settings.game.farmingMode === "Rise of the Beasts")
        ) {
            let title: string = ""
            if (bsc.settings.game.farmingMode === "Special") {
                title = "Dimensional Halo"
            } else if (bsc.settings.game.farmingMode === "Rise of the Beasts") {
                title = "Extreme+"
            } else {
                title = "Nightmare"
            }

            return (
                <Grid>
                    <Grid.Col span={12}>
                        <Text id="nightmare">
                            {title} Settings <Icon icon="ri:sword-fill" className="sectionTitleIcon" />
                        </Text>
                        <Text>If none of these settings are changed, then the bot will reuse the settings for the Farming Mode.</Text>
                    </Grid.Col>

                    <Grid.Col span={12}>
                        <CustomSwitch
                            label={`Enable Custom Settings for ${title}`}
                            description={`Enable customizing individual settings for ${title}`}
                            checked={bsc.settings.nightmare.enableCustomNightmareSettings}
                            onChange={(checked) => bsc.setSettings({ ...bsc.settings, nightmare: { ...bsc.settings.nightmare, enableCustomNightmareSettings: checked } })}
                        />
                    </Grid.Col>

                    <Grid.Col span={12}>
                        {bsc.settings.nightmare.enableCustomNightmareSettings ? (
                            <Stack>
                                {!bsc.settings.misc.alternativeCombatScriptSelector ? (
                                    <FileInput
                                        placeholder="None Selected"
                                        label="Nightmare Combat Script"
                                        description="Select a Combat Script text file."
                                        value={bsc.combatScriptFile}
                                        onChange={(file) => {
                                            loadCombatScript(bsc, file)
                                            if (file !== null) bsc.setCombatScriptFile(file)
                                            else bsc.setCombatScriptFile(undefined)
                                        }}
                                        clearable
                                    />
                                ) : (
                                    <FileInput
                                        placeholder="None Selected"
                                        label="Nightmare Combat Script"
                                        description="Select a Combat Script text file (alternative method)."
                                        onChange={(file) => {
                                            loadCombatScriptAlternative(bsc)
                                            if (file !== null) bsc.setCombatScriptFile(file)
                                            else bsc.setCombatScriptFile(undefined)
                                        }}
                                        clearable
                                    />
                                )}

                                <Group position="center">
                                    <Button onClick={() => setIsModalOpen(!isModalOpen)}>Select Nightmare Support Summons</Button>
                                </Group>
                                <Modal opened={isModalOpen} onClose={() => setIsModalOpen(false)} title="Select your Nightmare Support Summons" centered size="xl">
                                    <CustomTransferList isNightmare={true} />
                                </Modal>

                                <Grid justify="center" align="center">
                                    <Grid.Col id="gridItemNightmareGroup" span={4}>
                                        <CustomNumberInput
                                            label="Group #"
                                            description={`Set A: 1 to 7\nSet B: 8 to 14`}
                                            value={bsc.settings.nightmare.nightmareGroupNumber}
                                            onChange={(value) => bsc.setSettings({ ...bsc.settings, nightmare: { ...bsc.settings.nightmare, nightmareGroupNumber: value } })}
                                            min={1}
                                            max={14}
                                        />
                                    </Grid.Col>
                                    <Grid.Col id="gridItemNightmareParty" span={4} offset={4}>
                                        <CustomNumberInput
                                            label="Party #"
                                            description="From 1 to 6"
                                            value={bsc.settings.nightmare.nightmarePartyNumber}
                                            onChange={(value) => bsc.setSettings({ ...bsc.settings, nightmare: { ...bsc.settings.nightmare, nightmarePartyNumber: value } })}
                                            min={1}
                                            max={6}
                                        />
                                    </Grid.Col>
                                </Grid>
                            </Stack>
                        ) : null}
                    </Grid.Col>
                </Grid>
            )
        } else {
            return (
                <Grid>
                    <Grid.Col span={12}>
                        <Text id="nightmare">
                            Nightmare Settings <Icon icon="ri:sword-fill" className="sectionTitleIcon" />
                        </Text>
                        <Text className={classes.disabledText}>
                            Current Farming Mode either does not support Nightmares or the "Enable Nightmare Settings" option in the Settings page was not enabled.
                        </Text>
                    </Grid.Col>
                </Grid>
            )
        }
    }

    const renderMiscSettings = () => {
        return (
            <Grid>
                <Grid.Col span={12}>
                    <Text id="misc">
                        Misc Settings <Icon icon="dashicons:admin-settings" className="sectionTitleIcon" />
                    </Text>
                </Grid.Col>

                <Grid.Col span={12}>
                    <CustomSwitch
                        label="Enable Alternative File Picker for Combat Script selection"
                        description="Enable this if the regular method of combat script selection failed."
                        checked={bsc.settings.misc.alternativeCombatScriptSelector}
                        onChange={(checked) => bsc.setSettings({ ...bsc.settings, misc: { ...bsc.settings.misc, alternativeCombatScriptSelector: checked } })}
                    />
                </Grid.Col>
            </Grid>
        )
    }

    const renderSandboxDefenderSettings = () => {
        if (bsc.settings.sandbox.enableDefender && bsc.settings.game.farmingMode === "Arcarum Sandbox") {
            return (
                <Grid>
                    <Grid.Col span={12}>
                        <Text id="defender">
                            Defender Settings <Icon icon="ri:sword-fill" className="sectionTitleIcon" />
                        </Text>
                        <Text>If none of these settings are changed, then the bot will reuse the settings for the Farming Mode.</Text>
                    </Grid.Col>

                    <Grid.Col span={12}>
                        <Stack>
                            <CustomSwitch
                                label="Enable Custom Settings for Defender"
                                description="Enable customizing individual settings for Defender"
                                checked={bsc.settings.sandbox.enableCustomDefenderSettings}
                                onChange={(checked) => bsc.setSettings({ ...bsc.settings, sandbox: { ...bsc.settings.sandbox, enableCustomDefenderSettings: checked } })}
                            />

                            {bsc.settings.sandbox.enableCustomDefenderSettings ? (
                                <Stack align={"flex-start"}>
                                    {!bsc.settings.misc.alternativeCombatScriptSelector ? (
                                        <FileInput
                                            placeholder="None Selected"
                                            label="Defender Combat Script"
                                            description="Select a Combat Script text file."
                                            value={bsc.combatScriptFile}
                                            onChange={(file) => {
                                                loadCombatScript(bsc, file)
                                                if (file !== null) bsc.setCombatScriptFile(file)
                                                else bsc.setCombatScriptFile(undefined)
                                            }}
                                            clearable
                                        />
                                    ) : (
                                        <FileInput
                                            placeholder="None Selected"
                                            label="Defender Combat Script"
                                            description="Select a Combat Script text file (alternative method)."
                                            onChange={(file) => {
                                                loadCombatScriptAlternative(bsc)
                                                if (file !== null) bsc.setCombatScriptFile(file)
                                                else bsc.setCombatScriptFile(undefined)
                                            }}
                                            clearable
                                        />
                                    )}

                                    <CustomNumberInput
                                        label="How many times to run"
                                        description="Set how many defenders the bot should fight."
                                        value={bsc.settings.sandbox.numberOfDefenders}
                                        onChange={(value) => bsc.setSettings({ ...bsc.settings, sandbox: { ...bsc.settings.sandbox, numberOfDefenders: value } })}
                                        min={1}
                                    />

                                    <Grid justify="center" align="center">
                                        <Grid.Col id="gridItemDefenderGroup" span={4}>
                                            <CustomNumberInput
                                                label="Group #"
                                                description={`Set A: 1 to 7\nSet B: 8 to 14`}
                                                value={bsc.settings.sandbox.defenderGroupNumber}
                                                onChange={(value) => bsc.setSettings({ ...bsc.settings, sandbox: { ...bsc.settings.sandbox, defenderGroupNumber: value } })}
                                                min={1}
                                                max={14}
                                            />
                                        </Grid.Col>
                                        <Grid.Col id="gridItemDefenderParty" span={4} offset={4}>
                                            <CustomNumberInput
                                                label="Party #"
                                                description="From 1 to 6"
                                                value={bsc.settings.sandbox.defenderPartyNumber}
                                                onChange={(value) => bsc.setSettings({ ...bsc.settings, sandbox: { ...bsc.settings.sandbox, defenderPartyNumber: value } })}
                                                min={1}
                                                max={6}
                                            />
                                        </Grid.Col>
                                    </Grid>
                                </Stack>
                            ) : null}
                        </Stack>
                    </Grid.Col>
                </Grid>
            )
        } else {
            return (
                <Grid>
                    <Grid.Col span={12}>
                        <Text id="defender">
                            Defender Settings <Icon icon="ri:sword-fill" className="sectionTitleIcon" />
                        </Text>
                        <Text className={classes.disabledText}>Current Farming Mode is not set to "Arcarum Sandbox".</Text>
                    </Grid.Col>
                </Grid>
            )
        }
    }

    const renderAPIIntegrationSettings = () => {
        return (
            <Grid>
                <Grid.Col span={12}>
                    <Text id="api-integration">
                        API Integration Settings <Icon icon="mdi:api" className="sectionTitleIcon" />
                    </Text>
                    <Text>
                        You can opt-in to this feature where the bot will automatically send successful results from the Loot Collection process and you can view your results and similar ones over on
                        the Granblue Automation Statistics website.
                    </Text>
                </Grid.Col>

                <Grid.Col span={12}>
                    <CustomSwitch
                        label="Enable Opt-in for API Integration"
                        description="Enable API Integration with Granblue Automation Statistics"
                        checked={bsc.settings.api.enableOptInAPI}
                        onChange={(checked) => bsc.setSettings({ ...bsc.settings, api: { ...bsc.settings.api, enableOptInAPI: checked } })}
                    />
                </Grid.Col>

                <Grid.Col span={12}>
                    {bsc.settings.api.enableOptInAPI ? (
                        <Stack>
                            <Text>{`How this works:\n\nInput your username and password below that you used to register a new account on the website. The account registered on the website will be used to associate your success results from the Loot Collection process. A success result describes the Loot Collection process detecting a item drop after each run.`}</Text>
                            <Grid grow sx={{ width: "100%" }}>
                                <Grid.Col span={6}>
                                    <Textarea
                                        label="Username"
                                        placeholder="Insert your username here"
                                        value={bsc.settings.api.username}
                                        onChange={(e) => bsc.setSettings({ ...bsc.settings, api: { ...bsc.settings.api, username: e.target.value } })}
                                        minRows={2}
                                    />
                                </Grid.Col>
                                <Grid.Col span={6}>
                                    <Textarea
                                        label="Password"
                                        placeholder="Insert User ID here"
                                        value={bsc.settings.api.password}
                                        onChange={(e) => bsc.setSettings({ ...bsc.settings, api: { ...bsc.settings.api, password: e.target.value } })}
                                        minRows={2}
                                    />
                                </Grid.Col>
                                <Grid.Col span={4}>
                                    <Button disabled={testInProgress} onClick={(e) => testAPIIntegration(e)}>
                                        Test Login into API
                                    </Button>
                                </Grid.Col>
                            </Grid>
                        </Stack>
                    ) : null}
                </Grid.Col>
            </Grid>
        )
    }

    const renderDeviceSettings = () => {
        return (
            <Grid>
                <Grid.Col span={12}>
                    <Text id="device">
                        Device Settings <Icon icon="ic:baseline-device-unknown" className="sectionTitleIcon" />
                    </Text>
                </Grid.Col>

                <Grid.Col span={12}>
                    <CustomSwitch
                        label="Use First Notch instead of the Second"
                        description="Enable this if your screen size is small enough that the second notch makes the game too big. Using the second notch in this case will make the game reasonably fit."
                        checked={bsc.settings.device.useFirstNotch}
                        onChange={(checked) => bsc.setSettings({ ...bsc.settings, device: { ...bsc.settings.device, useFirstNotch: checked } })}
                    />
                </Grid.Col>

                <Grid.Col span={12}>
                    <Text>
                        Adjust and fine-tune settings related to device setups and image processing optimizations. The first confidence option handles single target template matching and the second
                        confidence option handles multi target template matching, including item detection.
                    </Text>
                </Grid.Col>

                <Grid.Col span={12}>
                    <Group>
                        <Stack>
                            <Grid grow sx={{ width: "100%" }}>
                                <Grid.Col span={6}>
                                    <CustomNumberInput
                                        label="Set Confidence Level"
                                        placeholder="Set the default confidence level for single-target image template matching."
                                        value={bsc.settings.device.confidence}
                                        onChange={(target) => bsc.setSettings({ ...bsc.settings, device: { ...bsc.settings.device, confidence: target } })}
                                        min={0.1}
                                        max={1.0}
                                        step={0.01}
                                    />
                                </Grid.Col>
                                <Grid.Col span={6}>
                                    <CustomNumberInput
                                        label="Set Confidence Level for Multiple Matching"
                                        placeholder="Set the default confidence level for multi-target image template matching. Example: Item Detection during Loot Collection"
                                        value={bsc.settings.device.confidenceAll}
                                        onChange={(target) => bsc.setSettings({ ...bsc.settings, device: { ...bsc.settings.device, confidenceAll: target } })}
                                        min={0.1}
                                        max={1.0}
                                        step={0.01}
                                    />
                                </Grid.Col>
                                <Grid.Col span={6}>
                                    <CustomNumberInput
                                        label="Set Custom Scale (Highly experimental)"
                                        placeholder="Set the scale at which to resize existing image assets to match what would be shown on your device. Internally supported are 1080p and 1440p. Highly experimental feature."
                                        value={bsc.settings.device.customScale}
                                        onChange={(target) => bsc.setSettings({ ...bsc.settings, device: { ...bsc.settings.device, customScale: target } })}
                                        min={0.1}
                                        max={5.0}
                                        step={0.01}
                                    />
                                </Grid.Col>
                                <Grid.Col span={6} />
                            </Grid>

                            <CustomSwitch
                                label="Enable Test for Home Screen"
                                description={`Enables test for getting to the Home screen instead of the regular bot process. If the test fails, then it will run a different test to find which scale is appropriate for your device.\n\nUseful for troubleshooting working confidences and scales for device compatibility.`}
                                checked={bsc.settings.device.enableTestForHomeScreen}
                                onChange={(checked) => bsc.setSettings({ ...bsc.settings, device: { ...bsc.settings.device, enableTestForHomeScreen: checked } })}
                            />
                        </Stack>
                    </Group>
                </Grid.Col>
            </Grid>
        )
    }

    // Attempt to kill the bot process if it is still active.
    const handleStop = async () => {
        if (testPID !== 0) {
            console.log("Killing process tree now...")
            const output = await new Command("powershell", `taskkill /F /T /PID ${testPID}`).execute() // Windows specific
            console.log(`Result of killing bot process using PID ${testPID}: \n${output.stdout}`)
            setTestPID(0)
        }
    }

    // Test Twitter API key.
    const testTwitter = async () => {
        // Construct the shell command using Tauri Command API.
        const command = new Command("python", ["backend/test.py", "9"])

        // Attach event listeners.
        command.on("close", (data) => {
            console.log(`\nChild process finished with code ${data.code}`)
            handleStop()

            setTestInProgress(false)
        })
        command.on("error", (error) => {
            console.log(`\nChild process finished with error ${error}`)
            handleStop()
            toast.error(`Child process finished with error ${error}`, { duration: 5000 })
        })
        command.stdout.on("data", (line: string) => {
            if (line.indexOf("Test successfully completed.") !== -1) {
                console.log("Testing Twitter API was successful.")
                toast.success("Testing Twitter API was successful.", { duration: 5000 })
            } else if (line.indexOf("Test failed.") !== -1) {
                console.log("Testing Twitter API was unsuccessful.")
                toast.error("Testing Twitter API was unsuccessful.", { duration: 5000 })
            }
        })
        command.stderr.on("data", (line) => {
            console.log("ERROR: ", line)
        })

        // Create the child process.
        const child = await command.spawn()
        console.log("PID: ", child.pid)
        setTestPID(child.pid)
        setTestInProgress(true)
    }

    // Test Discord API key.
    const testDiscord = async () => {
        // Construct the shell command using Tauri Command API.
        const command = new Command("python", ["backend/test.py", "10"])

        // Attach event listeners.
        command.on("close", (data) => {
            console.log(`\nChild process finished with code ${data.code}`)
            handleStop()

            setTestInProgress(false)
        })
        command.on("error", (error) => {
            console.log(`\nChild process finished with error ${error}`)
            handleStop()
            toast.error(`Child process finished with error ${error}`, { duration: 5000 })
        })
        command.stdout.on("data", (line: string) => {
            if (line.indexOf("Test successfully completed.") !== -1) {
                console.log("Testing Discord API was successful.")
                toast.success("Testing Discord API was successful.", { duration: 5000 })
            } else if (line.indexOf("Test failed.") !== -1) {
                console.log("Testing Discord API was unsuccessful.")
                toast.error("Testing Discord API was unsuccessful.", { duration: 5000 })
            }
        })
        command.stderr.on("data", (line) => {
            console.log("ERROR: ", line)
        })

        // Create the child process.
        const child = await command.spawn()
        console.log("PID: ", child.pid)
        setTestPID(child.pid)
        setTestInProgress(true)
    }

    const testAPIIntegration = (e: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
        e.preventDefault()
        setTestInProgress(true)
        axios
            .post(`${bsc.entryPoint}/api/login`, { username: bsc.settings.api.username, password: bsc.settings.api.password }, { withCredentials: true })
            .then(() => {
                toast.success("Testing API Integration was successful.", { duration: 5000 })
            })
            .catch((e: AxiosError) => {
                toast.error(`Testing API Integration was unsuccessful:\n\n${e.message}`, { duration: 5000 })
            })
            .finally(() => {
                setTestInProgress(false)
            })
    }

    return (
        <Container className={classes.container}>
            <Stack spacing="xs">
                {renderTwitterSettings()}
                <Divider my="xs" />
                {renderDiscordSettings()}
                <Divider my="xs" />
                {renderConfigurationSettings()}
                <Divider my="xs" />
                {renderNightmareSettings()}
                <Divider my="xs" />
                {renderMiscSettings()}
                <Divider my="xs" />
                {renderSandboxDefenderSettings()}
                <Divider my="xs" />
                {renderAPIIntegrationSettings()}
                <Divider my="xs" />
                {renderDeviceSettings()}
            </Stack>
        </Container>
    )
}

export default ExtraSettings
