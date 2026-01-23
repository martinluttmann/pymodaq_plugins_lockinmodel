from pymodaq.extensions.data_mixer.model import DataMixerModel

from pymodaq_data.data import DataToExport, DataWithAxes, DataCalculated, DataDim
from pymodaq_gui.parameter import Parameter



class DataMixerTraining(DataMixerModel):
    params = [{'title': 'Lock-in frequency', 'name':'lifreq', 'type':'float', 'value':500, 'suffix':'Hz', 'visible':True},]
    def ini_model(self):
        pass

    def update_settings(self, param: Parameter):
        if param.name() == 'get_data':
            pass
    def process_dte(self, dte: DataToExport):


        pass
