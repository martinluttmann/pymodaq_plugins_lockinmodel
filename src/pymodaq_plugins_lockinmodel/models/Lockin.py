import numpy as np
from scipy import signal

from pymodaq.extensions.data_mixer.model import DataMixerModel

from pymodaq_data.data import DataToExport, DataWithAxes, DataCalculated, DataDim
from pymodaq_gui.parameter import Parameter



class DataMixerLockin(DataMixerModel):



    params = [ {'title': 'Frequency', 'name':'liFreq', 'type':'float', 'value':500, 'suffix':'Hz', 'visible':True},
              {'title': 'Phase', 'name': 'liPhase', 'type': 'slide', 'value': 0, 'suffix': r'pi rad', 'visible': True, 'min':0, 'max':2},
              {'title': 'Integration range', 'name': 'liTime', 'type': 'slide', 'value': 100, 'suffix': '%', 'visible': True, 'min':1, 'max':100},
               {'title': 'Reference wave', 'name': 'refWave', 'type': 'list', 'limits': ['Sine', 'Square'],
                'value': 'Sine'},
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

        #trace = dte.get_data_from_name('MockSignalForLockin')[0]
        #print(dte.data[0].data)
        data1D = []
        data0D = []

        labels1D = []

        if self.settings.child('refWave').value() == 'Sine':
            reference_wave = self.sine_wave(dte.data[0].data[0], self.settings.child('liFreq').value(),
                                            self.settings.child('liPhase').value() * np.pi)
        if self.settings.child('refWave').value() == 'Square':
            reference_wave = self.square_wave(dte.data[0].data[0], self.settings.child('liFreq').value(),
                                              self.settings.child('liPhase').value() * np.pi)

        for trace in dte.data[0].data :

            Npts = np.shape(trace)[0]
            #print(Npts)


            #print(Npts)
            #time_step = 1/(self.settings.child('SamplingRate').value()*1e6)

            #time_window = self.settings.child('liTime').value()/(Npts*time_step)

            self.index_max = int(self.settings.child('liTime').value() * 0.01* Npts )



            trace_multiplied_integrated = self.multiply_with_ref_wave_and_integrate(trace, self.settings.child('liFreq').value(), self.settings.child('liPhase').value()*np.pi, self.index_max)

            data0D.append(np.atleast_1d(trace_multiplied_integrated))

            data1D.append(np.atleast_1d(trace))

        data1D.append(np.atleast_1d(reference_wave))
        new_data = DataToExport('Lockin',
                           data=[
                               DataCalculated('Traces', data=data1D,
                                              do_plot=self.settings.child('ShowTraces').value()),
                               DataCalculated('Demodulated', data=data0D)

                           ]

                           )

        return new_data


    def multiply_with_ref_wave_and_integrate(self, data, freq, phase, index_max):  #freq in acuqisition units, defined by user's sample rate

        if self.settings.child('refWave').value() == 'Sine':
            ref_wave = self.sine_wave(data, freq, phase)
        if self.settings.child('refWave').value() == 'Square':
            ref_wave = self.square_wave(data, freq, phase)

        return np.sum(np.multiply(data[:index_max], ref_wave[:index_max])) / index_max

    def sine_wave(self, data, freq, phase):
        axis = np.linspace(0, np.shape(data)[0] * 1 / (self.settings.child('SamplingRate').value()*1e6), np.shape(data)[0])
        return np.sin(2*np.pi*axis*freq + phase)

    def square_wave(self, data, freq, phase):
        axis = np.linspace(0, np.shape(data)[0] * 1 / (self.settings.child('SamplingRate').value()*1e6), np.shape(data)[0])
        return signal.square(t=2*np.pi*axis*freq + phase, duty=0.5)