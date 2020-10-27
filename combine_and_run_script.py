# running examples, Oct 26th
SVet_Path = "/Applications/storagevet2v101/StorageVET-master-git/"
# x,y=combineRuns.nsrFn(resultsPath = SVet_Path + "Results/output_run" + str(103) +"_NSR_only/",runID=103,resHour=[0,23],regScenario=1)
# x.to_csv(SVet_Path + "Data/user_constraints/userconstraints_nsr103_rs1_0-23.csv")
# pd.DataFrame({'value':y},index=[1]).to_csv(SVet_Path + "Data/user_constraints/value_nsr103_rs1_0-23.csv")


x,y=combineRuns.nsrFn(resultsPath = SVet_Path + "Results/output_run" + str(103) +"_NSR_only/",runID=103,resHour=[0,23],regScenario=3)
# x.to_csv(SVet_Path + "Data/user_constraints/userconstraints_nsr103_rs3_0-23.csv")
# pd.DataFrame({'value':y},index=[1]).to_csv(SVet_Path + "Data/user_constraints/value_nsr103_rs3_0-23.csv")
ID = "nsr103_rs3_0-23"
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
vc.runWithVC(shortname = "sr_RS1_14-20", description = "user constraints for nsr based on run 103 for 14h-20h. RA dispmode 0",
             Scenario_time_series_filename = "/Applications/storagevet2v101/StorageVET-master-git/Data/hourly_timeseries_"+ID+".csv", SR_active='no',
             NSR_active='yes',DA_active = 'yes', RA_active='yes', RA_dispmode = 0, User_active = 'yes', User_price = y)


x,y=combineRuns.nsrFn(resultsPath = SVet_Path + "Results/output_run" + str(103) +"_NSR_only/",runID=103,resHour=[14,20],regScenario=1)
# x.to_csv(SVet_Path + "Data/user_constraints/userconstraints_nsr103_rs1_14-20.csv")
# pd.DataFrame({'value':y},index=[1]).to_csv(SVet_Path + "Data/user_constraints/value_nsr103_rs1_14-20.csv")

x,y=combineRuns.nsrFn(resultsPath = SVet_Path + "Results/output_run" + str(103) +"_NSR_only/",runID=103,resHour=[14,20],regScenario=3)
# x.to_csv(SVet_Path + "Data/user_constraints/userconstraints_nsr103_rs3_14-20.csv")
# pd.DataFrame({'value':y},index=[1]).to_csv(SVet_Path + "Data/user_constraints/value_nsr103_rs3_14-20.csv")


# x,y=combineRuns.srFn(resultsPath = SVet_Path + "Results/output_run" + str(102) +"_NSR_only/",runID=102,resHour=[0,23],regScenario=1)
# x.to_csv(SVet_Path + "Data/user_constraints/userconstraints_sr102_rs1_0-23.csv")
# pd.DataFrame({'value':y},index=[1]).to_csv(SVet_Path + "Data/user_constraints/value_sr102_rs1_0-23.csv")
x,y=combineRuns.srFn(resultsPath = SVet_Path + "Results/output_run" + str(102) +"_NSR_only/",runID=102,resHour=[0,23],regScenario=3)
x.to_csv(SVet_Path + "Data/user_constraints/userconstraints_sr102_rs3_0-23.csv")
pd.DataFrame({'value':y},index=[1]).to_csv(SVet_Path + "Data/user_constraints/value_sr102_rs3_0-23.csv")
x,y=combineRuns.srFn(resultsPath = SVet_Path + "Results/output_run" + str(102) +"_NSR_only/",runID=102,resHour=[14,20],regScenario=1)
x.to_csv(SVet_Path + "Data/user_constraints/userconstraints_sr102_rs1_14-20.csv")
pd.DataFrame({'value':y},index=[1]).to_csv(SVet_Path + "Data/user_constraints/value_sr102_rs1_14-20.csv")
x,y=combineRuns.srFn(resultsPath = SVet_Path + "Results/output_run" + str(102) +"_NSR_only/",runID=102,resHour=[14,20],regScenario=3)
x.to_csv(SVet_Path + "Data/user_constraints/userconstraints_sr102_rs3_14-20.csv")
pd.DataFrame({'value':y},index=[1]).to_csv(SVet_Path + "Data/user_constraints/value_sr102_rs3_14-20.csv")
