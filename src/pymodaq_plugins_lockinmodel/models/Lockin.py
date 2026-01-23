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


        new_data = DataToExport('Lockin',
                           data=[
                               DataCalculated('divided by 2', data=[trace/2], labels=['Raw beam'])

                           ]

                           )

        return new_data
