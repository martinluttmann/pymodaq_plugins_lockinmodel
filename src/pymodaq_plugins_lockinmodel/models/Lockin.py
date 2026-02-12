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

               {'title': 'Envelope', 'name': 'Env', 'type': 'group', 'expanded': False, 'children': [
                   {'title': 'Shape', 'name': 'EnvShape', 'type': 'list', 'limits': ['Sine', 'Linear'],
                    'value': 'Sine'},
                   {'title': 'Width', 'name': 'EnvWidth', 'type': 'slide', 'value': 5, 'suffix': '%',
                    'visible': True, 'min': 0.01, 'max': 50},
                   ]},

               {'title': 'Outputs', 'name': 'Outputs', 'type': 'group', 'expanded': False, 'children': [
                   {'title': 'X', 'name': 'X', 'type': 'bool', 'value': False,
                    'visible': True},
                   {'title': 'Y', 'name': 'Y', 'type': 'bool', 'value': False,
                    'visible': True},
                   {'title': 'R', 'name': 'R', 'type': 'bool', 'value': True,
                    'visible': True},
                   {'title': 'Theta', 'name': 'Theta', 'type': 'bool', 'value': False,
                    'visible': True},
               ]}



               ]

    index_max = 100000
    def ini_model(self):
        pass

    def update_settings(self, param: Parameter):
        if param.name() == 'X':
            if param.value()==True:
                self.settings.child('Outputs', 'Y').setValue(False)
                self.settings.child('Outputs', 'R').setValue(False)
                self.settings.child('Outputs', 'Theta').setValue(False)
        if param.name() == 'Y':
            if param.value()==True:
                self.settings.child('Outputs', 'X').setValue(False)
                self.settings.child('Outputs', 'R').setValue(False)
                self.settings.child('Outputs', 'Theta').setValue(False)
        if param.name() == 'R':
            if param.value()==True:
                self.settings.child('Outputs', 'X').setValue(False)
                self.settings.child('Outputs', 'Y').setValue(False)
                self.settings.child('Outputs', 'Theta').setValue(False)
        if param.name() == 'Theta':
            if param.value()==True:
                self.settings.child('Outputs', 'X').setValue(False)
                self.settings.child('Outputs', 'Y').setValue(False)
                self.settings.child('Outputs', 'R').setValue(False)

    def process_dte(self, dte: DataToExport):

        #trace = dte.get_data_from_name('MockSignalForLockin')[0]
        #print(dte.data[0].data)
        data1D = []
        data0D = []

        labels1D = []
        labels0D = []

        if self.settings.child('refWave').value() == 'Sine':
            reference_wave = self.sine_wave(dte.data[0].data[0], self.settings.child('liFreq').value(),
                                            self.settings.child('liPhase').value() * np.pi)
        if self.settings.child('refWave').value() == 'Square':
            reference_wave = self.square_wave(dte.data[0].data[0], self.settings.child('liFreq').value(),
                                              self.settings.child('liPhase').value() * np.pi)
        i=0
        for trace in dte.data[0].data :
            i += 1
            Npts = np.shape(trace)[0]
            #print(Npts)
            labels1D.append('Signal '+str(i))

            #print(Npts)
            #time_step = 1/(self.settings.child('SamplingRate').value()*1e6)

            #time_window = self.settings.child('liTime').value()/(Npts*time_step)

            self.index_max = int(self.settings.child('liTime').value() * 0.01* Npts )

            if self.settings.child('Outputs', 'X').value() == True:
                trace_multiplied_integrated = self.multiply_with_ref_wave_and_integrate(trace, self.settings.child('liFreq').value(), self.settings.child('liPhase').value()*np.pi, self.index_max)
                labels0D.append('X'+str(i))
            if self.settings.child('Outputs', 'Y').value() == True:
                trace_multiplied_integrated = self.multiply_with_ref_wave_and_integrate(trace, self.settings.child('liFreq').value(), self.settings.child('liPhase').value()*np.pi + np.pi/2, self.index_max)
                labels0D.append('Y'+str(i))
            if self.settings.child('Outputs', 'R').value() == True:
                trace_multiplied_integrated = np.sqrt(
                    self.multiply_with_ref_wave_and_integrate(trace, self.settings.child('liFreq').value(), self.settings.child('liPhase').value()*np.pi + np.pi/2, self.index_max)**2
                    + self.multiply_with_ref_wave_and_integrate(trace, self.settings.child('liFreq').value(), self.settings.child('liPhase').value()*np.pi, self.index_max)**2 )
                labels0D.append('R'+str(i))
            if self.settings.child('Outputs', 'Theta').value() == True:
                trace_multiplied_integrated = np.arctan2(
                    self.multiply_with_ref_wave_and_integrate(trace, self.settings.child('liFreq').value(), self.settings.child('liPhase').value()*np.pi, self.index_max),
                    self.multiply_with_ref_wave_and_integrate(trace, self.settings.child('liFreq').value(),self.settings.child('liPhase').value() * np.pi + np.pi / 2, self.index_max)
                )
                labels0D.append('Theta'+str(i))

            data0D.append(np.atleast_1d(trace_multiplied_integrated))

            data1D.append(np.atleast_1d(trace))

        data1D.append(np.atleast_1d(reference_wave))

        labels1D.append('Ref')
        new_data = DataToExport('Lockin',
                           data=[
                               DataCalculated('Traces', data=data1D,
                                              do_plot=self.settings.child('ShowTraces').value(), labels=labels1D),
                               DataCalculated('Demodulated', data=data0D, labels=labels0D)

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

        wave = np.sin(2*np.pi*axis*freq + phase)

        if self.settings.child('Env', 'EnvShape').value() == 'Sine':

            width = int(self.settings.child('Env', 'EnvWidth').value()/100 * np.shape(data)[0])
            wave[:width] = np.multiply(wave[:width], self.sine_envelope_start(data[:width]))

            wave[-width:] = np.multiply(wave[-width:], self.sine_envelope_stop(data[-width:]))

        return wave

    def square_wave(self, data, freq, phase):
        axis = np.linspace(0, np.shape(data)[0] * 1 / (self.settings.child('SamplingRate').value()*1e6), np.shape(data)[0])
        wave = signal.square(t=2*np.pi*axis*freq + phase, duty=0.5)

        if self.settings.child('Env', 'EnvShape').value() == 'Sine':

            width = int(self.settings.child('Env', 'EnvWidth').value()/100 * np.shape(data)[0])
            wave[:width] = np.multiply(wave[:width], self.sine_envelope_start(data[:width]))

            wave[-width:] = np.multiply(wave[-width:], self.sine_envelope_stop(data[-width:]))

        return wave

    def sine_envelope_start(self, data):
        length = np.shape(data)[0]
        axis = np.linspace(0, length -1, length)
        return np.sin(2*np.pi*axis/(4* length))

    def sine_envelope_stop(self, data):
        length = np.shape(data)[0]
        axis = np.linspace(0, length -1, length)
        return np.cos(2*np.pi*axis/(4* length))