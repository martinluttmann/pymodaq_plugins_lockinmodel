from pymodaq.extensions.data_mixer.model import DataMixerModel

from pymodaq_data.data import DataToExport, DataWithAxes, DataCalculated, DataDim
from pymodaq_gui.parameter import Parameter
import laserbeamsize
import numpy as np

class DataMixerTraining(DataMixerModel):
    params = []
    def ini_model(self):
        pass

    def update_settings(self, param: Parameter):
        if param.name() == 'get_data':
            pass
    def process_dte(self, dte: DataToExport):


        beam = dte.get_data_from_name('BSCamera')[0]
        x, y, d_major, d_minor, phi = laserbeamsize.beam_size(beam)

        new_data = DataToExport('BeamProfiler',
                           data=[
                               DataCalculated('Beam', data=[beam], labels=['Raw beam']),
                               DataCalculated('Position', data=[np.atleast_1d(x), np.atleast_1d(y)], labels=['x', 'y']),
                               DataCalculated('Width', data=[np.atleast_1d(d_major), np.atleast_1d(d_minor)],
                                               labels=['Major axis', 'Minor axis']),
                               DataCalculated('Angle',
                                               data=[np.atleast_1d(phi)],
                                               labels=['Phi']),

                           ]

                           )

        return new_data
