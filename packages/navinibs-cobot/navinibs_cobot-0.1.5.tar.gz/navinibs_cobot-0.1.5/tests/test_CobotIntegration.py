
import asyncio
import jsbeautifier
import json
import logging
import numpy as np
import os
import pyperclip
import pytest
import pytransform3d.transformations as ptt
import pytransform3d.rotations as ptr
from qtpy import QtCore
import random
import shutil

from NaviNIBS.Navigator.GUI.NavigatorGUI import NavigatorGUI
from NaviNIBS.util.Transforms import applyTransform, invertTransform, composeTransform, concatenateTransforms
from NaviNIBS.util.numpy import array_equalish
from tests.test_NavigatorGUI import utils
from tests.test_NavigatorGUI.utils import (
    existingResourcesDataPath,
    navigatorGUIWithoutSession,
    workingDir,
    screenshotsDataSourcePath)

from NaviNIBS_Cobot.Devices.CobotConnector import (
    TargetingState,
    ContactMode,
    TargetChangeRetractMode,
    TargetChangeContactMode,
)
from NaviNIBS_Cobot.Navigator.GUI.ViewPanels.CobotWidgets import (
    CobotMoveToParkControlEntry,
    CobotMoveToWelcomeControlEntry,
    CobotTrackTargetControlEntry,
    CobotContactControlEntry
)


logger = logging.getLogger(__name__)


@pytest.fixture
def simulatedCobotAddr():
    return '127.0.0.1'


@pytest.fixture
def cobotToolsDataSourcePath(existingResourcesDataPath):
    return os.path.join(os.path.dirname(__file__), '..', 'Devices', 'resources', 'CobotTools.json')


@pytest.fixture
def simulatedCobotPositionsPath(existingResourcesDataPath):
    return os.path.join(existingResourcesDataPath, 'testSourceData',
                        'SimulatedPositions_Cobot.json')


@pytest.mark.asyncio
@pytest.mark.order(after='tests/test_NavigatorGUI/test_NavigatorGUI.py::test_basicNavigation')
async def test_enableCobotAddon(navigatorGUIWithoutSession: NavigatorGUI,
                                workingDir: str,
                                screenshotsDataSourcePath: str,
                                simulatedCobotAddr: str,
                                cobotToolsDataSourcePath: str):
    navigatorGUI = navigatorGUIWithoutSession

    sessionPath = utils.copySessionFolder(workingDir, 'BasicNavigation', 'CobotSetup')

    if False:
        # set up addon via GUI
        # (disabled for now since there is no GUI support for editing IP address or changing after startup)

        # open session
        navigatorGUI.manageSessionPanel.loadSession(sesFilepath=sessionPath)

        await asyncio.sleep(5.)  # give time to restore any previous simulated positions  (TODO: handle this differently to speed up test)

        # open manage session panel
        navigatorGUI._activateView(navigatorGUI.manageSessionPanel.key)

        await asyncio.sleep(1.)

        # add addon

        from NaviNIBS.Navigator.Model.Addons import installPath as addonBaseInstallPath

        addonConfigPath = os.path.join(addonBaseInstallPath, '..', 'addons', 'NaviNIBS_Cobot', 'addon_configuration.json')

        navigatorGUI.manageSessionPanel._addAddon(addonConfigPath)

        await asyncio.sleep(5.)

        await utils.captureAndCompareScreenshot(navigatorGUI=navigatorGUI,
                                                sessionPath=sessionPath,
                                                screenshotName='CobotSetup_AddonAdded',
                                                screenshotsDataSourcePath=screenshotsDataSourcePath)

        await utils.waitForever()  # TODO: debug, delete
        raise NotImplementedError  # TODO: edit IP address if needed

        # equivalent to clicking save button
        navigatorGUI.manageSessionPanel._onSaveSessionBtnClicked(checked=False)

        ses = utils.assertSavedSessionIsValid(sessionPath)

    else:
        # add to saved session config before loading session
        addonConfig = dict()
        addonConfig['addonInstallPath'] = '../addons/NaviNIBS_Cobot/'
        cobotConfig = dict()
        cobotConfig['cobotAddr'] = simulatedCobotAddr
        cobotConfig['cobotIsSimulated'] = True
        addonConfig['cobotControl'] = cobotConfig
        addonConfigName = 'SessionConfig_Addon_NaviNIBS_Cobot.json'
        addonConfigPath = os.path.join(sessionPath, addonConfigName)
        with open(addonConfigPath, 'w') as f:
            json.dump(addonConfig, f)

        baseConfigPath = os.path.join(sessionPath, 'SessionConfig.json')
        with open(baseConfigPath, 'r+') as f:
            baseConfig = json.load(f)
            if 'addons' not in baseConfig:
                baseConfig['addons'] = []
            baseConfig['addons'].append(addonConfigName)

            del baseConfig['dockWidgetLayouts']  # remove previous saved layouts since they don't include view pane for new addon

            opts = jsbeautifier.default_options()
            opts.indent_size = 2
            beautifier = jsbeautifier.Beautifier(opts)
            f.seek(0)
            f.write(beautifier.beautify(json.dumps(baseConfig)))
            f.truncate()

        # open session
        navigatorGUI.manageSessionPanel.loadSession(sesFilepath=sessionPath)

        await asyncio.sleep(5.)

        # resize window to smaller size so that screenshots are more readable when used in documentation
        navigatorGUIWithoutSession._win.resize(QtCore.QSize(1400, 800))

        # open manage session panel
        navigatorGUI._activateView(navigatorGUI.manageSessionPanel.key)

        await asyncio.sleep(1.)

        await utils.captureAndCompareScreenshot(navigatorGUI=navigatorGUI,
                                                sessionPath=sessionPath,
                                                screenshotName='CobotSetup_AddonAdded',
                                                screenshotsDataSourcePath=screenshotsDataSourcePath)

    from addons.NaviNIBS_Cobot.Navigator.GUI.ViewPanels.CobotDebugPanel import CobotDebugPanel

    # equivalent to clicking on tab
    cobotControlPanel: CobotDebugPanel = navigatorGUI._mainViewPanels['CobotDebugPanel']
    navigatorGUI._activateView(cobotControlPanel.key)

    await asyncio.sleep(1.)

    await utils.captureAndCompareScreenshot(navigatorGUI=navigatorGUI,
                                            sessionPath=sessionPath,
                                            screenshotName='CobotSetup_ControlPanel',
                                            screenshotsDataSourcePath=screenshotsDataSourcePath)

    # make sure that Cobot connected
    assert cobotControlPanel._controller.cobotClient.isConnectedToServer
    assert cobotControlPanel._controller.cobotClient.isConnected

    # equivalent to clicking save button
    navigatorGUI.manageSessionPanel._onSaveSessionBtnClicked(checked=False)

    ses = utils.assertSavedSessionIsValid(sessionPath)

    # import Cobot tools
    navigatorGUI._activateView(navigatorGUI.toolsPanel.key)
    navigatorGUI.toolsPanel._importToolsFromFile(cobotToolsDataSourcePath)

    await asyncio.sleep(1.)

    # equivalent to clicking on corresponding entry in table
    navigatorGUI.toolsPanel._tblWdgt.currentCollectionItemKey = 'CobotCart'

    await navigatorGUI.toolsPanel._toolWdgt.finishedAsyncInit.wait()

    # deactivate previous primary coil tool and calibration plate
    navigatorGUI.session.tools['Coil1'].isActive = False
    navigatorGUI.session.tools['CB60Calibration'].isActive = False

    await asyncio.sleep(2.)

    await utils.captureAndCompareScreenshot(navigatorGUI=navigatorGUI,
                                            sessionPath=sessionPath,
                                            screenshotName='CobotSetup_Tools',
                                            screenshotsDataSourcePath=screenshotsDataSourcePath)

    # equivalent to clicking save button
    navigatorGUI.manageSessionPanel._onSaveSessionBtnClicked(checked=False)

    ses = utils.assertSavedSessionIsValid(sessionPath)


@pytest.mark.asyncio
@pytest.mark.order(after='test_enableCobotAddon')
async def test_cobotNavigation(navigatorGUIWithoutSession: NavigatorGUI,
                                workingDir: str,
                                screenshotsDataSourcePath: str,
                               simulatedCobotPositionsPath: str,
                               ):
    navigatorGUI = navigatorGUIWithoutSession

    sessionPath = utils.copySessionFolder(workingDir, 'CobotSetup', 'CobotNavigation')

    # open session
    navigatorGUI.manageSessionPanel.loadSession(sesFilepath=sessionPath)

    await asyncio.sleep(5.)

    from addons.NaviNIBS_Cobot.Navigator.GUI.ViewPanels.NavigatePanelWithCobot import NavigatePanelWithCobot

    # equivalent to clicking on tab
    cobotNavPanel: NavigatePanelWithCobot = navigatorGUI._mainViewPanels['NavigateWithCobot']
    navigatorGUI._activateView(cobotNavPanel.key)

    await asyncio.sleep(15.)

    # should have auto-connected and initialized, and watchdog should not have triggered back to non-idle state
    assert cobotNavPanel._controller.cobotClient.state == TargetingState.IDLE

    # equivalent to dragging camera panel to left of main dock and resizing
    navigatorGUI._rootDockArea.moveDock(navigatorGUI.cameraPanel.dockWdgt,
                                        'left', cobotNavPanel.dockWdgt)

    navigatorGUI.cameraPanel.dockWdgt.setStretch(x=3, y=10)

    # resize window to smaller size so that screenshots are more readable when used in documentation
    navigatorGUIWithoutSession._win.resize(QtCore.QSize(1600, 900))

    await asyncio.sleep(15.)

    # await utils.captureAndCompareScreenshot(navigatorGUI=navigatorGUI,
    #                                         sessionPath=sessionPath,
    #                                         screenshotName='CobotNav_NoToolPoses',
    #                                         screenshotsDataSourcePath=screenshotsDataSourcePath)

    # should have auto-connected and initialized, and watchdog should not have triggered back to non-idle state
    assert cobotNavPanel._controller.cobotClient.state == TargetingState.IDLE

    # set tool positions
    from addons.NaviNIBS_Simulated_Tools.Navigator.GUI.ViewPanels.SimulatedToolsPanel import SimulatedToolsPanel
    simulatedToolsPanel: SimulatedToolsPanel = navigatorGUI._mainViewPanels['SimulatedToolsPanel']
    await simulatedToolsPanel.importPositionsSnapshot(simulatedCobotPositionsPath)

    # move to park position
    ctrl = cobotNavPanel._cobotControlWdgt._basicControlsWdgt._entries['moveToPark']
    assert isinstance(ctrl, CobotMoveToParkControlEntry)
    ctrl._wdgt.click()

    await asyncio.sleep(5.)

    navigatorGUI.cameraPanel._mainCameraView._autoOrientCamera(distance=2000)  # reorient to new head position

    await asyncio.sleep(1.)

    # check force sensor
    assert cobotNavPanel._controller.needsForceCheck

    cobotNavPanel._cobotControlWdgt._contactControlsWdgt._startForceCheck()

    await asyncio.sleep(1.)

    await utils.captureAndCompareScreenshot(navigatorGUI=navigatorGUI,
                                            sessionPath=sessionPath,
                                            screenshotName='CobotNav_ForceCheckStart',
                                            screenshotsDataSourcePath=screenshotsDataSourcePath)

    await cobotNavPanel._cobotControlWdgt._contactControlsWdgt._checkForceDlg._simulateCheck()

    await asyncio.sleep(1.)

    await utils.captureAndCompareScreenshot(navigatorGUI=navigatorGUI,
                                            sessionPath=sessionPath,
                                            screenshotName='CobotNav_ForceCheckDone',
                                            screenshotsDataSourcePath=screenshotsDataSourcePath)

    cobotNavPanel._cobotControlWdgt._contactControlsWdgt._checkForceDlg._wdgt.accept()

    await asyncio.sleep(1.)

    assert not cobotNavPanel._controller.needsForceCheck

    # equivalent to clicking save button
    navigatorGUI.manageSessionPanel._onSaveSessionBtnClicked(checked=False)

    ses = utils.assertSavedSessionIsValid(sessionPath)

    # equivalent to clicking on first target
    cobotNavPanel._targetsTableWdgt.currentCollectionItemKey = list(navigatorGUI.session.targets.keys())[0]

    await asyncio.sleep(5.)

    await utils.captureAndCompareScreenshot(navigatorGUI=navigatorGUI,
                                            sessionPath=sessionPath,
                                            screenshotName='CobotNav_Park',
                                            screenshotsDataSourcePath=screenshotsDataSourcePath)

    # move to welcome 1 position and screenshot
    ctrl = cobotNavPanel._cobotControlWdgt._basicControlsWdgt._entries['moveToWelcome']
    assert isinstance(ctrl, CobotMoveToWelcomeControlEntry)
    ctrl._wdgt.click()

    await asyncio.sleep(5.)

    await utils.captureAndCompareScreenshot(navigatorGUI=navigatorGUI,
                                            sessionPath=sessionPath,
                                            screenshotName='CobotNav_Welcome1',
                                            screenshotsDataSourcePath=screenshotsDataSourcePath)

    # align to target and screenshot
    ctrl = cobotNavPanel._cobotControlWdgt._trackingControlsWdgt._entries['track']
    assert isinstance(ctrl, CobotTrackTargetControlEntry)
    ctrl._wdgt.click()
    ctrl_track = ctrl

    await asyncio.sleep(5.)
    assert cobotNavPanel._controller.cobotClient.state == TargetingState.ALIGNED_RETRACTED

    await utils.captureAndCompareScreenshot(navigatorGUI=navigatorGUI,
                                            sessionPath=sessionPath,
                                            screenshotName='CobotNav_Aligned',
                                            screenshotsDataSourcePath=screenshotsDataSourcePath)

    # contact target and screenshot
    ctrl = cobotNavPanel._cobotControlWdgt._contactControlsWdgt._entries['contact']
    assert isinstance(ctrl, CobotContactControlEntry)
    ctrl._wdgt.click()
    ctrl_contact = ctrl

    await asyncio.sleep(10.)
    assert cobotNavPanel._controller.cobotClient.state == TargetingState.ALIGNED_CONTACTING

    await utils.captureAndCompareScreenshot(navigatorGUI=navigatorGUI,
                                            sessionPath=sessionPath,
                                            screenshotName='CobotNav_Contact',
                                            screenshotsDataSourcePath=screenshotsDataSourcePath)

    # TODO: retract from target and screenshot
    ctrl_contact._wdgt.click()
    await asyncio.sleep(5.)

    # TODO: stop aligning from target and screenshot
    ctrl_track._wdgt.click()
    await asyncio.sleep(5.)



@pytest.mark.asyncio
# @pytest.mark.skip(reason='For troubleshooting')
async def test_openCobotNavSession(workingDir):
    await utils.openSessionForInteraction(workingDir, 'CobotNavigation')



