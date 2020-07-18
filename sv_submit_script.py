#submit_script.py

import vc_wrap

# make a list of sets of arguments

arglist = [{'shortname' :"SR_only",'description' : "SR active only. 24 h horizon",'DA_Active' :'no','SR_Active' : 'yes'},
{'shortname' :"NSR_only",'description':"NSR active only. 24 h horizon", 'DA_active' :'no','NSR_active' : 'yes'},
{'shortname' :"Deferral_only",'description':"Deferral active only. 24 h horizon", 'DA_active' :'no','Deferral_active' : 'yes'},
{'shortname' :"DR_only",'description':"DR active only. 24 h horizon", 'DA_active' :'no','DR_active' : 'yes'},
{'shortname' :"RA_only",'description':"RA active only. 24 h horizon. 11a to 7p", 'DA_active' :'no','RA_active' : 'yes'},
{'shortname' :"RA_only",'description':"RA active only. 24 h horizon. 2p to 9p", 'DA_active' :'no','RA_active' : 'yes', 'DR_program_start_hour'  : 14, 'DR_program_end_hour' : 21, 'DR_length' : 7},
{'shortname' :"LF_only",'description':"LF active only. 24 h horizon.", 'DA_active' :'no','LF_active' : 'yes'}]

#for testing
vc_wrap.runWithVC(**arglist[4]) 

for i in range(0,len(arglist)):
  print(i)
  vc_wrap.runWithVC(**arglist[i]) 
  
  
# arglist = [{'shortname' :"SR_only",'description' : "SR active only. 24 h horizon",
# 'DA_Active' :'no','SR_Active' : 'yes'}]
# testargs = [{'shortname':"test",'description':"testing out vc wrapper", 'PV_Active' : 'yes', 'ICE_ccost' : 2000}]
