pymodaq_plugins_lockinmodel
########################

.. the following must be adapted to your developed package, links to pypi, github  description...

.. image:: https://img.shields.io/pypi/v/pymodaq_plugins_template.svg
   :target: https://pypi.org/project/pymodaq_plugins_template/
   :alt: Latest Version

.. image:: https://readthedocs.org/projects/pymodaq/badge/?version=latest
   :target: https://pymodaq.readthedocs.io/en/stable/?badge=latest
   :alt: Documentation Status

.. image:: https://github.com/PyMoDAQ/pymodaq_plugins_template/workflows/Upload%20Python%20Package/badge.svg
   :target: https://github.com/PyMoDAQ/pymodaq_plugins_template
   :alt: Publication Status

.. image:: https://github.com/PyMoDAQ/pymodaq_plugins_template/actions/workflows/Test.yml/badge.svg
    :target: https://github.com/PyMoDAQ/pymodaq_plugins_template/actions/workflows/Test.yml


Plugin containing a DataMixer model performing lockin amplification (https://en.wikipedia.org/wiki/Lock-in_amplifier) of 1D signals, as well as a 1D mock DAQ_viewer to test it !
Tutorial : https://youtu.be/8UwQzjvH1BQ



Authors
=======

* Martin Luttmann  (martin.luttmann@epfl.ch)


.. if needed use this field

    Contributors
    ============

    * First Contributor
    * Other Contributors

.. if needed use this field

  Depending on the plugin type, delete/complete the fields below


Instruments
===========

Below is the list of instruments included in this plugin



Viewer1D
++++++++

* **MockSignalForLockin**: spits out 2 noisy signals with adjustable frequency, amplitude, phase and noise level. The first signal is a sine wave, the 2nd one is a pulse train.





Models
==========
* **Lockin**: a DataMixer model performing lockin amplification.



Installation instructions
=========================

* Tested on PyMoDAQ version 5.1.7
* Tested Windows 11.
* Uses scipy.signal
