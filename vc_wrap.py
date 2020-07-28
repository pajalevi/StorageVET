"""
vs_wrap.py

This wrapper script encloses calls to run_StorageVET.py in a version control framework.
It does the following
- edit default params based on arguments
- make a results folder for this run that is named with the runID
- save params in Results folder
- note this run in a run log with associated runID and git commit hash

Patricia Levi July 2020
"""

import pandas as pd
import os
import subprocess
import shlex
import datetime
import sys

SVet_Path = "/Applications/storagevet2v101/StorageVET-master-git/"
default_params_file = "Model_Parameters_2v1-0-2_default.csv"
runs_log_file = "Results/runsLog.csv"

#params = {'ICE_Active': 'yes', 'DR_days': 20, 'RA_idmode' : 'Peak by Month'} # for testing

def paramSetup(result_fol, runID_num, params, default_params_path = SVet_Path + default_params_file):
  """This function takes an arbitrary dict of params to modify, creates the appropriate 
  params csv, and saves it in result_fol. It returns the full filepath. The keys in params
  must have the format 'Tag_Key'  """
  
  # add Results_dir_absolute_path and Results_label to params
  params['Results_dir_absolute_path'] = SVet_Path + "Results/" + result_fol
  params['Results_label'] = "_runID" + str(runID_num)
  params['Results_errors_log_path'] = SVet_Path + "Results/" + result_fol + "/"
  
  #load default params csv
  default_params = pd.read_csv(SVet_Path + default_params_file)
  
  #parse params arg and change params
  for p in params:
    # parse out tag from key
    tag, key = p.split("_",1)
    filter_tag = default_params.Tag == tag
  
    if(key == "Active" or key == "active"):
      #change activity of that tag
      filter_activation = default_params.Active !=  "."
      filter_all = filter_tag & filter_activation
      if sum(filter_all) != 1:
          raise RuntimeError("Identified the wrong number of rows to change for Active status for tag " +  str(tag))
      default_params.loc[filter_all,'Active'] = params[p]
    else:
      # identify correct row, return error if not found
      filter_key = default_params.Key == key
      filter_all = filter_tag & filter_key 
      # change value
      default_params.loc[filter_all,'Value'] = params[p]
  
  # save new params in results folder
  param_filepath = SVet_Path + "Results/" + result_fol + "/params_run" + str(runID_num) + ".csv"
  default_params.to_csv(param_filepath, index=False)

  #return params file path
  return param_filepath
  
def runStorageVET(runID_num, newParams_path, SVet_Path = SVet_Path):
  "Runs StorageVET via command line"
  print("Running StorageVET for runID" + str(runID_num) + " with parameters in " + newParams_path)
  # check that result folder exists with param file in it
  if(not(os.path.exists(newParams_path))):
    raise FileNotFoundError("Params file does not exist. Given path was " + newParams_path)
  # call StorageVET
  process = subprocess.Popen(["python","/Applications/storagevet2v101/StorageVET-master-git/run_storagevet.py",newParams_path], stdout=sys.stdout) #stdout=subprocess.PIPE)
  # print output in realtime
  # while True:
  #   output = process.stdout.readline().decode()
  #   if output == '' and process.poll() is not None:
  #     break
  #   if output:
  #     print(output.strip())
  # rc = process.poll()
  # return rc
  

  
def updateRunLog(SVet_Path, runs_log_file, description, shortname):
  "Creates a new entry in Run Log, returns runID of current run"
  
  # test if runs log exists, create if no
  # with followng cols: runID, date, git hash, description
  if(not(os.path.exists(SVet_Path + runs_log_file))):
    raise FileNotFoundError("runs log file does not exist. Given path was "+SVet_Path+runs_log_file)
    #TODO: create empty runs log file instead

  # identify new runID by examining runs log
  runsLog = pd.read_csv(SVet_Path + runs_log_file)
  runID = int(runsLog[['runID']].max()) + 1
  print("This run has ID number " + str(runID))
  
  # identify current git hash
  # this must be called from within the git repo in order to work
  old_path = os.getcwd()
  os.chdir(SVet_Path)
  gitID_raw = subprocess.check_output(['git','rev-parse','--short','HEAD']).strip()
  gitID = gitID_raw.strip().decode('ascii')
  os.chdir(old_path)
  
  #get date
  date = datetime.datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
  
  # create entry in runs log
  new_run_log_line =  "\n" + str(runID) + "," + date + "," + gitID + "," + shortname.replace(",",".") + "," + description.replace(",",".")
  # append line
  with open(SVet_Path + runs_log_file, 'a') as rl:
    rl.write(new_run_log_line)
  
  #return runID
  return runID

  
def runWithVC(shortname, description, SVet_Path = SVet_Path, default_params_file = default_params_file, 
runs_log_file = runs_log_file, **params):
  """calls paramSetup, creates result folder, updates runsLog, and runs StorageVET
  params arguments should have the format 'Tag_Key = 'Value' """
  print(params)
  
  # update run log and get new runID
  runID_num = updateRunLog(SVet_Path, runs_log_file, description, shortname)
  
  # make results folder for that runID
  result_fol = "output_run" + str(runID_num) + "_" + shortname
  os.makedirs(SVet_Path + "Results/" + result_fol)

  # make new params file & save in results folder
  newParams_path = paramSetup(result_fol, runID_num, params, default_params_path = SVet_Path + default_params_file)
  
  # call storageVET
  runStorageVET(runID_num,newParams_path)

# import importlib
# importlib.reload(vc_wrap)  
# vc_wrap.runWithVC("test","testing out vc wrapper", PV_Active = 'yes', ICE_ccost = 2000)
# vc_wrap.runWithVC("DAFR_only","testing out vc wrapper with DA and FR only active", DR_Active = 'yes', FR_active = 'yes')

# vc_wrap.runWithVC("DAFR_only","testing out vc wrapper with DA and FR only active, 72 hour horizon", DR_Active = 'yes', FR_active = 'yes', Scenario_n = "72")
  
  
  
  
