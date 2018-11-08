# DPO7254Control
Tektronix DPO7254 Oscilloscope stand-alone and DAQ-integrated control implemented for Test Beam Fermilab (November20018). 

- [Quick start](#quick-start)
  * [Installation](#installation)
  * [Required directories](#required-directories)
- [Standalone-configuration](#standalone-configuration)
  * [Output files](#output_files) 
  
  ## Quick start
 The Phyton script to run the acquisition can be found in the machine otsdaq@ftbf-daq-08. You'll need to create the python environment 
 
 - ssh otsdaq@ftbf-daq-08.FNAL.GOV   (you need to be included in the users list)
 - cd /home/otsdaq/NetScope_standalone/DPO7254COntrol
 - source /home/otsdaq/CMSTimingSetup.sh 
  
  ### Installation
  no need to install a new python version. 
  IF NOT ALREADY DONE: Need to locally install pipenv to download needed libraries.
  
  ### Required directories
  
 - Python 2.7 or newer 
 - pyvisa, pyvisa-py, numpy
 - pip install 'library'
 
 
 ## Standalone configuration
 The oscilloscope can run completely independent from the Otsdaq. The number of triggers to acquire is set as script options.
 
 IMPORTANT: the Run number is auto generated!
 
 - Triggers number =  numbr of data / # of sample
 - python dpo_fastframe.py 'totalNumber' 'numFrames' 
 
 ### Output files
 The data files generated are waveforms file in the format ".wfm". They can be recalled from the scope to be displayed. 
 The files are saved locally in a shared directory connected to the otsdaq: 
 
[otsdaq@ftbf-daq-08 Tektronix}
 
 
 
 
 
 
 