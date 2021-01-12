#submit_script.py
# if needed
import sys
sys.path.append('../')
import vc_wrap as vc

# make a list of sets of arguments

# SR, NSR, RF and LF require DA or RT to also be on. What are RF and RT?
arglist = [#{'shortname' :"DA_only",'description' : "DA active only",'DA_Active' :'yes'},
{'shortname' :"SR_only",'description' : "SR active only. 2019 data",'DA_Active' :'yes','SR_Active' : 'yes'},
{'shortname' :"NSR_only",'description':"NSR active only. 2019 data", 'DA_active' :'yes','NSR_active' : 'yes'}#,
# {'shortname' :"Deferral_only",'description':"Deferral active only.", 'DA_active' :'no','Deferral_active' : 'yes'},
# {'shortname' :"DR_only",'description':"DR active only", 'DA_active' :'no','DR_active' : 'yes'},
# {'shortname' :"RA_only",'description':"RA active only. 11a to 7p", 'DA_active' :'no','RA_active' : 'yes'},
# {'shortname' :"RA_only_disp0",'description':"RA active only. 11a to 7p. dispmode 0", 'DA_active' :'no','RA_active' : 'yes','RA_dispmode':0},
# {'shortname' :"RA_only_2to9",'description':"RA active only. 2p to 9p", 'DA_active' :'no','RA_active' : 'yes', 'DR_program_start_hour'  : 14, 'DR_program_end_hour' : 21, 'DR_length' : 7},
# # {'shortname' :"LF_only",'description':"LF active only.", 'DA_active' :'yes','LF_active' : 'yes'},
# {'shortname':'All_options1','description':'DA SR NSR RA all active','DA_active':'yes','SR_active':'yes','NSR_active':'yes','RA_active':'yes'},
# {'shortname':'All_options2_mpc','description':'DA SR, NSR, DR all active with model predictive control','DA_active':'yes','SR_active':'yes','NSR_active':'yes','DR_active':'yes'}]
]
#for testing
# vc_wrap.runWithVC(**arglist[4]) 

for i in range(0,len(arglist)):
  print(i)
  vc_wrap.runWithVC(**arglist[i]) 
  
  
# arglist = [{'shortname' :"SR_only",'description' : "SR active only.",
# 'DA_Active' :'no','SR_Active' : 'yes'}]
# testargs = [{'shortname':"test",'description':"testing out vc wrapper", 'PV_Active' : 'yes', 'ICE_ccost' : 2000}]

  arglist = {'shortname' :"baseline",'description':"all active", 'DA_active' :'yes','Deferral_active' : 'yes'}
  vc_wrap.runWithVC(**arglist)

  arglist = {'shortname' :"Deferral_only",'description':"Deferral active only.", 'DA_active' :'no','Deferral_active' : 'yes'}
  vc_wrap.runWithVC(**arglist)

vc.runWithVC(shortname = "sr_RS1_14-20", description = "user constraints for sr based on run 108 for 14h-20h. DR not day ahead ie dispmode 1",
Scenario_time_series_filename = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_sr_RS1_14-20.csv", SR_active='no',
NSR_active='yes',DA_active = 'yes', DR_active='yes', DR_day_ahead = 0, User_active = 'yes', User_price = 69530.71064)

vc.runWithVC(shortname = "comparison_sr_RS1_14-20", description = "no user constraints. all else same. DR not day ahead ie dispmode 1",
Scenario_time_series_filename = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_sr_RS1_14-20.csv", SR_active='yes',
NSR_active='yes',DA_active = 'yes', DR_active='yes', DR_day_ahead = 0, User_active = 'no')

vc.runWithVC(shortname = "sr_RS1_14-20", description = "user constraints for sr based on run 108 for 14h-20h. RA dispmode 0",
Scenario_time_series_filename = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_sr_RS1_14-20.csv", SR_active='no',
NSR_active='yes',DA_active = 'yes', RA_active='yes', RA_dispmode = 0, User_active = 'yes', User_price = 69530.71064)

vc.runWithVC(shortname = "comparison_sr_RS1_14-20", description = "no user constraints. all else same. RA dispmode 0",
Scenario_time_series_filename = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_sr_RS1_14-20.csv", SR_active='yes',
NSR_active='yes',DA_active = 'yes', RA_active='yes', RA_dispmode = 0, User_active = 'no')



vc.runWithVC(shortname = "test_dervet", description = "testing dervet's version of svet",
Scenario_time_series_filename = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_v2.csv", SR_active='yes',
NSR_active='yes',DA_active = 'yes', RA_active='yes', RA_dispmode = 0, User_active = 'no')

vc.runWithVC(shortname = "test_dervet", description = "testing dervet's version of svet with deferral",
Scenario_time_series_filename = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_v2.csv", SR_active='yes',
NSR_active='yes',DA_active = 'yes', RA_active='yes', RA_dispmode = 0, User_active = 'no', Deferral_active='yes')

  
