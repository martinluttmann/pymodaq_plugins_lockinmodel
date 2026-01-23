import numpy as np
from pymodaq.extensions.data_mixer.model import DataMixerModel

from pymodaq_data.data import DataToExport, DataWithAxes, DataCalculated, DataDim
from pymodaq_gui.parameter import Parameter



class DataMixerTraining(DataMixerModel):
    params = [ {'title': 'Lockin prameters',
         'name': 'Liparams',
         'type': 'group', 'children':
            [
{'title': 'Frequency', 'name':'liFreq', 'type':'float', 'value':500, 'suffix':'Hz', 'visible':True},
              {'title': 'Phase', 'name': 'liPhase', 'type': 'float', 'value': 0, 'suffix': 'rad', 'visible': True},
              {'title': 'Time constant', 'name': 'liTime', 'type': 'float', 'value': 200, 'suffix': 'ms', 'visible': True},


              ] } ]
    def ini_model(self):
        pass

    def update_settings(self, param: Parameter):
        if param.name() == 'get_data':
            pass
    def process_dte(self, dte: DataToExport):
        trace = dte.get_data_from_name('MockSignalForLockin')[0]

        trace_multiplied = self.multiply_with_sine_wave(self, trace, trace.axes(), 1, 0)


        new_data = DataToExport('Lockin',
                           data=[
                               DataCalculated('multiplied', data=[trace_multiplied], labels=['Multiplied trace'])

                           ]

                           )

        return new_data


    def multiply_with_sine_wave(self, data, axis, freq, phase):

        sine_wave = np.sin(axis*freq + phase)

        return np.multiply(data, sine_wave)