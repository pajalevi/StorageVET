# running examples, Oct 26th
SVet_Path = "/Applications/storagevet2v101/StorageVET-master-git/"
# x,y=combineRuns.nsrFn(resultsPath = SVet_Path + "Results/output_run" + str(103) +"_NSR_only/",runID=103,resHour=[0,23],regScenario=1)
# x.to_csv(SVet_Path + "Data/user_constraints/userconstraints_nsr103_rs1_0-23.csv")
# pd.DataFrame({'value':y},index=[1]).to_csv(SVet_Path + "Data/user_constraints/value_nsr103_rs1_0-23.csv")

vc.runWithVC(shortname = "nsr_sr_comparison", description = "baseline for nsr and sr runs. RA dispmode 0",
             Scenario_time_series_filename = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_2019.csv", SR_active='yes',
             NSR_active='yes',DA_active = 'yes', RA_active='yes', RA_dispmode = 0, User_active = 'no')

x,y=combineRuns.nsrFn(resultsPath = SVet_Path + "Results/output_run" + str(103) +"_NSR_only/",runID=103,resHour=[0,23],regScenario=3)
# x.to_csv(SVet_Path + "Data/user_constraints/userconstraints_nsr103_rs3_0-23.csv")
# pd.DataFrame({'value':y},index=[1]).to_csv(SVet_Path + "Data/user_constraints/value_nsr103_rs3_0-23.csv")
ID = "nsr103_RS3_0-23"
basedata = pd.read_csv(SVet_Path+"Data/hourly_timeseries_2019.csv")
basedata = basedata.set_index(x.index)
basedata['Power Min (kW)'] = x['chgMin_kW']
basedata['Power Max (kW)'] = x['chgMax_kW']
basedata['Energy Max (kWh)'] = x['eMax_kWh']
basedata['Energy Min (kWh)'] = x['eMin_kWh']
basedata.to_csv(SVet_Path + "Data/hourly_timeseries_"+ID+".csv")
f = open(SVet_Path + "Data/user_constraints/values.csv","a")
# f.write("ID,value\n")
f.write(ID + "," + str(y)+"\n")
f.close()
vc.runWithVC(shortname = "nsr_RS3_24h", description = "user constraints for nsr based on run 103 for all hours. RA dispmode 0",
             Scenario_time_series_filename = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_"+ID+".csv", SR_active='yes',
             NSR_active='no',DA_active = 'yes', RA_active='yes', RA_dispmode = 0, User_active = 'yes', User_price = y)
             # infeasible at  2017-06-09 00:00:00 hb
vc.runWithVC(shortname = "nsr_RS3_24h", description = "user constraints for nsr based on run 103 for all hours. RA dispmode 1",
             Scenario_time_series_filename = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_"+ID+".csv", SR_active='yes',
             NSR_active='no',DA_active = 'yes', RA_active='yes', RA_dispmode = 1, User_active = 'yes', User_price = y)
# infeasible at 2017-05-22 00:00:00 hb


x,y=combineRuns.nsrFn(resultsPath = SVet_Path + "Results/output_run" + str(103) +"_NSR_only/",runID=103,resHour=[14,20],regScenario=1)
# x.to_csv(SVet_Path + "Data/user_constraints/userconstraints_nsr103_rs1_14-20.csv")
# pd.DataFrame({'value':y},index=[1]).to_csv(SVet_Path + "Data/user_constraints/value_nsr103_rs1_14-20.csv")
ID = "nsr103_rs1_14-20"
basedata = pd.read_csv(SVet_Path+"Data/hourly_timeseries_2019.csv")
basedata = basedata.set_index(x.index)
basedata['Power Min (kW)'] = x['chgMin_kW']
basedata['Power Max (kW)'] = x['chgMax_kW']
basedata['Energy Max (kWh)'] = x['eMax_kWh']
basedata['Energy Min (kWh)'] = x['eMin_kWh']
basedata.to_csv(SVet_Path + "Data/hourly_timeseries_"+ID+".csv")
f = open(SVet_Path + "Data/user_constraints/values.csv","a")
# f.write("ID,value\n")
f.write(ID + "," + str(y)+"\n")
f.close()
vc.runWithVC(shortname = "nsr_RS1_14-20", description = "user constraints for nsr based on run 103 for 14h-20h. RA dispmode 0",
             Scenario_time_series_filename = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_"+ID+".csv", SR_active='yes',
             NSR_active='no',DA_active = 'yes', RA_active='yes', RA_dispmode = 0, User_active = 'yes', User_price = y)
# OH THANK GOD THIS RAN
vc.runWithVC(shortname = "nsr_RS1_14-20", description = "user constraints for nsr based on run 103 for 14h-20h. RA dispmode 1",
             Scenario_time_series_filename = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_"+ID+".csv", SR_active='yes',
             NSR_active='no',DA_active = 'yes', RA_active='yes', RA_dispmode = 1, User_active = 'yes', User_price = y)
#infeasible at 2017-07-24 00:00:00 hb


x,y=combineRuns.nsrFn(resultsPath = SVet_Path + "Results/output_run" + str(103) +"_NSR_only/",runID=103,resHour=[14,20],regScenario=3)
# x.to_csv(SVet_Path + "Data/user_constraints/userconstraints_nsr103_rs3_14-20.csv")
# pd.DataFrame({'value':y},index=[1]).to_csv(SVet_Path + "Data/user_constraints/value_nsr103_rs3_14-20.csv")
ID = "nsr103_rs3_14-20"
basedata = pd.read_csv(SVet_Path+"Data/hourly_timeseries_2019.csv")
basedata = basedata.set_index(x.index)
basedata['Power Min (kW)'] = x['chgMin_kW']
basedata['Power Max (kW)'] = x['chgMax_kW']
basedata['Energy Max (kWh)'] = x['eMax_kWh']
basedata['Energy Min (kWh)'] = x['eMin_kWh']
basedata.to_csv(SVet_Path + "Data/hourly_timeseries_"+ID+".csv")
f = open(SVet_Path + "Data/user_constraints/values.csv","a")
# f.write("ID,value\n")
f.write(ID + "," + str(y)+"\n")
f.close()
vc.runWithVC(shortname = "nsr_RS3_14-20", description = "user constraints for nsr based on run 103 for 14h-20h. RA dispmode 0",
             Scenario_time_series_filename = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_"+ID+".csv", SR_active='yes',
             NSR_active='no',DA_active = 'yes', RA_active='yes', RA_dispmode = 0, User_active = 'yes', User_price = y)
#YAY THIS RAN TOO
vc.runWithVC(shortname = "nsr_RS3_14-20", description = "user constraints for nsr based on run 103 for 14h-20h. RA dispmode 1",
             Scenario_time_series_filename = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_"+ID+".csv", SR_active='yes',
             NSR_active='no',DA_active = 'yes', RA_active='yes', RA_dispmode = 1, User_active = 'yes', User_price = y)
# infeasible at 2017-07-25 12:00:00 hb

# x,y=combineRuns.srFn(resultsPath = SVet_Path + "Results/output_run" + str(102) +"_SR_only/",runID=102,resHour=[0,23],regScenario=1)
# x.to_csv(SVet_Path + "Data/user_constraints/userconstraints_sr102_rs1_0-23.csv")
# pd.DataFrame({'value':y},index=[1]).to_csv(SVet_Path + "Data/user_constraints/value_sr102_rs1_0-23.csv")
x,y=combineRuns.srFn(resultsPath = SVet_Path + "Results/output_run" + str(102) +"_SR_only/",runID=102,resHour=[0,23],regScenario=3)
# x.to_csv(SVet_Path + "Data/user_constraints/userconstraints_sr102_rs3_0-23.csv")
# pd.DataFrame({'value':y},index=[1]).to_csv(SVet_Path + "Data/user_constraints/value_sr102_rs3_0-23.csv")
ID = "sr102_rs3_24h"
basedata = pd.read_csv(SVet_Path+"Data/hourly_timeseries_2019.csv")
basedata = basedata.set_index(x.index)
basedata['Power Min (kW)'] = x['chgMin_kW']
basedata['Power Max (kW)'] = x['chgMax_kW']
basedata['Energy Max (kWh)'] = x['eMax_kWh']
basedata['Energy Min (kWh)'] = x['eMin_kWh']
basedata.to_csv(SVet_Path + "Data/hourly_timeseries_"+ID+".csv")
f = open(SVet_Path + "Data/user_constraints/values.csv","a")
# f.write("ID,value\n")
f.write(ID + "," + str(y)+"\n")
f.close()
vc.runWithVC(shortname = ID, description = "user constraints for sr based on run 102 for 24h. RA dispmode 0",
             Scenario_time_series_filename = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_"+ID+".csv", SR_active='no',
             NSR_active='yes',DA_active = 'yes', RA_active='yes', RA_dispmode = 0, User_active = 'yes', User_price = y)
#frig this didn't run even though it ran before. Infeasible at 2017-06-09 00:00:00 hb
vc.runWithVC(shortname = ID, description = "user constraints for sr based on run 102 for 24h. RA dispmode 1",
             Scenario_time_series_filename = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_"+ID+".csv", SR_active='no',
             NSR_active='yes',DA_active = 'yes', RA_active='yes', RA_dispmode = 1, User_active = 'yes', User_price = y)
# also infeasible at 2017-07-25 12:00:00 hb
# ok this time it was infeasible at t 2017-05-22 00:00:00 hb


x,y=combineRuns.srFn(resultsPath = SVet_Path + "Results/output_run" + str(102) +"_SR_only/",runID=102,resHour=[14,20],regScenario=1)
# x.to_csv(SVet_Path + "Data/user_constraints/userconstraints_sr102_rs1_14-20.csv")
# pd.DataFrame({'value':y},index=[1]).to_csv(SVet_Path + "Data/user_constraints/value_sr102_rs1_14-20.csv")
ID = "sr102_rs1_14-20"
basedata = pd.read_csv(SVet_Path+"Data/hourly_timeseries_2019.csv")
basedata = basedata.set_index(x.index)
basedata['Power Min (kW)'] = x['chgMin_kW']
basedata['Power Max (kW)'] = x['chgMax_kW']
basedata['Energy Max (kWh)'] = x['eMax_kWh']
basedata['Energy Min (kWh)'] = x['eMin_kWh']
basedata.to_csv(SVet_Path + "Data/hourly_timeseries_"+ID+".csv")
f = open(SVet_Path + "Data/user_constraints/values.csv","a")
# f.write("ID,value\n")
f.write(ID + "," + str(y)+"\n")
f.close()
vc.runWithVC(shortname = ID, description = "user constraints for sr based on run 102 for 14-20. RA dispmode 0",
             Scenario_time_series_filename = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_"+ID+".csv", SR_active='no',
             NSR_active='yes',DA_active = 'yes', RA_active='yes', RA_dispmode = 0, User_active = 'yes', User_price = y)
#THIS RAN TOO WHOOP
vc.runWithVC(shortname = ID, description = "user constraints for sr based on run 102 for 14-20. RA dispmode 1",
             Scenario_time_series_filename = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_"+ID+".csv", SR_active='no',
             NSR_active='yes',DA_active = 'yes', RA_active='yes', RA_dispmode = 1, User_active = 'yes', User_price = y)
#infeasible at 2017-07-24 00:00:00 hb

x,y=combineRuns.srFn(resultsPath = SVet_Path + "Results/output_run" + str(102) +"_SR_only/",runID=102,resHour=[14,20],regScenario=3)
# x.to_csv(SVet_Path + "Data/user_constraints/userconstraints_sr102_rs3_14-20.csv")
# pd.DataFrame({'value':y},index=[1]).to_csv(SVet_Path + "Data/user_constraints/value_sr102_rs3_14-20.csv")
ID = "sr102_rs3_14-20"
basedata = pd.read_csv(SVet_Path+"Data/hourly_timeseries.csv")
basedata = basedata.set_index(x.index)
basedata['Power Min (kW)'] = x['chgMin_kW']
basedata['Power Max (kW)'] = x['chgMax_kW']
basedata['Energy Max (kWh)'] = x['eMax_kWh']
basedata['Energy Min (kWh)'] = x['eMin_kWh']
basedata.to_csv(SVet_Path + "Data/hourly_timeseries_"+ID+".csv")
f = open(SVet_Path + "Data/user_constraints/values.csv","a")
# f.write("ID,value\n")
f.write(ID + "," + str(y)+"\n")
f.close()
vc.runWithVC(shortname = ID, description = "user constraints for sr based on run 102 for 14-20. RA dispmode 0",
             Scenario_time_series_filename = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_"+ID+".csv", SR_active='no',
             NSR_active='yes',DA_active = 'yes', RA_active='yes', RA_dispmode = 0, User_active = 'yes', User_price = y)
#THIS RAN TOO WHOOP!
vc.runWithVC(shortname = ID, description = "user constraints for sr based on run 102 for 14-20. RA dispmode 1",
             Scenario_time_series_filename = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_"+ID+".csv", SR_active='no',
             NSR_active='yes',DA_active = 'yes', RA_active='yes', RA_dispmode = 1, User_active = 'yes', User_price = y)
             #infeasible at 2017-07-25 12:00:00 hb
