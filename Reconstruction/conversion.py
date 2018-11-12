import time
#import matplotlib.pyplot as plt # https://matplotlib.org/
import numpy as np # http://www.numpy.org/
import tekwfm
import os,sys
import ctypes

from ROOT import TFile, TTree
from array import array

if len(sys.argv)==3:
    path = sys.argv[1]
    outputfile = sys.argv[2]

if len(sys.argv)==2:
    path = sys.argv[1]
    runName = path.split('/')[-1].strip('/')
    if runName=='':
        runName = path.split('/')[-2].strip('/')
    # print(runName)
    outputfile = path + '/../../ROOT/%s.root'%(runName)
    print("Using default output: %s"%(outputfile))

if len(sys.argv)<2 or len(sys.argv)>3:
    raise Exception("Usage: python converter.py inputDir [outputFile]")

f = TFile( outputfile, 'recreate' )
t = TTree( 'pulse', 'Test beam samples' )

i_evt = np.zeros(1,dtype=np.dtype("u4"))
channel = np.zeros([4,1000],dtype=np.float32)
time = np.zeros([1,1000],dtype=np.float32)
baseline = np.zeros([4])
baseline_RMS = np.zeros([4])
amp = np.zeros([4])
t_peak = np.zeros([4])
integral = np.zeros([4])
intfull = np.zeros([4])
risetime = np.zeros([4])
decaytime = np.zeros([4])
fallingtime = np.zeros([4])
gaus_mean = np.zeros([4])
gaus_sigma = np.zeros([4])
gaus_chi2 = np.zeros([4])
LP1_10 = np.zeros([4])
LP1_20 = np.zeros([4])
LP1_30 = np.zeros([4])
LP2_10 = np.zeros([4])
LP2_20 = np.zeros([4])
LP2_30 = np.zeros([4])

t.Branch( 'i_evt', i_evt, 'i_evt/i' )
t.Branch( 'channel', channel, 'channel[4][1000]/F' )
t.Branch( 'time', time, 'time[1][1000]/F')
#t.Branch( 'baseline', baseline, 'baseline[4]/F')
#t.Branch( 'baseline_RMS', baseline_RMS,'baseline_RMS[4]/F')
#t.Branch( 'amp', amp, 'amp[4]/F')
#t.Branch( 't_peak', t_peak, 't_peak[4]/F')
#t.Branch( 'integral', integral, 'integral[4]/F')
#t.Branch( 'intfull', intfull, 'intfull[4]/F')
#t.Branch( 'risetime', risetime, 'risetime[4]/F')
#t.Branch( 'decaytime', decaytime, 'decaytime[4]/F')
#t.Branch( 'gaus_mean', gaus_mean, 'gaus_mean[4]/F')
#t.Branch( 'gaus_sigma', gaus_sigma, 'gaus_sigma[4]/F')
#t.Branch( 'gaus_chi2', gaus_chi2, 'gaus_chi2[4]/F')
#t.Branch( 'LP1_10', LP1_10, 'LP1_10[4]/F')
#t.Branch( 'LP1_20', LP1_20, 'LP1_20[4]/F')
#t.Branch( 'LP1_30', LP1_30, 'LP1_30[4]/F')
#t.Branch( 'LP2_10', LP1_10, 'LP1_10[4]/F')
#t.Branch( 'LP2_20', LP1_20, 'LP1_20[4]/F')
#t.Branch( 'LP2_30', LP1_30, 'LP1_30[4]/F')

def openfiles(path):
    dirs = os.listdir(path)
    ch_set = set()
    run_set = []
    prerun_name = ""
    for file in dirs:
        file_split = file.split('_')
        # print file_split
        run_num_str = file_split[len(file_split)-2]
        run_num = int(file_split[len(file_split)-2])
        if run_num < 0:
            print >> sys.stderr, "error: invalid run number"
        run_set.append(run_num_str)
        #file_split[len(file_split)-1]
        chan_num = int(file_split[len(file_split)-1][2])
        ch_set.update(file_split[len(file_split)-1][2])
        i = 0
        prerun_name = path + '/'
        for i in range(len(file_split)-2):
            prerun_name+= file_split[i] + '_'
    return len(ch_set), len(run_set), prerun_name
    max(run_num)

numbChannels, numbFiles, fname = openfiles(path)
print(numbFiles)
print(fname)
if numbChannels != 4:
    raise Exception("Problem with the number of channels")

for fnum in range(1,numbFiles/numbChannels +1):
    try:
        print("I'm reading: %s%i_CH1.wfm"%(fname,fnum))
        volts_ch1, tstart_ch1, tscale_ch1, tfrac_ch1, tdatefrac_ch1, tdate_ch1 = tekwfm.read_wfm("%s%i_CH1.wfm"%(fname,fnum))
        print("I'm reading: %s%i_CH2.wfm"%(fname,fnum))
        volts_ch2, tstart_ch2, tscale_ch2, tfrac_ch2, tdatefrac_ch2, tdate_ch2 = tekwfm.read_wfm("%s%i_CH2.wfm"%(fname,fnum))
        print("I'm reading: %s%i_CH3.wfm"%(fname,fnum))
        volts_ch3, tstart_ch3, tscale_ch3, tfrac_ch3, tdatefrac_ch3, tdate_ch3 = tekwfm.read_wfm("%s%i_CH3.wfm"%(fname,fnum))
        print("I'm reading: %s%i_CH4.wfm"%(fname,fnum))
        volts_ch4, tstart_ch4, tscale_ch4, tfrac_ch4, tdatefrac_ch4, tdate_ch4 = tekwfm.read_wfm("%s%i_CH4.wfm"%(fname,fnum))
    except:
        print("Skipping....")
    else:
        if tfrac_ch1.all() != tfrac_ch2.all() and tfrac_ch1.all() != tfrac_ch3.all() and tfrac_ch1.all() != tfrac_ch4.all():
            raise Exception("times don't match between channels!")
        if tscale_ch1 != tscale_ch2 and tscale_ch1 != tscale_ch3 and tscale_ch1 != tscale_ch4:
            raise Exception("time scales don't match between channels!")

        print("I'm filling the tree: %s"%(outputfile))
        samples = 1000
        tstop_ch1 = samples * tscale_ch1 + tstart_ch1
        t0 = np.linspace(tstart_ch1, tstop_ch1, num=samples, endpoint=False)

        evt_offset = len(tfrac_ch1)*(fnum-1)
        time_temp = np.zeros(volts_ch1.shape)
        for frame, subsample in enumerate(tfrac_ch1):
            toff = subsample * tscale_ch1
            time_temp[:samples,frame] = t0 + toff

        for evt_local in range(len(tfrac_ch1)):
            i_evt[0] = evt_local + evt_offset
            # print(i_evt[0])

            channel[0] = volts_ch1[:samples,evt_local]
            channel[1] = volts_ch2[:samples,evt_local]
            channel[2] = volts_ch3[:samples,evt_local]
            channel[3] = volts_ch4[:samples,evt_local]
            time[0] = time_temp[:samples,evt_local]

            t.Fill()


f.Write()
f.Close()
