# adjust FR prices
library(tidyverse)
isolist = c("caiso",
             "ercot",
             "isone",
             "pjm",
             "nyiso")
folder = "/Applications/storagevet2v101/StorageVET-master-git/Data/"

factor = 0.25

for(i in 1:length(isolist)){
  file = paste0("hourly_timeseries_",isolist[i],"_2019.csv")
  dat = read_csv(paste0(folder, file))
  
  
  dat$`Reg Down Price ($/kW)` = dat$`Reg Down Price ($/kW)` * factor
  dat$`Reg Up Price ($/kW)` = dat$`Reg Up Price ($/kW)` * factor
  dat$`FR Price ($/kW)` = dat$`FR Price ($/kW)` * factor
  
  write_csv(dat,paste0(folder,"hourly_timeseries_",isolist[i],"_",factor,"_FR-prices.csv"))
}