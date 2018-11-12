# Shifter quick Manual
A quick guide to acuire data with the DPO7254 Tektronix oscilloscope, convert them to .root and run the analysis.

### TO RUN THE ACQUISITION
  1. `cd /home/daq/fnal_tb_18_11/Tektronix_DPO7254Control/RunOscilloscope` 
  2. `dpo_fastframe.py --totalNumber=<int> --numFrames=<int> --trigCh = 'string' --trig = 'float'` &nbsp; *### Lunch the oscilloscope acquisition* <br />
  3. **REMEMBER TO ADD THE INFO TO THE LOG BOOK AND SPREADSHEET IF YOU CHANGE SENSORS OR SCOPE CONFIG!!!!!**
     * spreadhseet: https://docs.google.com/spreadsheets/d/1w8Xzyr6kfaaHiJRtUg55FBBeXtrGfKv6OfC9XdTYLko/edit?ts=5be4d629#gid=0
     * LogBook: https://docs.google.com/document/d/1PVd6DxdxLFYFbk_dmaxY3c2C5qMCfLAmNJD_r8xbN_4/edit#
      
      **Remember:** <br />
      * Number of files generated = # of triggers(totalNumber) / # of trigger for each file(numFrames)<br />
      * numFrames is not striclty required, set to 500 by default
      * Each trigger size is 1KB. Check the scope available disk's space from time to time.
      * the possible option for trigCh are: CH1,CH2,CH3,CH4,AUX
      * If no arguments are given the script set the default trigger to -50 mv AUX (external trigger) <br /><br />
      
      
      
      
      
      **To change the scope's configuration:** 
        ```python
      # variables for individual settings
      hScale = 10e-9  # horizontal scale in seconds, !!!!DO NOT CHANGE!!!! 
      numFrames = int(args.numFrames) # number of frames for each file
      totalNumber = int(args.totalNumber) # total number of frames

      #vertical scale
      vScale_ch1 = 0.05 # in Volts for division
      vScale_ch2 = 0.01 # in Volts for division
      vScale_ch3 = 0.01 # in Volts for division
      vScale_ch4 = 0.01 # in Volts for division

      #vertical position
      vPos_ch1 = 4  # in Divisions
      vPos_ch2 = 4  # in Divisions
      vPos_ch3 = 4  # in Divisions
      vPos_ch4 = 4  # in Divisions

      #trigger
      trigCh = (args.trigCh) # string with trigger channel number [CH1..CH4]
      trigLevel = float(args.trig)

        ```
        
        
        NOTE:<br />
        manual changes applied to the scope config will be overwitten by the script config -> If you wanna
        manually adjust the scope paprameter remeber to **comment the set up lines**. <br />
        
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
   
   
  ### In case the disks have to be mounted<br />
  1. `sudo sshfs -o allow_other YOURCERNUSERNAME@lxplus.cern.ch:/eos/cms/store/group/phys_susy/razor/FNAL_TB_1811/Scope_standalone/ /home/daq/fnal_tb_18_11/data/`
  2. `sudo su`  
  3. `kinit YOURFNALUSERNAME@FNAL.GOV`
        
        
  ### Data location and reconstruction<br />
  - The data are stored locally on the directory  **'C:\ETL_Nov2018'** in the format **run_scope{}**.<br />
  The files in the format **test_run{}** are produced by the scope development script -> do not analyze these ones <br />
  - This directory is shared to a folder in the otsdaq@ftbf-daq-08   **'/Tektronix/'** AND also in a local folder /home/daq/fnal_tb_18_11/ScopeMount/ <br />
  - The files are automatically copied to a direcotry on lxplus mounted on the otsdaq@ftbf-daq-08: **'/lxplus/Scope_standalone/RAW/'**
  
  
  ### Raw-data 2 root-tree conversion <br />
To reconstruct root files from the RAW '.wfm' files:
- cd /home/daq/fnal_tb_18_11/Tektronix_DPO7254Control/Reconstruction
- . run_conversion.sh 

* The input files are in the folder /home/daq/fnal_tb_18_11/ScopeMount/run_scope{}
* The output files are in the folder /eos/cms/store/group/phys_susy/razor/FNAL_TB_1811/Scope_standalone/ROOT/

  

