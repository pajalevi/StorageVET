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
  battcapmax = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'ene_max_rated'),'Value'].values[0]) 
  maxsoc = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'ulsoc'),'Value'].values[0]) 
  minsoc = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'llsoc'),'Value'].values[0]) 
  battcap = battcapmax * (maxsoc / 100)

  # nsr creates energy constraints, so we return only those
  # start by pre-filling output with dummy constraints that dont do anything - just replicate batt params
  output = pd.DataFrame(index = pd.date_range(start="1/1/2017",periods=8760,freq="h"), columns = ["chgMin_kW","eMin_kWh"])  
  output.loc[:,"eMin_kWh"] = battcap * (minsoc/100)
  
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
    dur = float(params.loc[(params['Tag'] == 'NSR') & (params['Key'] == 'duration'),'Value'].values[0])
    if dur >1:
      nrgres = battpwr #here we convert from power (kW) to energy (kWh)
    else:
      nrgres = battpwr * (1/dur)
    ## insert into output during approppriate times
    output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'eMin_kWh'] = nrgres + (battcapmax * minsoc/100)
    
    # calculate value - multiply NSR price signal by battpwr for every active hour
    valueseries = timeseries.loc[:,"NSR Price Signal ($/kW)"] * battpwr
    ll = (timeseries.index.hour >= resHour[0]) & (timeseries.index.hour <= resHour[1])
    value = sum(valueseries[ll])

  elif regScenario == 2:
    raise ValueError("regScenario 2 has not been coded yet")
  elif regScenario == 3:
    #create reservations based on previous dispatch
    # colnames = ['Non-spinning Reserve (Charging) (kW)','Non-spinning Reserve (Discharging) (kW)']
    minres = timeseries['Non-spinning Reserve (Discharging) (kW)'] + (battcapmax * minsoc/100)
    chgres = timeseries['Non-spinning Reserve (Charging) (kW)']
    output.loc[:,'eMin_kWh'] = minres
    output.loc[:,'chgMin_kW'] = chgres

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
  battcapmax = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'ene_max_rated'),'Value'].values[0]) 
  maxsoc = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'ulsoc'),'Value'].values[0]) 
  minsoc = float(params.loc[(params['Tag'] == 'Battery') & (params['Key'] == 'llsoc'),'Value'].values[0]) 
  battcap = battcapmax * (maxsoc / 100)

  # sr creates energy constraints, so we return only those
  # start by pre-filling output with dummy constraints that dont do anything - just replicate batt params
  output = pd.DataFrame(index = pd.date_range(start="1/1/2017",periods=8760,freq="h"), columns = ["chgMin_kW","eMin_kWh"])  
  output.loc[:,"eMin_kWh"] = battcap * (minsoc/100)
  
  # load timeseries - has prices, results
  timeseries = pd.read_csv(resultsPath + "timeseries_results_runID" + str(runID) + ".csv"  )
  timeseries["date"] = pd.to_datetime(timeseries['Start Datetime (hb)'])
  timeseries = timeseries.set_index('date') 

  if regScenario == 1:
    ## create reservations based on resHours
    ### ID duration of sr commitment & batt storage size -> calculate energy reservation requirement
    #assumes ch and disch are equal
    #TODO: account for different ch/disch, and CHARGING EFFICIENCY
    dur = float(params.loc[(params['Tag'] == 'SR') & (params['Key'] == 'duration'),'Value'].values[0])
    if dur >1:
      nrgres = battpwr #here we convert from power (kW) to energy (kWh)
    else:
      nrgres = battpwr * (1/dur)
    ## insert into output during approppriate times
    output.loc[(output.index.hour >= resHour[0]) & (output.index.hour <= resHour[1]),'eMin_kWh'] = nrgres + (battcapmax * minsoc/100)
    
    # calculate value - multiply SR price signal by battpwr for every active hour
    valueseries = timeseries.loc[:,"SR Price Signal ($/kW)"] * battpwr
    ll = (timeseries.index.hour >= resHour[0]) & (timeseries.index.hour <= resHour[1])
    value = sum(valueseries[ll])

  elif regScenario == 2:
    raise ValueError("regScenario 2 has not been coded yet")
  elif regScenario == 3:
    #create reservations based on previous dispatch
    # colnames = ['Non-spinning Reserve (Charging) (kW)','Non-spinning Reserve (Discharging) (kW)']
    minres = timeseries['Spinning Reserve (Discharging) (kW)'] + (battcapmax * minsoc/100)
    chgres = timeseries['Spinning Reserve (Charging) (kW)']
    output.loc[:,'eMin_kWh'] = minres
    output.loc[:,'chgMin_kW'] = chgres
    
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
  output = pd.DataFrame(index = pd.date_range(start="1/1/2017",periods=8760,freq="h"), columns = ["eMax_kWh","eMin_kWh"])  
  output.loc[:,"eMin_kWh"] = battcapmax * (minsoc/100)
  output.loc[:,"eMax_kWh"] = battcapmax * (maxsoc/100)
  
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
