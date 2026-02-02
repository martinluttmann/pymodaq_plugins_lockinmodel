from qtpy.QtCore import QThread
from qtpy import QtWidgets
from pymodaq.control_modules.viewer_utility_classes import DAQ_Viewer_base, main
import numpy as np
from easydict import EasyDict as edict
from pymodaq.utils.daq_utils import ThreadCommand, getLineInfo
from pymodaq.utils.data import DataFromPlugins, Axis, DataToExport
from pymodaq.utils.math_utils import gauss1D, linspace_step
from pymodaq.control_modules.viewer_utility_classes import comon_parameters
from pymodaq.utils.parameter.utils import iter_children
from scipy import signal

class DAQ_1DViewer_MockSignalForLockin(DAQ_Viewer_base):
    """

    """
    params = comon_parameters + [
        {'title': 'Sampling rate', 'name': 'SamplingRate', 'type': 'float', 'value': 0.1, 'default': 0.1, 'suffix': 'MHz'},
        {'title': 'Signal 1 (sine wave)', 'name': 'Mock1', 'type': 'group', 'children': [
            {'title': 'Freq', 'name': 'Freq', 'type': 'float', 'value': 600, 'default': 600, 'suffix':'Hz'},
            {'title': 'Amp', 'name': 'Amp', 'type': 'float', 'value': 0.05, 'default': 0.05},
            {'title': 'Phase', 'name': 'Phase', 'type': 'slide', 'value': 0, 'default': 0, 'suffix': 'pi rad', 'min':0, 'max':2},
            {'title': 'Amp noise:', 'name': 'AmpNoise', 'type': 'float', 'value': 20, 'default': 20},
            {'title': 'Phase noise', 'name': 'PhaseNoise', 'type': 'float', 'value': 0.12, 'default': 0.12},
        ]},

        {'title': 'Signal 2 (pulses)', 'name': 'Mock2', 'type': 'group', 'children': [
            {'title': 'Freq', 'name': 'Freq', 'type': 'float', 'value': 500, 'default': 500, 'suffix':'Hz'},
            {'title': 'Amp', 'name': 'Amp', 'type': 'float', 'value': 1, 'default': 1},
            {'title': 'Phase', 'name': 'Phase', 'type': 'slide', 'value': 0, 'default': 0, 'suffix': 'pi rad', 'min':0, 'max':2},
            {'title': 'Amp noise:', 'name': 'AmpNoise', 'type': 'float', 'value': 5, 'default': 5},
            {'title': 'Phase noise', 'name': 'PhaseNoise', 'type': 'float', 'value': 0.12, 'default': 0.12},
        ]},


        {'title': 'xaxis:', 'name': 'x_axis', 'type': 'group', 'children': [
            {'title': 'Npts:', 'name': 'Npts', 'type': 'int', 'value': 100000, },
            {'title': 'x0:', 'name': 'x0', 'type': 'float', 'value': 0, },
            {'title': 'dx:', 'name': 'dx', 'type': 'float', 'value': 1, },
        ]},
    ]
    hardware_averaging = False

    def __init__(self, parent=None,
                 params_state=None):  # init_params is a list of tuple where each tuple contains info on a 1D channel (Ntps,amplitude, width, position and noise)
        super().__init__(parent, params_state)

        self.x_axis: Axis = None
        self.ind_data = 0
        self._update_x_axis = True

    def commit_settings(self, param):
        """
            Setting the mock data

            ============== ========= =================
            **Parameters**  **Type**  **Description**
            *param*         none      not used
            ============== ========= =================

            See Also
            --------
            set_Mock_data
        """
        if param.name() in iter_children(self.settings.child('x_axis'), []):
            if param.name() == 'x0':
                self.get_spectro_wl()
            self.set_x_axis()
        else:
            self.set_Mock_data()

    def set_Mock_data(self):
        """
            For each parameter of the settings tree :
                * compute linspace numpy distribution with local parameters values
                * shift right the current data of ind_data position
                * add computed results to the data_mock list

            Returns
            -------
            list
                The computed data_mock list.
        """


        sampling_rate = self.settings.child('SamplingRate').value() * 1e6
        amp_signal1 = self.settings.child('Mock1', 'Amp').value()
        amp_signal2 = self.settings.child('Mock2', 'Amp').value()
        amp_noise1 = self.settings.child('Mock1', 'AmpNoise').value()
        amp_noise2 = self.settings.child('Mock2', 'AmpNoise').value()
        phase_noise1 = self.settings.child('Mock1', 'PhaseNoise').value()
        phase_noise2 = self.settings.child('Mock2', 'PhaseNoise').value()
        frequency1 = self.settings.child('Mock1', 'Freq').value()
        frequency2 = self.settings.child('Mock2', 'Freq').value()

        data_tot1 = amp_signal1 * np.sin(2*np.pi* self.x_axis.get_data()/sampling_rate * frequency1 + phase_noise1 * np.random.rand()) + amp_noise1 * (np.random.rand((self.x_axis.size)) - 0.5 )

        data_tot2 = amp_signal2 * signal.square(t=2*np.pi*self.x_axis.get_data()/sampling_rate*frequency2 + phase_noise2* np.random.rand(), duty=0.05) + amp_noise2 * (np.random.rand((self.x_axis.size)) - 0.5 )

        return [data_tot1, data_tot2]

    def set_x_axis(self):
        Npts = self.settings['x_axis', 'Npts']
        x0 = self.settings['x_axis', 'x0']
        dx = self.settings['x_axis', 'dx']
        self.x_axis = Axis(label='Samples', units='samples',
                           data=linspace_step(x0 - (Npts - 1) * dx / 2, x0 + (Npts - 1) * dx / 2, dx),
                           index=0)
        self._update_x_axis = True

    def ini_detector(self, controller=None):
        """
            Initialisation procedure of the detector updating the status dictionnary.

            See Also
            --------
            set_Mock_data, daq_utils.ThreadCommand
        """
        self.ini_detector_init(controller, "Mock controller")

        if self.is_master:

            self.settings.child('x_axis', 'Npts').setValue(100000)
            self.settings.child('x_axis', 'x0').setValue(0)
            self.settings.child('x_axis', 'dx').setValue(1)



            self.set_x_axis()

            # initialize viewers with the future type of data
            self.dte_signal_temp.emit(DataToExport('Mock1D',
                                                   data=[DataFromPlugins(name='Mock1', data=self.set_Mock_data(),
                                                                         dim='Data1D',
                                                                         axes=[self.x_axis],
                                                                         labels=['Signal 1', 'Signal 2']),]))

            initialized = True
            info = ''
            return info, initialized

    def close(self):
        """
            Not implemented.
        """
        pass

    def grab_data(self, Naverage=1, **kwargs):
        """
            | Start new acquisition

            For each integer step of naverage range:
                * set mock data
                * wait 100 ms
                * update the data_tot array

            | Send the data_grabed_signal once done.

            =============== ======== ===============================================
            **Parameters**  **Type**  **Description**
            *Naverage*      int       Number of spectrum to average.
                                      Specify the threshold of the mean calculation
            =============== ======== ===============================================

            See Also
            --------
            set_Mock_data
        """







        if not self._update_x_axis:
            self.dte_signal.emit(DataToExport('Mock1D',
                                              data=[DataFromPlugins(name='MockSignalForLockin', data=self.set_Mock_data())]))
        else:
            self.dte_signal.emit(DataToExport('Mock1D',
                                              data=[DataFromPlugins(name='MockSignalForLockin', data=self.set_Mock_data(),
                                                                    axes=[self.x_axis, self.x_axis], labels=['Signal 1', 'Signal 2'])]))

    def stop(self):
        """
            not implemented.
        """

        return ""


if __name__ == '__main__':
    main(__file__)