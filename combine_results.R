# iterate through desired runIDs and calculate proforma
library(plyr)
library(tidyverse)
# runIDs = c(1,3,24,25,26)#  c(132,167,176,177)
# runIDs = c(51:76)
# runIDs = c(78:85)
resultsfolder = "/Applications/storagevet2v101/StorageVET-master-git/Results/"
#discount = 0.1
#growth_rate = 1.03
savecsv = T
plotTF = F

combine_results = function(runIDs, savecsv = F, plotTF = F,resultsfolder = "/Applications/storagevet2v101/StorageVET-master-git/Results/"){

  for(i in 1:length(runIDs)){
    # find run folder
    folders = list.files(resultsfolder, pattern = paste0("output_run",runIDs[i],"_"))
    if(length(folders) > 1){stop("too many output folders identified")
    } else if(length(folders) ==0){
      print(paste("run number", runIDs[i],"does not have an output folder and is skipped"))
      next()
    }
    
    # load pro-forma
    if(!file.exists(paste0(resultsfolder, folders[1],'/pro_forma_runID',runIDs[i],".csv"))){
      print(paste("run number", runIDs[i],"does not have a proforma and is skipped"))
      next()
    }
    inputs = read_csv(paste0(resultsfolder, folders[1],'/params_run',runIDs[i],".csv"))
    discount_rate = as.numeric(inputs[inputs$Tag == "Finance" & inputs$Key == "npv_discount_rate","Value"])/100
    inflation_rate = as.numeric(inputs[inputs$Tag == "Finance" & inputs$Key == "inflation_rate","Value"])/100
    discount = discount_rate + inflation_rate
    proforma = read_csv(paste0(resultsfolder, folders[1],'/pro_forma_runID',runIDs[i],".csv"))
    #create project year index for calculations
    proforma$year = as.numeric(proforma$X1)
    minyear = min(proforma$year,na.rm=T)
    proforma$projectyear = proforma$year - minyear
    
    # Is there a user constraint column? if so, fix it
    if("User Constraints Value" %in% dimnames(proforma)[[2]]){
      proforma$`User Constraints Value`= max(proforma$`User Constraints Value`) * (1 + inflation_rate)^proforma$projectyear
    }
    # need to do this after user constraint calculation
    proforma$projectyear[is.na(proforma$projectyear)] = 0
    
    # calculate NPV for each column
    npvbyyear = select(proforma, -X1, -year, -`Yearly Net Value`, -projectyear)
    for(j in 1:ncol(npvbyyear)){
      colname = dimnames(npvbyyear)[[2]][j]
      
      npvbyyear[,colname] = proforma[,colname] /((1+discount_rate)^proforma[,'projectyear'])
    }
    # sum and add to output framework
    tot = colSums(npvbyyear,na.rm=T)
    tot = pivot_wider(enframe(tot), values_from = value, names_from = name)
    # add run name and total value to tot
    tot$total = sum(tot[1,])
    tot$runID = runIDs[i]
    tot$outputfol = folders[1]
  
    # add NPV to output framework
    if(i==1){
      output = tot
    } else {
      output = rbind.fill(output, tot)
    }
    
    write_csv(npvbyyear, path = paste0(resultsfolder, folders[1],'/npv_by_year_runID',runIDs[i],".csv"))
    write_csv(proforma, path = paste0(resultsfolder, folders[1],'/proforma_recalculated_runID',runIDs[i],".csv"))
  }
  
  if(savecsv){write_csv(output,path = paste0(resultsfolder,"npv_runs",min(runIDs),"-",max(runIDs),".csv"))}
  
  dark2scale =c('#1b9e77','#d95f02','#7570b3','#e7298a','#66a61e','#e6ab02','#a6761d','#666666')
  scale = (c("#2f4f4f","#8b4513","#228b22","#000080","#ff0000","#ffff00","#00ff00","#00ffff","#ff00ff","#eee8aa","#6495ed","#ff69b4"))
  # create shorter names for each runID
  runnames = tibble(runID = output$runID)
  # runnames$shortname = c("Unconstrained", #131
  #                        "SR only", #132
  #                        "NSR only", #133
  #                        "Unconstrained, no RA", #134
  #                        "NSR must-offer", #135
  #                        "NSR must-offer no RA", #136
  #                        "NSR must-offer no RA", #138
  #                        "NSR priority no RA", #139
  #                        "SR must-offer", #140
  #                        "SR must-offer no RA", #141
  #                        "SR priority", #143
  #                        "SR priority, no RA", #144
  #                        "Unconstrained w FR", #151
  #                        "Unconst SR and NSR", #152
  #                        "FR only",
  #                        "unconstrained 2019",
  #                        "SR priority 24h no RA",
  #                        "SR priority 24h plus SR test",
  #                        "SR priority only") 
  # runnames$keyFn = c("Unconstrained",
  #                    "SR",
  #                    "NSR",
  #                    "Unconstrained",
  #                    "NSR",
  #                    "NSR",
  #                    "NSR",
  #                    "NSR",
  #                    "SR",
  #                    "SR",
  #                    "SR",
  #                    "SR",
  #                    "Unconstrained",
  #                    "Unconstrained",
  #                    "FR",
  #                    "Unconstrained",
  #                    "SR",
  #                    "SR",
  #                    "SR")
  # runnames$keyFn = c("SR","SR","SR","SR")
  # #RS1: must offer
  # #RS3: priority
  # output = merge(output, runnames, all.x = T)
  
  # runslog = read_csv(file = paste0(resultsfolder,"runsLog_old.csv"))
  runslog = read_csv(file = paste0(resultsfolder,"runsLog.csv"))
  output = merge(output, runslog[,c("runID","shortname", "description")], by = "runID")
  
  
  # create ability to subselect by runID
  if(plotTF){
    ## stacked revenue
    talloutput = pivot_longer(output, cols = c(-runID,-total,-outputfol,-shortname,-description),names_to = "value_type", values_to = "value")  #removed -keyFn
    talloutput$name = substr(talloutput$outputfol,10,100)
    tallrevenue = filter(talloutput,value>0)
    ggplot(tallrevenue,aes(fill = value_type, x = reorder(shortname,-total), y = value)) +
      geom_bar(position="stack", stat = "identity") +
      # geom_hline(yintercept = 0, color = "black") + 
      theme_minimal() + 
      # theme(axis.text.x = element_text(angle = 90, vjust = 0, hjust=1)) +
      theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1)) +
      scale_y_continuous(labels = scales::dollar_format()) +
      scale_fill_brewer(palette = "Dark2") # +
      # scale_fill_manual(values = scale)
    # ggsave(filename = paste0(resultsfolder,"SR_demo_plot_maxRA.png"), width = 8, height = 6)
    # can use removeGrid from package ggExtra to remove vertical gridlines in future
    # ggplot(data, aes(fill=condition, y=value, x=specie)) + 
    #   geom_bar(position="stack", stat="identity")
    
    # TODO: names of runs reflect number of hours with RA constraint
    output_constrained = output[output$runID %in% c(42,44,46,48),]
    output_constrained$Num_RA_Events = c(10,20,30,40)
    ggplot(output_constrained,aes(x=Num_RA_Events, y = total)) + geom_col() +
      ylim(-115000,0) +theme_minimal() +
      theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1)) +
      labs(y = "Total NPV", x="Number of days with RA events")
    
  
    ## stacked cost
    tallcost = filter(talloutput,value<0)
    ggplot(tallcost,aes(fill = value_type, x = name, y = value)) +
      geom_bar(position="stack", stat = "identity") +
      geom_hline(yintercept = 0, color = "black") + theme_minimal() + 
      theme(axis.text.x = element_text(angle = 50, vjust = 1, hjust=0.9)) +
      scale_y_continuous(labels = scales::dollar_format()) +
      scale_fill_brewer(palette = "Dark2")
    
    ## stacked value without NSR only
    tallrevSR = filter(talloutput, value>0 & keyFn != "NSR")
    tallrevSRshort = filter(tallrevSR,shortname == "Unconstrained" | shortname == "SR only" | shortname == "SR priority" | shortname == "SR priority, no RA" |
                              shortname == "SR priority 24h no RA" | shortname == "SR priority only")
    # tallrevSR$shortname = as.factor(tallrevSR$shortname)
    ggplot(tallrevSRshort,aes(fill = value_type, x = reorder(shortname, -total), y = value)) +
      geom_bar(position="stack", stat = "identity") +
      theme_minimal() + 
      theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1)) +
      scale_y_continuous(labels = scales::dollar_format()) +
      scale_fill_brewer(palette = "Dark2")
    
    
    ##total NPV
    
    ##total NPV w alternate RA values
    
    ##grouped bar of revenue types
    talloutput = pivot_longer(output, cols = c(-runID,-total,-outputfol),names_to = "value_type", values_to = "value")  
    talloutput$name = substr(talloutput$outputfol,10,100)
    tallrevenue = filter(talloutput,value>0)
    ggplot(tallrevenue,aes(fill = value_type, x = name , y = value)) +
      geom_bar(position="stack", stat = "identity") +
      # geom_hline(yintercept = 0, color = "black") + 
      theme_minimal() + 
      # theme(axis.text.x = element_text(angle = 90, vjust = 0, hjust=1)) +
      theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1)) +
      scale_y_continuous(labels = scales::dollar_format()) +
      scale_fill_brewer(palette = "Dark2") 
  }
    return(output)
}

