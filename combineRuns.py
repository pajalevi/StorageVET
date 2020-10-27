"""
combineRuns.py

This function generates the inputs for a run that combines
constraints from multiple runs according to the given inputs.
It then runs StorageVET.

Patricia Levi July 2020
"""

import pandas as pd
import os
import vc_wrap as vc
# import subprocess
# import shlex
# import datetime
# import sys

SVet_Path = "/Applications/storagevet2v101/StorageVET-master-git/"
default_params_file = "Model_Parameters_2v1-0-2_default.csv"
runs_log_file = "Results/runsLog.csv"


def combineRuns(runIDs, resTypes, resHours, regScenario,
SVet_Path = SVet_Path, default_params_file = default_params_file, runs_log_file = runs_log_file, test = False):
  """This function takes as input the type of regulatory scenario desired and three
  pieces of information regarding each run used to make the combined run: the run number,
  the resource type {“NSR”,”SR”,”RA1”,”RA0”,”DR1”,”DR0”…} and the hours in which a resource
  is given priority (e.g. [[6,16], [16,23]]), which may not overlap. It uses this information
  to run StorageVET with the desired combination of storage value stacking"""

  # check that runIDs, resTypes, and resHours are the same length

  # check for overlap in resHours & that each element has length 2

  # create empty matrix of user constraints
  # create placeholder for value

  # for each resource...
  for i in range(len(runIDs)):

    # ID folder:
    # read in runs log file
    runsLog = pd.read_csv(SVet_Path + runs_log_file)
    runsfilter = runsLog['runID']==runIDs[i]
    shortname = runsLog.loc[runsLog['runID'] == runIDs[i]]['shortname'].values[0]
    # id row with runID
    # id shortname

    # call appropriate read-in fn for that resource
    resultsPath = SVet_Path + "Results/output_run" + str(runIDs[i]) + "_" + shortname + "/"#"timeseries_results_runID" + str(runIDs[i]) + ".csv"

    resType_to_fn(resTypes[i],resultsPath,resHours[i], regScenario)

    # add outputs to user constraint matrix
    # select for most binding user constraints
    # add value to value placeholder

  # write new hourly_timseries input file

  # git commit if NOT test

  # run svet via vc_wrap


# function resource does the following
# read in timeseries of dispatch
# identify appropriate columns
# subset for desired hours
# translate output to appropriate limits
# also calculate value of that service

def resType_to_fn(resType,resultsPath,resHour,regScenario):
  switch_case = {
    "NSR": nsrFn,
    "SR": srFn
  }
  func = switch_case.get(resType) #get returns the value of the item associated with key
  func(resultsPath,resHour,regScenario) #TODO: define inputs
#end resType_to_fn


runID = 103
regScenario = 1
resHour = [14,20]
resultsPath = SVet_Path + "Results/output_run" + str(runID) + "_NSR_only/"#"timeseries_results_runID" + str(runID) + ".csv"
def nsrFn(resultsPath, runID, resHour, regScenario):
  """create user constraints for nsr within window defined by resHour
  according to the logic of the regScenario """
  print("nsrFn called")

  # load parameter file for run
  params = pd.read_csv(resultsPath + "params_run" + str(runID) + ".csv")
  battpwr = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'ch_max_rated'),'Value'].values[0])
  battpwrd = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'dis_max_rated'),'Value'].values[0])
  battcapmax = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'ene_max_rated'),'Value'].values[0])
  maxsoc = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'ulsoc'),'Value'].values[0])
  minsoc = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'llsoc'),'Value'].values[0])
  battcap = battcapmax * (maxsoc / 100)
  rte = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'rte'),'Value'].values[0])/100

  # nsr creates energy constraints, so we return only those
  # start by pre-filling output with dummy constraints that dont do anything - just replicate batt params
  output = pd.DataFrame(index = pd.date_range(start="1/1/2017",periods=8760,freq="h"), columns = ["chgMin_kW","chgMax_kW","eMin_kWh","eMax_kWh"])
  output.loc[:,"eMin_kWh"] = battcap * (minsoc/100)
  output.loc[:,"eMax_kWh"] = battcap * (maxsoc/100)
  output.loc[:,"chgMin_kW"] = battpwr * -1
  output.loc[:,"chgMax_kW"] = battpwr

  # load timeseries - has prices, results
  timeseries = pd.read_csv(resultsPath + "timeseries_results_runID" + str(runID) + ".csv"  )
  timeseries["date"] = pd.to_datetime(timeseries['Start Datetime (hb)'])
  timeseries = timeseries.set_index('date')

  if regScenario == 1:
    ## create reservations based on resHours
    ### ID duration of NSR commitment & batt storage size -> calculate energy reservation requirement
    # chgMin is so that batt can reduce charging to provide NSR - since it's not possible to simulate the battery
    # charging at a set amount each hour for a large number of hours (as it would get full) we will just model
    # the reservation of SOC for NSR via discharging
    #TODO: account for different ch/disch, and CHARGING EFFICIENCY
    # dur = float(params.loc[(params['Tag'] == 'NSR') & (params['Key'] == 'duration'),'Value'].values[0])
    # if dur >1:
    #   nrgres = battpwr #here we convert from power (kW) to energy (kWh)
    # else:
    #   nrgres = battpwr * (1/dur)
    # ## insert into output during approppriate times
    # output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'eMin_kWh'] = nrgres + (battcapmax * minsoc/100)
    output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'eMin_kWh'] = (battcapmax * (minsoc / 100)) + battpwr#nrgres + (battcapmax * minsoc/100)
    output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'eMax_kWh'] = battcap - rte*battpwr
    output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'chgMin_kW'] = -1
    output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'chgMax_kW'] = 1

    # calculate value - multiply NSR price signal by battpwr for every active hour
    valueseries = timeseries.loc[:,"NSR Price Signal ($/kW)"] * battpwr
    ll = (timeseries.index.hour >= resHour[0]) & (timeseries.index.hour <= resHour[1])
    value = sum(valueseries[ll])

  elif regScenario == 2:
    raise ValueError("regScenario 2 has not been coded yet")
  elif regScenario == 3:
    #create reservations based on previous dispatch
    # colnames = ['Non-spinning Reserve (Charging) (kW)','Non-spinning Reserve (Discharging) (kW)']
    # minres = timeseries['Non-spinning Reserve (Discharging) (kW)'] + (battcapmax * minsoc/100)
    # chgres = timeseries['Non-spinning Reserve (Charging) (kW)']
    # output.loc[:,'eMin_kWh'] = minres
    # output.loc[:,'chgMin_kW'] = chgres
    
    #avoid infeasibility: pwrmin and pwrmax must not be equal. (same for energy)
    sel = (timeseries['Non-spinning Reserve (Discharging) (kW)'] + timeseries['Non-spinning Reserve (Charging) (kW)']) == battpwr*2
    timeseries.loc[sel,'Non-spinning Reserve (Discharging) (kW)'] = timeseries.loc[sel,'Non-spinning Reserve (Discharging) (kW)'] -1
      
    chgmin = -1*(battpwrd - timeseries['Non-spinning Reserve (Discharging) (kW)'])
    chgmax = battpwr - timeseries['Non-spinning Reserve (Charging) (kW)']
    pwrmin = (battcapmax * (minsoc / 100)) + timeseries['Non-spinning Reserve (Discharging) (kW)']
    pwrmax = battcap - rte*timeseries['Non-spinning Reserve (Charging) (kW)']
    output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'chgMin_kW'] = chgmin.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1])]
    output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'chgMax_kW'] = chgmax.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1])]
    output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'eMin_kWh'] = pwrmin.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1])]
    output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'eMax_kWh'] = pwrmax.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1])]


    valueseries = timeseries.loc[:,"NSR Price Signal ($/kW)"] * (timeseries['Non-spinning Reserve (Discharging) (kW)'] + timeseries['Non-spinning Reserve (Charging) (kW)'])
    ll = (timeseries.index.hour >= resHour[0]) & (timeseries.index.hour <= resHour[1])
    value = sum(valueseries[ll])
  else:
    raise ValueError("regScenario must be 1, 2 or 3")

  return(output, value)
#end nsrFn

# # runID = 107
runID = 108
# runID = 109
# regScenario = 1
# resHour = [14,20]
# # resultsPath = SVet_Path + "Results/output_run" + str(runID) + "_4h_SR/"#"timeseries_results_runID" + str(runID) + ".csv"
resultsPath = SVet_Path + "Results/output_run" + str(runID) + "_1h_SR/"#"timeseries_results_runID" + str(runID) + ".csv"
# resultsPath = SVet_Path + "Results/output_run" + str(runID) + "_0.5h_SR/"#"timeseries_results_runID" + str(runID) + ".csv"
def srFn(resultsPath, runID, resHour, regScenario):
  """create user constraints for sr within window defined by resHour
  according to the logic of the regScenario """
  print("srFn called")

  # load parameter file for run
  params = pd.read_csv(resultsPath + "params_run" + str(runID) + ".csv")
  battpwr = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'ch_max_rated'),'Value'].values[0])
  battpwrd = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'dis_max_rated'),'Value'].values[0])
  battcapmax = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'ene_max_rated'),'Value'].values[0])
  maxsoc = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'ulsoc'),'Value'].values[0])
  minsoc = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'llsoc'),'Value'].values[0])
  battcap = battcapmax * (maxsoc / 100)
  rte = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'rte'),'Value'].values[0])/100

  # sr creates energy constraints, so we return only those
  # start by pre-filling output with dummy constraints that dont do anything - just replicate batt params
  output = pd.DataFrame(index = pd.date_range(start="1/1/2017",periods=8760,freq="h"), columns = ["chgMin_kW","chgMax_kW","eMin_kWh","eMax_kWh"])
  output.loc[:,"eMin_kWh"] = battcap * (minsoc/100)
  output.loc[:,"eMax_kWh"] = battcap * (maxsoc/100)
  output.loc[:,"chgMin_kW"] = battpwr * -1
  output.loc[:,"chgMax_kW"] = battpwr

  # load timeseries - has prices, results
  timeseries = pd.read_csv(resultsPath + "timeseries_results_runID" + str(runID) + ".csv"  )
  timeseries["date"] = pd.to_datetime(timeseries['Start Datetime (hb)'])
  timeseries = timeseries.set_index('date')

  if regScenario == 1:
    ## create reservations based on resHours
    ### ID duration of sr commitment & batt storage size -> calculate energy reservation requirement
    #assumes ch and disch are equal
    #TODO: account for different ch/disch, and CHARGING EFFICIENCY
    # dur = float(params.loc[(params['Tag'] == 'SR') & (params['Key'] == 'duration'),'Value'].values[0])
    # if dur <= battcapmax/ch_max_rated:# >1: # assumes that ch and disch are equal!
      # nrgres = battpwr #here we convert from power (kW) to energy (kWh)
    # else:
      # nrgres = battpwr * (1/dur)
    ## insert into output during approppriate times
    output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'eMin_kWh'] = (battcapmax * (minsoc / 100)) + battpwr#nrgres + (battcapmax * minsoc/100)
    output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'eMax_kWh'] = battcap - rte*battpwr
    output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'chgMin_kW'] = -1
    output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'chgMax_kW'] = 1

    # calculate value - multiply SR price signal by battpwr for every active hour
    # TODO: does this account for both up and down regulation?
    valueseries = timeseries.loc[:,"SR Price Signal ($/kW)"] * battpwr
    ll = (timeseries.index.hour >= resHour[0]) & (timeseries.index.hour <= resHour[1])
    value = sum(valueseries[ll])

  elif regScenario == 2:
    raise ValueError("regScenario 2 has not been coded yet")
  elif regScenario == 3:
    #create reservations based on previous dispatch
    # colnames = ['Non-spinning Reserve (Charging) (kW)','Non-spinning Reserve (Discharging) (kW)']
    # min res = timeseries['Spinning Reserve (Discharging) (kW)'] + (battcapmax * minsoc/100)
    # chgres = timeseries['Spinning Reserve (Charging) (kW)']
    #avoid infeasibility
    sel = (timeseries['Non-spinning Reserve (Discharging) (kW)'] + timeseries['Non-spinning Reserve (Charging) (kW)']) == battpwr*2
    timeseries.loc[sel,'Non-spinning Reserve (Discharging) (kW)'] = timeseries.loc[sel,'Non-spinning Reserve (Discharging) (kW)'] -1

    chgmin = -1*(battpwrd - timeseries['Spinning Reserve (Discharging) (kW)'])
    chgmax = battpwr - timeseries['Spinning Reserve (Charging) (kW)']
    pwrmin = (battcapmax * (minsoc / 100)) + timeseries['Spinning Reserve (Discharging) (kW)']
    pwrmax = battcap - rte*timeseries['Spinning Reserve (Charging) (kW)']
    output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'chgMin_kW'] = chgmin.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1])]
    output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'chgMax_kW'] = chgmax.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1])]
    output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'eMin_kWh'] = pwrmin.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1])]
    output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'eMax_kWh'] = pwrmax.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1])]

    valueseries = timeseries.loc[:,"SR Price Signal ($/kW)"] * (timeseries['Spinning Reserve (Discharging) (kW)'] + timeseries['Spinning Reserve (Charging) (kW)'])
    # this won't match the objective_values.csv values because those do not take into account model predictive control for SR in which last chunk of run is discarded
    ll = (timeseries.index.hour >= resHour[0]) & (timeseries.index.hour <= resHour[1])
    value = sum(valueseries[ll])
  else:
    raise ValueError("regScenario must be 1, 2 or 3")

  return(output, value)
#end srFn

runID = 110
regScenario = 1
resHour = [14,20]
resultsPath = SVet_Path + "Results/output_run" + str(runID) + "_FR_only/"
def frFn(resultsPath, runID, resHour, regScenario):
  """create user constraints for frequency regulation within window defined by resHour
  according to the logic of the regScenario """
  print("frFn called")

  # load parameter file for run
  params = pd.read_csv(resultsPath + "params_run" + str(runID) + ".csv")
  battpwr = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'ch_max_rated'),'Value'].values[0])
  battcapmax = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'ene_max_rated'),'Value'].values[0])
  maxsoc = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'ulsoc'),'Value'].values[0])
  minsoc = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'llsoc'),'Value'].values[0])
  splitmktTF = bool(params.loc[(params['Tag'] == 'FR') & (params['Key'] == 'CombinedMarket'),'Value'].values[0])

    # start by pre-filling output with dummy constraints that dont do anything - just replicate batt params
  output = pd.DataFrame(index = pd.date_range(start="1/1/2017",periods=8760,freq="h"), columns = ["chgMin_kW","chgMax_kW","eMin_kWh","eMax_kWh"])
  output.loc[:,"eMin_kWh"] = battcap * (minsoc/100)
  output.loc[:,"eMax_kWh"] = battcap * (maxsoc/100)
  output.loc[:,"chgMin_kW"] = battpwr * -1
  output.loc[:,"chgMax_kW"] = battpwr

  # load timeseries - has prices, results
  timeseries = pd.read_csv(resultsPath + "timeseries_results_runID" + str(runID) + ".csv"  )
  timeseries["date"] = pd.to_datetime(timeseries['Start Datetime (hb)'])
  timeseries = timeseries.set_index('date')

  if regScenario == 1:
    ## create reservations based on resHours
    ### ID duration of fr commitment & batt storage size -> calculate energy reservation requirement
    #TODO: account for different ch/disch, and CHARGING EFFICIENCY
    dur = float(params.loc[(params['Tag'] == 'FR') & (params['Key'] == 'duration'),'Value'].values[0])
    if dur >1:
      nrgres = battpwr #here we convert from power (kW) to energy (kWh)
    else:
      nrgres = battpwr * (1/dur)
    ## insert into output during approppriate times
    output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'eMin_kWh'] = nrgres + (battcapmax * minsoc/100)
    output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'eMax_kWh'] = (battcapmax * maxsoc/100) - nrgres

    # calculate value - multiply FR price signal by battpwr for every active hour
#    valueseries = timeseries.loc[:,"SR Price Signal ($/kW)"] * battpwr
    ll = (timeseries.index.hour >= resHour[0]) & (timeseries.index.hour <= resHour[1])
    value = sum(valueseries[ll])

  elif regScenario == 2:
    raise ValueError("regScenario 2 has not been coded yet")
  elif regScenario == 3:
    #create reservations based on previous dispatch
    # colnames = ['Non-spinning Reserve (Charging) (kW)','Non-spinning Reserve (Discharging) (kW)']
#    minres = timeseries['Spinning Reserve (Discharging) (kW)'] + (battcapmax * minsoc/100)
#    chgres = timeseries['Spinning Reserve (Charging) (kW)']
    output.loc[:,'eMin_kWh'] = minres
    output.loc[:,'chgMin_kW'] = chgres

#    valueseries = timeseries.loc[:,"SR Price Signal ($/kW)"] * (timeseries['Spinning Reserve (Discharging) (kW)'] + timeseries['Spinning Reserve (Charging) (kW)'])
    # this won't match the objective_values.csv values because those do not take into account model predictive control for SR in which last chunk of run is discarded
    ll = (timeseries.index.hour >= resHour[0]) & (timeseries.index.hour <= resHour[1])
    value = sum(valueseries[ll])
  else:
    raise ValueError("regScenario must be 1, 2 or 3")

  return(output, value)


# to save a csv:
  # save new params in results folder
  # param_filepath = SVet_Path + "Results/" + result_fol + "/params_run" + str(runID_num) + ".csv"
  # default_params.to_csv(param_filepath, index=False)
  
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
