import { Container, createStyles, Divider, Grid, Stack, Text } from "@mantine/core"
import { useContext } from "react"
import CustomSwitch from "../../components/CustomSwitch"
import CustomNumberInput from "../../components/CustomNumberInput"
import { BotStateContext } from "../../context/BotStateContext"

const Adjustments = () => {
    const useStyles = createStyles((theme) => ({
        container: {
            width: "100%",
            height: "100%",
            padding: "10px 20px 10px 20px",
        },
    }))

    const { classes } = useStyles()

    const bsc = useContext(BotStateContext)

    const renderStart = () => {
        return (
            <Grid>
                <Grid.Col span={12}>
                    <Text id="starting-calibration">Starting Calibration</Text>
                </Grid.Col>

                <Grid.Col span={12}>
                    <CustomSwitch
                        label="Enable Starting Calibration Adjustments"
                        description="Enable adjustment of tries for Starting Calibration."
                        checked={bsc.settings.adjustment.enableCalibrationAdjustment}
                        onChange={(checked) => bsc.setSettings({ ...bsc.settings, adjustment: { ...bsc.settings.adjustment, enableCalibrationAdjustment: checked } })}
                    />
                </Grid.Col>

                <Grid.Col span={12}>
                    {bsc.settings.adjustment.enableCalibrationAdjustment ? (
                        <Grid grow sx={{ width: "100%" }}>
                            <Grid.Col span={6}>
                                <CustomNumberInput
                                    label="Home Calibration"
                                    value={bsc.settings.adjustment.adjustCalibration}
                                    onChange={(value) => bsc.setSettings({ ...bsc.settings, adjustment: { ...bsc.settings.adjustment, adjustCalibration: value } })}
                                    min={1}
                                    max={999}
                                    description="Home calibration occurs when the bot is first started and attempts to find and save the location of the game window."
                                />
                            </Grid.Col>
                            <Grid.Col span={6} />
                        </Grid>
                    ) : null}
                </Grid.Col>
            </Grid>
        )
    }

    const renderGeneral = () => {
        return (
            <Grid>
                <Grid.Col span={12}>
                    <Text id="general-image-searching">General Image Searching</Text>
                </Grid.Col>

                <Grid.Col span={12}>
                    <CustomSwitch
                        label="Enable General Image Searching Adjustments"
                        description="Enable adjustment of tries for General. This encompasses a vast majority of the image processing operations of the bot so adjusting these will greatly affect the average
                        running time."
                        checked={bsc.settings.adjustment.enableGeneralAdjustment}
                        onChange={(checked) => bsc.setSettings({ ...bsc.settings, adjustment: { ...bsc.settings.adjustment, enableGeneralAdjustment: checked } })}
                    />
                </Grid.Col>

                <Grid.Col span={12}>
                    {bsc.settings.adjustment.enableGeneralAdjustment ? (
                        <Grid grow sx={{ width: "100%" }}>
                            <Grid.Col span={6}>
                                <CustomNumberInput
                                    label="General Image Template Matching for button image assets"
                                    value={bsc.settings.adjustment.adjustButtonSearchGeneral}
                                    onChange={(value) => bsc.setSettings({ ...bsc.settings, adjustment: { ...bsc.settings.adjustment, adjustButtonSearchGeneral: value } })}
                                    min={1}
                                    max={999}
                                    description="Set the default number of tries for overall button template matching. This will be overwritten by the specific settings down below if applicable."
                                />
                            </Grid.Col>
                            <Grid.Col span={6}>
                                <CustomNumberInput
                                    label="General Image Template Matching for header image assets"
                                    value={bsc.settings.adjustment.adjustHeaderSearchGeneral}
                                    onChange={(value) => bsc.setSettings({ ...bsc.settings, adjustment: { ...bsc.settings.adjustment, adjustHeaderSearchGeneral: value } })}
                                    min={1}
                                    max={999}
                                    description="Set the default number of tries for overall button template matching. This will be overwritten by the specific settings down below if applicable."
                                />
                            </Grid.Col>
                        </Grid>
                    ) : null}
                </Grid.Col>
            </Grid>
        )
    }

    const renderPendingBattles = () => {
        return (
            <Grid>
                <Grid.Col span={12}>
                    <Text id="pending-battles">Check for Pending Battles</Text>
                </Grid.Col>

                <Grid.Col span={12}>
                    <CustomSwitch
                        label="Enable Pending Battles Adjustments"
                        description="Enable adjustment of tries of check for Pending Battles."
                        checked={bsc.settings.adjustment.enablePendingBattleAdjustment}
                        onChange={(checked) => bsc.setSettings({ ...bsc.settings, adjustment: { ...bsc.settings.adjustment, enablePendingBattleAdjustment: checked } })}
                    />
                </Grid.Col>

                <Grid.Col span={12}></Grid.Col>
                {bsc.settings.adjustment.enablePendingBattleAdjustment ? (
                    <Grid grow sx={{ width: "100%" }}>
                        <Grid.Col span={6}>
                            <CustomNumberInput
                                label="Delay Before Starting Check"
                                value={bsc.settings.adjustment.adjustBeforePendingBattle}
                                onChange={(value) => bsc.setSettings({ ...bsc.settings, adjustment: { ...bsc.settings.adjustment, adjustBeforePendingBattle: value } })}
                                min={1}
                                max={999}
                                description="Set the default number of seconds before starting the check for Pending Battles."
                            />
                        </Grid.Col>
                        <Grid.Col span={6}>
                            <CustomNumberInput
                                label="Check for Pending Battles"
                                value={bsc.settings.adjustment.adjustPendingBattle}
                                onChange={(value) => bsc.setSettings({ ...bsc.settings, adjustment: { ...bsc.settings.adjustment, adjustPendingBattle: value } })}
                                min={1}
                                max={999}
                                description="Set the default number of tries to check for Pending Battles."
                            />
                        </Grid.Col>
                    </Grid>
                ) : null}
            </Grid>
        )
    }

    const renderCaptcha = () => {
        return (
            <Grid>
                <Grid.Col span={12}>
                    <Text id="captcha">Check for CAPTCHA</Text>
                </Grid.Col>

                <Grid.Col span={12}>
                    <CustomSwitch
                        label="Enable CAPTCHA Adjustments"
                        description="Enable adjustment of tries of check for CAPTCHA."
                        checked={bsc.settings.adjustment.enableCaptchaAdjustment}
                        onChange={(checked) => bsc.setSettings({ ...bsc.settings, adjustment: { ...bsc.settings.adjustment, enableCaptchaAdjustment: checked } })}
                    />
                </Grid.Col>

                <Grid.Col span={12}>
                    {bsc.settings.adjustment.enableCaptchaAdjustment ? (
                        <Grid grow sx={{ width: "100%" }}>
                            <Grid.Col span={6}>
                                <CustomNumberInput
                                    label="Check for CAPTCHA"
                                    value={bsc.settings.adjustment.adjustCaptcha}
                                    onChange={(value) => bsc.setSettings({ ...bsc.settings, adjustment: { ...bsc.settings.adjustment, adjustCaptcha: value } })}
                                    min={1}
                                    max={999}
                                    description="Set the default number of tries to check for CAPTCHA."
                                />
                            </Grid.Col>
                            <Grid.Col span={6} />
                        </Grid>
                    ) : null}
                </Grid.Col>
            </Grid>
        )
    }

    const renderSupportSummonSelection = () => {
        return (
            <Grid>
                <Grid.Col span={12}>
                    <Text id="support-summons">Support Summon Selection Screen</Text>
                </Grid.Col>

                <Grid.Col span={12}>
                    <CustomSwitch
                        label="Enable Summon Selection Screen Adjustments"
                        description="Enable adjustment of tries for Support Summon Selection Screen."
                        checked={bsc.settings.adjustment.enableSupportSummonSelectionScreenAdjustment}
                        onChange={(checked) => bsc.setSettings({ ...bsc.settings, adjustment: { ...bsc.settings.adjustment, enableSupportSummonSelectionScreenAdjustment: checked } })}
                    />
                </Grid.Col>

                <Grid.Col span={12}>
                    {bsc.settings.adjustment.enableSupportSummonSelectionScreenAdjustment ? (
                        <Grid grow sx={{ width: "100%" }}>
                            <Grid.Col span={6}>
                                <CustomNumberInput
                                    label="Arrival at Support Summon Selection screen"
                                    value={bsc.settings.adjustment.adjustSupportSummonSelectionScreen}
                                    onChange={(value) => bsc.setSettings({ ...bsc.settings, adjustment: { ...bsc.settings.adjustment, adjustSupportSummonSelectionScreen: value } })}
                                    min={1}
                                    max={999}
                                    description="Set the default number of tries to check if the bot arrived at the Support Summon Selection screen."
                                />
                            </Grid.Col>
                            <Grid.Col span={6} />
                        </Grid>
                    ) : null}
                </Grid.Col>
            </Grid>
        )
    }

    const renderCombatMode = () => {
        return (
            <Grid>
                <Grid.Col span={12}>
                    <Text id="combat-mode">Combat Mode</Text>
                </Grid.Col>

                <Grid.Col span={12}>
                    <CustomSwitch
                        label="Enable Combat Mode Adjustments"
                        description="Enable adjustment of tries for Combat Mode Adjustments."
                        checked={bsc.settings.adjustment.enableCombatModeAdjustment}
                        onChange={(checked) => bsc.setSettings({ ...bsc.settings, adjustment: { ...bsc.settings.adjustment, enableCombatModeAdjustment: checked } })}
                    />
                </Grid.Col>

                <Grid.Col span={12}>
                    {bsc.settings.adjustment.enableCombatModeAdjustment ? (
                        <Grid grow sx={{ width: "100%" }}>
                            <Grid.Col span={6}>
                                <CustomNumberInput
                                    label="Arrival at Combat Screen"
                                    value={bsc.settings.adjustment.adjustCombatStart}
                                    onChange={(value) => bsc.setSettings({ ...bsc.settings, adjustment: { ...bsc.settings.adjustment, adjustCombatStart: value } })}
                                    min={1}
                                    max={999}
                                    description="Set the default number of tries for checking when the bot arrives at the Combat Screen."
                                />
                            </Grid.Col>
                            <Grid.Col span={6}>
                                <CustomNumberInput
                                    label="Check for Dialog Popups"
                                    value={bsc.settings.adjustment.adjustDialog}
                                    onChange={(value) => bsc.setSettings({ ...bsc.settings, adjustment: { ...bsc.settings.adjustment, adjustDialog: value } })}
                                    min={1}
                                    max={999}
                                    description="Set the default number of tries for checking when a dialog popup from Lyria/Vyrn is present during combat."
                                />
                            </Grid.Col>
                            <Grid.Col span={6}>
                                <CustomNumberInput
                                    label="Skill Usage"
                                    value={bsc.settings.adjustment.adjustSkillUsage}
                                    onChange={(value) => bsc.setSettings({ ...bsc.settings, adjustment: { ...bsc.settings.adjustment, adjustSkillUsage: value } })}
                                    min={1}
                                    max={999}
                                    description="Set the default number of tries for checking when a skill is used."
                                />
                            </Grid.Col>
                            <Grid.Col span={6}>
                                <CustomNumberInput
                                    label="Summon Usage"
                                    value={bsc.settings.adjustment.adjustSummonUsage}
                                    onChange={(value) => bsc.setSettings({ ...bsc.settings, adjustment: { ...bsc.settings.adjustment, adjustSummonUsage: value } })}
                                    min={1}
                                    max={999}
                                    description="Set the default number of tries for checking when a Summon is used."
                                />
                            </Grid.Col>
                            <Grid.Col span={6}>
                                <CustomNumberInput
                                    label="Waiting for Reload"
                                    value={bsc.settings.adjustment.adjustWaitingForReload}
                                    onChange={(value) => bsc.setSettings({ ...bsc.settings, adjustment: { ...bsc.settings.adjustment, adjustWaitingForReload: value } })}
                                    min={1}
                                    max={999}
                                    description="Set the default number of seconds for checking when a reload is finished, whether or not the bot ends up back at the Combat screen or the Loot Collection screen."
                                />
                            </Grid.Col>
                            <Grid.Col span={6}>
                                <CustomNumberInput
                                    label="Waiting for Attack"
                                    value={bsc.settings.adjustment.adjustWaitingForAttack}
                                    onChange={(value) => bsc.setSettings({ ...bsc.settings, adjustment: { ...bsc.settings.adjustment, adjustWaitingForAttack: value } })}
                                    min={1}
                                    max={999}
                                    description="Set the default number of tries for checking when an attack is finished after the Attack button is pressed."
                                />
                            </Grid.Col>
                            <Grid.Col span={6}>
                                <CustomNumberInput
                                    label="Check for No Loot Screen"
                                    value={bsc.settings.adjustment.adjustCheckForNoLootScreen}
                                    onChange={(value) => bsc.setSettings({ ...bsc.settings, adjustment: { ...bsc.settings.adjustment, adjustCheckForNoLootScreen: value } })}
                                    min={1}
                                    max={999}
                                    description="Set the default number of tries for the frequent checking of the No Loot screen during Combat Mode. This occurs when the bot just joined a raid and takes an action but the boss died already in the process of loading into the raid. This influences when the bot gets to reload the page."
                                />
                            </Grid.Col>
                            <Grid.Col span={6}>
                                <CustomNumberInput
                                    label="Check for Battle Concluded Popup"
                                    value={bsc.settings.adjustment.adjustCheckForBattleConcludedPopup}
                                    onChange={(value) => bsc.setSettings({ ...bsc.settings, adjustment: { ...bsc.settings.adjustment, adjustCheckForBattleConcludedPopup: value } })}
                                    min={1}
                                    max={999}
                                    description="Set the default number of tries for the frequent checking of the Battle Concluded popup during Combat Mode. This occurs when the bot takes an action but the boss died at that exact moment. This influences when the bot gets to reload the page."
                                />
                            </Grid.Col>
                            <Grid.Col span={6}>
                                <CustomNumberInput
                                    label="Check for Exp Gained Popup"
                                    value={bsc.settings.adjustment.adjustCheckForExpGainedPopup}
                                    onChange={(value) => bsc.setSettings({ ...bsc.settings, adjustment: { ...bsc.settings.adjustment, adjustCheckForExpGainedPopup: value } })}
                                    min={1}
                                    max={999}
                                    description="Set the default number of tries for the frequent checking of the Exp Gained popup after Combat Mode on the Loot Collection screen. This influences when the bot gets to reload the page."
                                />
                            </Grid.Col>
                            <Grid.Col span={6}>
                                <CustomNumberInput
                                    label="Check for Loot Collection Screen"
                                    value={bsc.settings.adjustment.adjustCheckForLootCollectionScreen}
                                    onChange={(value) => bsc.setSettings({ ...bsc.settings, adjustment: { ...bsc.settings.adjustment, adjustCheckForLootCollectionScreen: value } })}
                                    min={1}
                                    max={999}
                                    description="Set the default number of tries for the frequent checking if the bot arrived at the Loot Collection screen after Combat Mode. This influences when the bot gets to reload the page."
                                />
                            </Grid.Col>
                        </Grid>
                    ) : null}
                </Grid.Col>
            </Grid>
        )
    }

    const renderArcarum = () => {
        return (
            <Grid>
                <Grid.Col span={12}>
                    <Text id="arcarum">Arcarum</Text>
                </Grid.Col>

                <Grid.Col span={12}>
                    <CustomSwitch
                        label="Enable Arcarum Adjustments"
                        description="Enable adjustment of tries for Arcarum Adjustments."
                        checked={bsc.settings.adjustment.enableArcarumAdjustment}
                        onChange={(checked) => bsc.setSettings({ ...bsc.settings, adjustment: { ...bsc.settings.adjustment, enableArcarumAdjustment: checked } })}
                    />
                </Grid.Col>

                <Grid.Col span={12}>
                    {bsc.settings.adjustment.enableArcarumAdjustment ? (
                        <Grid grow sx={{ width: "100%" }}>
                            <Grid.Col span={6}>
                                <CustomNumberInput
                                    label="Determining Which Action To Take"
                                    value={bsc.settings.adjustment.adjustArcarumAction}
                                    onChange={(value) => bsc.setSettings({ ...bsc.settings, adjustment: { ...bsc.settings.adjustment, adjustArcarumAction: value } })}
                                    min={1}
                                    max={999}
                                    description="Set the default number of tries for checking which action to take during Arcarum."
                                />
                            </Grid.Col>
                            <Grid.Col span={6}>
                                <CustomNumberInput
                                    label="Checking for Stage Effect during Combat"
                                    value={bsc.settings.adjustment.adjustArcarumStageEffect}
                                    onChange={(value) => bsc.setSettings({ ...bsc.settings, adjustment: { ...bsc.settings.adjustment, adjustArcarumStageEffect: value } })}
                                    min={1}
                                    max={999}
                                    description="Set the default number of tries for checking if there is an active stage effect popup at the start of Combat Mode."
                                />
                            </Grid.Col>
                        </Grid>
                    ) : null}
                </Grid.Col>
            </Grid>
        )
    }

    return (
        <Container className={classes.container}>
            <Stack spacing="xs">
                <Text>Adjust the default number of tries for the following situations. On average for a 8c CPU and CUDA-compatible GPU with the bot using CUDA, a try takes about 0.175 seconds.</Text>
                {renderStart()}
                <Divider my="xs" />
                {renderGeneral()}
                <Divider my="xs" />
                {renderPendingBattles()}
                <Divider my="xs" />
                {renderCaptcha()}
                <Divider my="xs" />
                {renderSupportSummonSelection()}
                <Divider my="xs" />
                {renderCombatMode()}
                <Divider my="xs" />
                {renderArcarum()}
            </Stack>
        </Container>
    )
}

export default Adjustments
