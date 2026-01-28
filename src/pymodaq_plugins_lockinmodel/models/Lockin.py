import numpy as np
from scipy import signal

from pymodaq.extensions.data_mixer.model import DataMixerModel

from pymodaq_data.data import DataToExport, DataWithAxes, DataCalculated, DataDim
from pymodaq_gui.parameter import Parameter



class DataMixerTraining(DataMixerModel):



    params = [ {'title': 'Frequency', 'name':'liFreq', 'type':'float', 'value':500, 'suffix':'Hz', 'visible':True},
              {'title': 'Phase', 'name': 'liPhase', 'type': 'float', 'value': 0, 'suffix': r'pi rad', 'visible': True},
              {'title': 'Integration range', 'name': 'liTime', 'type': 'slide', 'value': 100, 'suffix': '%', 'visible': True, 'min':1, 'max':100},
            {'title': 'Sampling rate', 'name': 'SamplingRate', 'type': 'float', 'value': 0.1, 'suffix': 'MHz',
                         'visible': True},
               {'title': 'Show traces', 'name': 'ShowTraces', 'type': 'bool', 'value': False,
                'visible': True},
               ]

    index_max = 100000
    def ini_model(self):
        pass

    def update_settings(self, param: Parameter):
        if param.name() == 'get_data':
            pass
    def process_dte(self, dte: DataToExport):
        trace = dte.get_data_from_name('MockSignalForLockin')[0]





        Npts = np.shape(trace)[0]
        #print(Npts)
        #time_step = 1/(self.settings.child('SamplingRate').value()*1e6)

        #time_window = self.settings.child('liTime').value()/(Npts*time_step)

        self.index_max = int(self.settings.child('liTime').value() * 0.01* Npts )

        reference_wave = self.sine_wave(trace, self.settings.child('liFreq').value(),
                                          self.settings.child('liPhase').value() * np.pi)
        print(self.index_max)

        trace_multiplied_integrated = self.multiply_with_ref_wave_and_integrate(trace, self.settings.child('liFreq').value(), self.settings.child('liPhase').value()*np.pi, self.index_max)


        new_data = DataToExport('Lockin',
                           data=[
                               DataCalculated('Traces', data=[np.atleast_1d(trace), np.atleast_1d(reference_wave)],
                                              labels=['raw signal', 'reference wave'], do_plot=self.settings.child('ShowTraces').value()),
                               DataCalculated('multiplied', data=[np.atleast_1d(trace_multiplied_integrated)], labels=['Lockin signal'])

                           ]

                           )

        return new_data


    def multiply_with_ref_wave_and_integrate(self, data, freq, phase, index_max):  #freq in acuqisition units, defined by user's sample rate


        sine_wave = self.sine_wave(data, freq, phase)

        return np.sum(np.multiply(data[:index_max], sine_wave[:index_max])) / index_max

    def sine_wave(self, data, freq, phase):
        axis = np.linspace(0, np.shape(data)[0] * 1 / (self.settings.child('SamplingRate').value()*1e6), np.shape(data)[0])
        return np.sin(2*np.pi*axis*freq + phase)

    def square_wave(self, data, freq, phase):
        axis = np.linspace(0, np.shape(data)[0] * 1 / (self.settings.child('SamplingRate').value()*1e6), np.shape(data)[0])
        return signal.square(t=2*np.pi*axis*freq + phase, duty=0.5)