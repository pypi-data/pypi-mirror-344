import typing as tp
from typing import ClassVar

import attrs

from NaviNIBS.Navigator.GUI.ViewPanels.NavigatePanel.NavigationView import SinglePlotterNavigationView


@attrs.define
class CobotWorkspaceAlignedView(SinglePlotterNavigationView):
    _type: ClassVar[str] = 'CobotWorkspaceAlignedView'
    _plotInSpace: str = 'World'
    _alignCameraTo: str = 'tool-CobotWorkspace-X'
    _doParallelProjection: bool = True
    _cameraDist: float = 400

    def __attrs_post_init__(self):
        super().__attrs_post_init__()

        plotLayer = 0

        self.addLayer(type='HeadMeshSurface', key='Skin', surfKey='skinSimpleSurf',
                      color='#c9c5c2',
                      layeredPlotterKey='SkinMesh',
                      plotterLayer=plotLayer)
        plotLayer += 1

        # self.addLayer(type='TargetingTargetCrosshairs', key='Target',
        #               layeredPlotterKey='Crosshairs',
        #               plotterLayer=plotLayer)
        # self.addLayer(type='TargetingCoilCrosshairs', key='Coil', layeredPlotterKey='Crosshairs')
        # plotLayer += 1

        self.addLayer(type='ToolMeshSurface', key='Workspace',
                      toolKey='CobotWorkspace',
                      opacity=0.2,
                      layeredPlotterKey='WorkspaceMesh',
                        plotterLayer=plotLayer)
        plotLayer += 1

    async def _finishInitialization_async(self):
        await super()._finishInitialization_async()

        with self._plotter.allowNonblockingCalls():
            self._plotter.enable_depth_peeling(2)