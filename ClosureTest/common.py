import json
import ROOT
import re
import os
from collections import OrderedDict
from math import sqrt

##################
##  Basic SetUp ##
##################

cmsswBase = '../../'

inputFile_path = {
  '2016apv':     '/eos/cms/store/group/phys_top/ExtraYukawa/2016apvMerged/',
  '2016postapv': '/eos/cms/store/group/phys_top/ExtraYukawa/2016postapvMerged/',
  '2017':        '/eos/cms/store/group/phys_top/ExtraYukawa/TTC_version9/',
  '2018':        '/eos/cms/store/group/phys_top/ExtraYukawa/2018/'
}

subera_list = {
  '2016apv':     ['B2','C','D','E','F'],
  '2016postapv': ['F','G','H'],
  '2017':        ['B','C','D','E','F'],
  '2018':        ['A','B','C','D_0','D_1']
}

channel_list = {
  '2016apv':     {'DoubleElectron': ['SingleEG','DoubleEG'],
                  'ElectronMuon':   ['MuonEG','SingleMuon','SingleEG'],
                  'DoubleMuon':     ['SingleMuon','DoubleMuon']
                 },
  '2016postapv': {'DoubleElectron': ['SingleEG','DoubleEG'],
                  'ElectronMuon':   ['MuonEG','SingleMuon','SingleEG'],
                  'DoubleMuon':     ['SingleMuon','DoubleMuon']
                 },
  '2017':        {'DoubleElectron': ['SingleEG','DoubleEG'],
                  'ElectronMuon':   ['MuonEG','SingleMuon','SingleEG'],
                  'DoubleMuon':     ['SingleMuon','DoubleMuon']
                 },
  '2018':        {'DoubleElectron': ['EGamma'],
                  'ElectronMuon':   ['MuonEG','SingleMuon','EGamma'],
                  'DoubleMuon':     ['SingleMuon','DoubleMuon']
                 } 
}

####################
## Basic Function ##
####################

def FindProcess(era, fin_name):

  subprocess = fin_name.replace('.root','')

  jsonfile = open(os.path.join(cmsswBase + '/src/FakeRateClosureTest/data/sample_' + str(era) + 'UL.json'))
  samples  = json.load(jsonfile, encoding='utf-8', object_pairs_hook=OrderedDict).items()
  jsonfile.close()
  process = None

  for sample, desc in samples:
    if subprocess == sample:
      process = desc[2]
  
  return process

def GetTrainingFile(era, isTrain): # -1: drop, 0: used not for training, 1: used for training
  jsonfile = open(os.path.join(cmsswBase + '/src/FakeRateClosureTest/data/sample_' + str(era) + 'UL.json'))
  samples  = json.load(jsonfile, encoding='utf-8', object_pairs_hook=OrderedDict).items()
  jsonfile.close()
  TrainingFile_List = []
  for process, desc in samples:
    if desc[4] == isTrain:
      TrainingFile_List.append(str((process + ".root")))
  print(TrainingFile_List)
  return TrainingFile_List

def GetDataFile(era, channel):
  
  suberas = subera_list[era]
  samples = channel_list[era][channel]

  middle = '_' if '2016' in era else ''

  datafile_list = []

  for sample in samples:
    for subera in suberas:
      datafile_list.append(str(sample + middle + subera + '.root'))  

  return datafile_list

def GetTrigger_MC(era):

  jsonfile = open(os.path.join(cmsswBase + '/src/FakeRateClosureTest/data/DiLeptonTriggers_%s.json'%era))
  trig_list = json.load(jsonfile, encoding='utf-8')
  jsonfile.close()

  jsonfile = open(os.path.join(cmsswBase + '/src/FakeRateClosureTest/data/Trigger_command_%s.json'%era))
  trig_command_list = json.load(jsonfile, encoding='utf-8',object_pairs_hook=OrderedDict)
  jsonfile.close()

  ee_trigger = trig_command_list['DoubleElectron']['MC']
  em_trigger = trig_command_list['ElectronMuon']['MC']
  mm_trigger = trig_command_list['DoubleMuon']['MC']

  all_trigger = "((" + ee_trigger + ")||(" + em_trigger + ")||(" + mm_trigger + "))"

  return str(all_trigger)

def GetTrigger_Data(era, fin_name, channel):

  jsonfile = open(os.path.join(cmsswBase + '/src/FakeRateClosureTest/data/DiLeptonTriggers_%s.json'%era))
  run_dict = json.load(jsonfile, encoding='utf-8')
  jsonfile.close()

  jsonfile = open(os.path.join(cmsswBase + '/src/FakeRateClosureTest/data/Trigger_command_%s.json'%era))
  trig_command_list = json.load(jsonfile, encoding='utf-8',object_pairs_hook=OrderedDict)
  jsonfile.close()

  sample_list = channel_list[era][channel]

  dataset = None
  subera  = fin_name.replace('.root','')

  for sample in sample_list:
    if sample in fin_name:
      subera = subera.replace(str(sample),'')
      dataset = sample
  if '2016' in era:
    subera = subera.replace('_','')

  print(subera)

  DiLepton_slc_run = dict()
  Run_List = run_dict["Data"][channel][subera]

  for Name in Run_List.keys():
    DiLepton_slc_run[Name] = ROOT.std.vector('int')()
    for i in Run_List[Name]:
       DiLepton_slc_run[Name].push_back(i)

  if "EGamma" in fin_name:
    if channel == "DoubleElectron":
      Trigger = "(" + str(trig_command_list[channel]["Data"][subera]["DoubleEG"]) + ")||(" + str(trig_command_list[channel]["Data"][subera]["SingleEG"]) + ")"
    else:
      Trigger = trig_command_list[channel]["Data"][subera]["SingleEG"]
  else:
     Trigger = trig_command_list[channel]["Data"][subera][dataset]

  p1 = re.compile(r'[{](.*?)[}]', re.S)
  variables = re.findall(p1,Trigger)
  var_list = []
  for var in variables:
     Trigger = Trigger.replace(var,"")
     runs = eval(var)
     runs = [str(run) for run in runs]
     runs = ','.join(runs)
     run_command = "{" + runs + "}"
     var_list.append(run_command)

  Trigger = Trigger.format(*var_list)  

  return str(Trigger)

def GetMETFilter_MC(era, fin_name):

  jsonfile = open(os.path.join(cmsswBase + '/src/FakeRateClosureTest/data/%s_MET_Filters.json'%era))
  MET_list = json.load(jsonfile, encoding='utf-8',object_pairs_hook=OrderedDict)
  jsonfile.close()

  process     = FindProcess(era, fin_name)
  subprocess  = fin_name.replace('.root','')
  if 'ttc' not in fin_name:
    MET_filters = MET_list["MC"][process][subprocess]
  else:
    MET_filters = MET_list["MC"]["TT"]["TTTo2L"]
  MET_filter  = " && ".join(MET_filters)

  return str(MET_filter)


def GetMETFilter_Data(era):

  jsonfile = open(os.path.join(cmsswBase + '/src/FakeRateClosureTest/data/%s_MET_Filters.json'%era))
  MET_list = json.load(jsonfile, encoding='utf-8',object_pairs_hook=OrderedDict)
  jsonfile.close()

  MET_filters = MET_list["Data"]
  MET_filter = " && ".join(MET_filters)

  return MET_filter

def DefinePrefireWeight(df_MC_tree, era):

  if era == '2018':
    df_MC_tree = df_MC_tree.Define("PrefireWeight", "1.0f");
    df_MC_tree = df_MC_tree.Define("PrefireWeight_Up", "1.0f");
    df_MC_tree = df_MC_tree.Define("PrefireWeight_Down", "1.0f");

  return df_MC_tree

def get_mcEventnumber(filename):
  print 'opening file ', filename
  nevent_temp=0
  for i in range(0,len(filename)):
    ftemp=ROOT.TFile.Open(filename[i])
    htemp=ftemp.Get('nEventsGenWeighted')
    nevent_temp=nevent_temp+htemp.GetBinContent(1)
  return nevent_temp

def overunder_flowbin(h1):
  h1.SetBinContent(1,h1.GetBinContent(0)+h1.GetBinContent(1))
  h1.SetBinError(1,sqrt(h1.GetBinError(0)*h1.GetBinError(0)+h1.GetBinError(1)*h1.GetBinError(1)))
  h1.SetBinContent(h1.GetNbinsX(),h1.GetBinContent(h1.GetNbinsX())+h1.GetBinContent(h1.GetNbinsX()+1))
  h1.SetBinError(h1.GetNbinsX(),sqrt(h1.GetBinError(h1.GetNbinsX())*h1.GetBinError(h1.GetNbinsX())+h1.GetBinError(h1.GetNbinsX()+1)*h1.GetBinError(h1.GetNbinsX()+1)))
  return h1

def get_hist(df, hist_name, histo, weight):
  h = df.Histo1D((hist_name, '', histo[2], histo[0], histo[1]), hist_name, str(weight))
  h.Draw()
  return overunder_flowbin(h.GetValue().Clone())

def Add_2Dbin(h,addedX,addedY,addX,addY):
  h.SetBinContent(addedX, addedY, h.GetBinContent(addedX,addedY) + h.GetBinContent(addX,addY))
  h.SetBinError(addedX, addedY, sqrt(h.GetBinError(addedX, addedY)*h.GetBinError(addedX, addedY) + h.GetBinError(addX,addY)*h.GetBinError(addX,addY)))
  return h

def overunder_flowbin2D(h1):
  nbinX = h1.GetNbinsX()
  nbinY = h1.GetNbinsY()

  # Add Edge
  for i in range(nbinX):
    h1 = Add_2Dbin(h1, i+1,     1, i+1,       0)
    h1 = Add_2Dbin(h1, i+1, nbinY, i+1, nbinY+1)
  for i in range(nbinY):
    h1 = Add_2Dbin(h1,     1, i+1,       0, i+1)
    h1 = Add_2Dbin(h1, nbinX, i+1, nbinX+1, i+1)

  # Add Corner
  h1 = Add_2Dbin(h1, 1,         1,       0,       0)
  h1 = Add_2Dbin(h1, 1,     nbinY,       0, nbinY+1)
  h1 = Add_2Dbin(h1, nbinX,     1, nbinX+1,       0)
  h1 = Add_2Dbin(h1, nbinX, nbinY, nbinX+1, nbinY+1)
  return h1

def get_hist2D(df, hist_name, histo, weight,norm):
  h = df.Histo2D((hist_name, ';' + histo[0] + ';' + histo[1], histo[2], histo[3], histo[4], histo[5]), str(histo[0]), str(histo[1]), str(weight))
  h.Draw()
  h = overunder_flowbin2D(h.GetValue().Clone())
  if norm:
    for i in range(h.GetNbinsX()):
      integral = h.Integral(i+1, i+1, 1, h.GetNbinsY())
      if integral > 0:
        for j in range(h.GetNbinsY()):
          h.SetBinContent(i+1, j+1, h.GetBinContent(i+1,j+1)/integral)
  return h.Clone()
