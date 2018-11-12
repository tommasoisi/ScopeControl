# Shifter quick Manual
A quick guide to acuire data with the DPO7254 Tektronix oscilloscope, convert them to .root and run the analysis.

### TO RUN THE ACQUISITION

  1. `kinit username.FNAL.GOV`
  2. `ssh otsdaq@ftbf-daq-08.FNAL.GOV`  *### you need to be included in the users list*
  3. `cd /home/otsdaq/NetScope_standalone/Tektronix_DPO7254Control/RunOscilloscope` 
  4. `source /includes/CMSTimingSetup.sh`  *#### Create the right environment for the oscilloscope control and analysis*
  5. `dpo_fastframe.py --totalNumber=<int> --numFrames=<int>` &nbsp; *### Lunch the oscilloscope acquisition* <br />
  6. **REMEMBER TO ADD THE INFO TO THE LOG BOOK AND SPREADSHEET IF YOU CHANGE SENSORS OR SCOPE CONFIG!!!!!**
     * spreadhseet: https://docs.google.com/spreadsheets/d/1w8Xzyr6kfaaHiJRtUg55FBBeXtrGfKv6OfC9XdTYLko/edit?ts=5be4d629#gid=0
     * LogBook: https://docs.google.com/document/d/1PVd6DxdxLFYFbk_dmaxY3c2C5qMCfLAmNJD_r8xbN_4/edit#
      
      **Remember:** <br />
      * Number of files generated = # of triggers(totalNumber) / # of trigger for each file(numFrames)<br />
      * numFrames is not striclty required, set to 500 by default
      * Each trigger size is 1KB. Check the scope available disk's space from time to time. <br /><br />
      
      
      
      
      **To change the scope's configuration:** 
        ```python
      # variables for individual settings
      hScale = 10e-9  # horizontal scale in seconds, !!!!DO NOT CHANGE!!!! 
      numFrames = int(args.numFrames) # number of frames for each file
      totalNumber = int(args.totalNumber) # total number of frames

      #vertical scale
      vScale_ch1 = 0.01 # in Volts
      vScale_ch2 = 0.01 # in Volts
      vScale_ch3 = 0.01 # in Volts
      vScale_ch4 = 0.01 # in Volts

      #vertical position
      vPos_ch1 = 4  # in Divisions
      vPos_ch2 = 4  # in Divisions
      vPos_ch3 = 4  # in Divisions
      vPos_ch4 = 4  # in Divisions

      #trigger
      trigCh = 'CH2' # string with trigger channel number [CH1..CH4]
      trigLevel = - 0.025
        ```
        
        
        NOTE:<br />
        manual changes applied to the scope config will be overwitten by the script config -> If you wanna
        manually adjust the scope paprameter remmeber to comment the set up lines. <br />
        
        * Example:  
        ```python
          """#################TRIGGER SETUP#################"""
          dpo.write('TRIGGER:A:TYPE EDGE;:TRIGGER:A:LEVEL {};:TRIGGER:A:EDGE:SOURCE CH2'.format(trigLevel)) 
        ```
        The Tektronix DPO7254 programmer Manual can be found at the link:  http://www.dmf.unisalento.it/~daqatlas/gas_lab/instrumentation/specification/oscilloscope/CSA7000-TDS7000GPIBGuide.pdf <br /><br />
        
        **IMPORTANT:**<br />
       * The bandwidth is automatically set to be the maximum available for each channel (2.5GHz). **This option 
        is available only if the vertical scale is set to be greater or equal to 10mV/div!!!** <br /> 
       * The Caltech analysis script work with root trees that contain a fixed (1000) number of samples! Do not change the horizontal scale (10e-9 s) if you wanna produce compatible files! 
       
        
  ### Data location and reconstruction<br />
  - The data are stored locally on the directory  **'C:\ETL_Nov2018'** in the format **run_scope{}**.<br />
  The files in the format **test_run{}** are produced by the scope development script -> do not analyze these ones <br />
  - This directory is shared to a folder in the otsdaq@ftbf-daq-08   **'/Tektronix/'**<br />
  - The files are automatically copied to a direcotry on lxplus mounted on the otsdaq@ftbf-daq-08: **'/lxplus/Scope_standalone/RAW/'**
  
  
  ### Raw-data 2 root-tree conversion <br />
To reconstruct root files from the RAW '.wfm' files:
- ssh username@lxplus.cern.ch
- cd /YOURWORKINGAREA
- git clone 
- cd /Tektronix_DPO7254Control/Reconstruction
- source ../includes/CMSTimingSetup.sh
- python conversion.py /eos/cms/store/group/phys_susy/razor/FNAL_TB_1811/Scope_standalone/RAW/run_scope{}/

* The input files are in the folder $FNAL_SCOPE_DIR (/eos/cms/store/group/phys_susy/razor/FNAL_TB_1811/Scope_standalone/RAW/run_scope{}/)
* The output files are in the folder /eos/cms/store/group/phys_susy/razor/FNAL_TB_1811/Scope_standalone/ROOT/

