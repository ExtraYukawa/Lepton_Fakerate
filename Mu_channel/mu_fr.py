#==============
# Last used:
# python mu_fr.py --era 2016APV --saveDir Mu_config1
# python mu_fr.py --era 2016postAPV --saveDir Mu_config1
# python mu_fr.py --era 2017 --saveDir Mu_config1
# python mu_fr.py --era 2018 --saveDir Mu_config1
#==============

import ROOT
import time
import os
import sys
import math
from array import array
from math import sqrt
import plot_fakerate

ROOT.gROOT.SetBatch(True) # no flashing canvases

SAVEFORMATS  = "png" #pdf,png,C"
SAVEDIR      = None

from argparse import ArgumentParser
parser = ArgumentParser()

parser.add_argument("--era", dest="era", default="2016APV",
                    help="When making the plots, read the files with this era(years), default: 2016APV")

parser.add_argument("-s", "--saveFormats", dest="saveFormats", default = SAVEFORMATS,
                      help="Save formats for all plots [default: %s]" % SAVEFORMATS)

parser.add_argument("--saveDir", dest="saveDir", default=SAVEDIR, 
                      help="Directory where all pltos will be saved [default: %s]" % SAVEDIR)

opts = parser.parse_args()


TTC_header_path = os.path.join("TTC.h")
ROOT.gInterpreter.Declare('#include "{}"'.format(TTC_header_path))


# the EnableImplicitMT option should only use in cluster, at lxplus, it will make the code slower(my experience)
#ROOT.ROOT.EnableImplicitMT()

def overunder_flowbin(h2):
  binx=h2.GetNbinsX()
  biny=h2.GetNbinsY()
  for i in range(1,1+binx):
    h2.SetBinContent(i,1,h2.GetBinContent(i,0)+h2.GetBinContent(i,1))
    h2.SetBinError(i,1,sqrt(h2.GetBinError(i,0)*h2.GetBinError(i,0)+h2.GetBinError(i,1)*h2.GetBinError(i,1)))
    h2.SetBinContent(i,biny,h2.GetBinContent(i,biny)+h2.GetBinContent(i,biny+1))
    h2.SetBinError(i,biny,sqrt(h2.GetBinError(i,biny)*h2.GetBinError(i,biny)+h2.GetBinError(i,biny+1)*h2.GetBinError(i,biny+1)))
  for i in range(1,1+biny):
    h2.SetBinContent(1,i,h2.GetBinContent(0,i)+h2.GetBinContent(1,i))
    h2.SetBinError(1,i,sqrt(h2.GetBinError(0,i)*h2.GetBinError(0,i)+h2.GetBinError(1,i)*h2.GetBinError(1,i)))
    h2.SetBinContent(binx,i,h2.GetBinContent(binx,i)+h2.GetBinContent(binx+1,i))
    h2.SetBinError(binx,i,sqrt(h2.GetBinError(binx,i)*h2.GetBinError(binx,i)+h2.GetBinError(binx+1,i)*h2.GetBinError(binx+1,i)))
  return h2

def get_mcEventnumber(filename):
  print 'opening file ', filename
  nevent_temp=0
  for i in range(0,len(filename)):
    ftemp=ROOT.TFile.Open(filename[i])
    htemp=ftemp.Get('nEventsGenWeighted')
    nevent_temp=nevent_temp+htemp.GetBinContent(1)
  return nevent_temp

def trigger(df):
  if opts.era == "2017":
    all_trigger = df.Filter("(HLT_Mu8_TrkIsoVVL && l1_conept < 25) || (HLT_Mu17_TrkIsoVVL && l1_conept > 25)")
  else:
    all_trigger = df.Filter("(HLT_Mu8_TrkIsoVVL && l1_pt < 25) || (HLT_Mu17_TrkIsoVVL && l1_pt > 25)")

  return all_trigger


# Select the corret path for different year

if opts.era == "2016APV":
  path='/eos/cms/store/group/phys_top/ExtraYukawa/Fakerate_dataset/2016apv/'
elif opts.era == "2016postAPV":
  path='/eos/cms/store/group/phys_top/ExtraYukawa/Fakerate_dataset/2016/'
elif opts.era == "2017":
  path='/eos/cms/store/group/phys_top/ExtraYukawa/Fakerate_dataset/2017/'
elif opts.era == "2018":
  path='/eos/cms/store/group/phys_top/ExtraYukawa/Fakerate_dataset/2018/'
else:
  raise Exception ("select correct era!")


doubleMu_names = ROOT.std.vector('string')()
if opts.era == "2016APV":
  print ("Reading 2016 APV files \n")
  for f in ["DoubleMuon_B2.root","DoubleMuon_C.root","DoubleMuon_D.root","DoubleMuon_E.root","DoubleMuon_F.root"]:
    doubleMu_names.push_back(path+f)

elif opts.era == "2016postAPV":
  print ("Reading 2016 postAPV files \n")
  for f in ["DoubleMuonF.root","DoubleMuonG.root","DoubleMuonH.root"]:
    doubleMu_names.push_back(path+f)

elif opts.era == "2017":
  print ("Reading 2017 files \n")
  for f in ["DoubleMuonB.root","DoubleMuonC.root","DoubleMuonD.root","DoubleMuonE.root","DoubleMuonF.root"]:
    doubleMu_names.push_back(path+f)

elif opts.era == "2018":
  print ("Reading 2018 files \n")
  for f in ["DoubleMuA.root","DoubleMuB.root","DoubleMuC.root","DoubleMuD.root"]:
    doubleMu_names.push_back(path+f)

else:
  raise Exception ("select correct era!")

DY_list = ROOT.std.vector('string')()
for f in ['DYnlo.root']:
  DY_list.push_back(path+f)

WJet_list = ROOT.std.vector('string')()
for f in ['WJets.root']:
  WJet_list.push_back(path+f)

TTTo1L_list = ROOT.std.vector('string')()
for f in ['TTTo1L.root']:
  TTTo1L_list.push_back(path+f)

TTTo2L_list = ROOT.std.vector('string')()
for f in ['TTTo2L.root']:
  TTTo2L_list.push_back(path+f)

def Fakerate_Analysis(opts):

  histos_deno = []
  histos_nume = []

  lumi = 65.647

  ptbin=array('d',[20, 30, 40, 60, 80])
  #ptbin=array('d',[20, 25, 30, 35, 45, 60])
  etabin=array('d',[0, 0.5,1.0,1.5,2.0,2.5])

  DY_xs = 6077.22
  DY_ev = get_mcEventnumber(DY_list)

  WJet_xs = 61526.7
  WJet_ev = get_mcEventnumber(WJet_list)

  TTTo1L_xs = 365.4574
  TTTo1L_ev = get_mcEventnumber(TTTo1L_list)

  TTTo2L_xs = 88.3419
  TTTo2L_ev = get_mcEventnumber(TTTo2L_list)

  # define the filters here, 1:2mu, 2:1e1m, 3:2ele
  filters_numerator="n_tight_muon==1 && mt<30 &&met<30 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && jet_selection_30_dr07"
  filters_denominator="(n_tight_muon==1 ||n_fakeable_muon==1)&& mt<30 && met<30 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && jet_selection_30_dr07"

  h2_deno=ROOT.TH2D('','',5,etabin,4,ptbin)
  h2_nume=ROOT.TH2D('','',5,etabin,4,ptbin)
  h2_deno_model=ROOT.RDF.TH2DModel(h2_deno)
  h2_nume_model=ROOT.RDF.TH2DModel(h2_nume)

  df_DoubleMu_deno_tree = ROOT.RDataFrame("Events", doubleMu_names)
  df_DoubleMu_deno_tree = df_DoubleMu_deno_tree.Define("abs_l1eta","abs(l1_eta)")
  df_DoubleMu_deno = df_DoubleMu_deno_tree.Filter(filters_denominator)
  df_DoubleMu_deno_trigger = trigger(df_DoubleMu_deno)
  if opts.era == "2017":
    df_DoubleMu_deno_histo = df_DoubleMu_deno_trigger.Histo2D(h2_deno_model,"abs_l1eta","l1_conept")
  else:
    df_DoubleMu_deno_histo = df_DoubleMu_deno_trigger.Histo2D(h2_deno_model,"abs_l1eta","l1_pt")

  df_DoubleMu_nume_tree = ROOT.RDataFrame("Events", doubleMu_names)
  df_DoubleMu_nume_tree = df_DoubleMu_nume_tree.Define("abs_l1eta","abs(l1_eta)")
  df_DoubleMu_nume = df_DoubleMu_nume_tree.Filter(filters_numerator)
  df_DoubleMu_nume_trigger = trigger(df_DoubleMu_nume)
  if opts.era == "2017":
    df_DoubleMu_nume_histo = df_DoubleMu_nume_trigger.Histo2D(h2_nume_model,"abs_l1eta","l1_conept")
  else:
    df_DoubleMu_nume_histo = df_DoubleMu_nume_trigger.Histo2D(h2_nume_model,"abs_l1eta","l1_pt")

  df_DY_deno_tree = ROOT.RDataFrame("Events",DY_list)
  df_DY_deno_tree = df_DY_deno_tree.Define("abs_l1eta","abs(l1_eta)")
  if opts.era == "2017":
    df_DY_deno_tree = df_DY_deno_tree.Define("eff_lumi","MC_eff_lumi_"+opts.era+"(l1_conept)")
  else:
    df_DY_deno_tree = df_DY_deno_tree.Define("eff_lumi","MC_eff_lumi_"+opts.era+"(l1_pt)")
  
  if opts.era == "2018":
    df_DY_deno_tree = df_DY_deno_tree.Define("genweight","puWeight*eff_lumi*genWeight/abs(genWeight)")
  else:
    df_DY_deno_tree = df_DY_deno_tree.Define("genweight","puWeight*eff_lumi*PrefireWeight*genWeight/abs(genWeight)")

  df_DY_deno = df_DY_deno_tree.Filter(filters_denominator)
  df_DY_deno_trigger = trigger(df_DY_deno)
  if opts.era == "2017":
    df_DY_deno_histo = df_DY_deno_trigger.Histo2D(h2_deno_model,"abs_l1eta","l1_conept",'genweight')
  else:
    df_DY_deno_histo = df_DY_deno_trigger.Histo2D(h2_deno_model,"abs_l1eta","l1_pt",'genweight')
  
  #aa = df_DY_deno_histo.GetValue()
  #print "aa.Integral()", aa.Integral()
  #sys.exit(1)
   
  df_DY_nume_tree = ROOT.RDataFrame("Events",DY_list)
  df_DY_nume_tree = df_DY_nume_tree.Define("abs_l1eta","abs(l1_eta)")
  if opts.era == "2017":
    df_DY_nume_tree = df_DY_nume_tree.Define("eff_lumi","MC_eff_lumi_"+opts.era+"(l1_conept)")
  else:
    df_DY_nume_tree = df_DY_nume_tree.Define("eff_lumi","MC_eff_lumi_"+opts.era+"(l1_pt)")
  
  if opts.era == "2018":
    df_DY_nume_tree = df_DY_nume_tree.Define("genweight","puWeight*eff_lumi*genWeight/abs(genWeight)")
  else:
    df_DY_nume_tree = df_DY_nume_tree.Define("genweight","puWeight*eff_lumi*PrefireWeight*genWeight/abs(genWeight)")
  df_DY_nume = df_DY_nume_tree.Filter(filters_numerator)
  df_DY_nume_trigger = trigger(df_DY_nume)
  if opts.era == "2017":
    df_DY_nume_histo = df_DY_nume_trigger.Histo2D(h2_nume_model,"abs_l1eta","l1_conept",'genweight')
  else:
    df_DY_nume_histo = df_DY_nume_trigger.Histo2D(h2_nume_model,"abs_l1eta","l1_pt",'genweight')

  df_WJet_deno_tree = ROOT.RDataFrame("Events",WJet_list)
  df_WJet_deno_tree = df_WJet_deno_tree.Define("abs_l1eta","abs(l1_eta)")
  if opts.era == "2017":
    df_WJet_deno_tree = df_WJet_deno_tree.Define("eff_lumi","MC_eff_lumi_"+opts.era+"(l1_conept)")
  else:
    df_WJet_deno_tree = df_WJet_deno_tree.Define("eff_lumi","MC_eff_lumi_"+opts.era+"(l1_pt)")
  
  if opts.era == "2018":
    df_WJet_deno_tree = df_WJet_deno_tree.Define("genweight","puWeight*eff_lumi*genWeight/abs(genWeight)")
  else:
    df_WJet_deno_tree = df_WJet_deno_tree.Define("genweight","puWeight*eff_lumi*PrefireWeight*genWeight/abs(genWeight)")
  df_WJet_deno = df_WJet_deno_tree.Filter(filters_denominator)
  df_WJet_deno_trigger = trigger(df_WJet_deno)
  if opts.era == "2017":
    df_WJet_deno_histo = df_WJet_deno_trigger.Histo2D(h2_deno_model,"abs_l1eta","l1_conept",'genweight')
  else:
    df_WJet_deno_histo = df_WJet_deno_trigger.Histo2D(h2_deno_model,"abs_l1eta","l1_pt",'genweight')

  df_WJet_nume_tree = ROOT.RDataFrame("Events",WJet_list)
  df_WJet_nume_tree = df_WJet_nume_tree.Define("abs_l1eta","abs(l1_eta)")
  if opts.era == "2017":
    df_WJet_nume_tree = df_WJet_nume_tree.Define("eff_lumi","MC_eff_lumi_"+opts.era+"(l1_conept)")
  else:
    df_WJet_nume_tree = df_WJet_nume_tree.Define("eff_lumi","MC_eff_lumi_"+opts.era+"(l1_pt)")

  if opts.era == "2018":
    df_WJet_nume_tree = df_WJet_nume_tree.Define("genweight","puWeight*eff_lumi*genWeight/abs(genWeight)")
  else:
    df_WJet_nume_tree = df_WJet_nume_tree.Define("genweight","puWeight*eff_lumi*PrefireWeight*genWeight/abs(genWeight)")
  df_WJet_nume = df_WJet_nume_tree.Filter(filters_numerator)
  df_WJet_nume_trigger = trigger(df_WJet_nume)
  if opts.era == "2017":
    df_WJet_nume_histo = df_WJet_nume_trigger.Histo2D(h2_nume_model,"abs_l1eta","l1_conept",'genweight')
  else:
    df_WJet_nume_histo = df_WJet_nume_trigger.Histo2D(h2_nume_model,"abs_l1eta","l1_pt",'genweight')

  df_TTTo1L_deno_tree = ROOT.RDataFrame("Events",TTTo1L_list)
  df_TTTo1L_deno_tree = df_TTTo1L_deno_tree.Define("abs_l1eta","abs(l1_eta)")
  if opts.era == "2017":
    df_TTTo1L_deno_tree = df_TTTo1L_deno_tree.Define("eff_lumi","MC_eff_lumi_"+opts.era+"(l1_conept)")
  else:
    df_TTTo1L_deno_tree = df_TTTo1L_deno_tree.Define("eff_lumi","MC_eff_lumi_"+opts.era+"(l1_pt)")
  
  if opts.era == "2018":
    df_TTTo1L_deno_tree = df_TTTo1L_deno_tree.Define("genweight","puWeight*eff_lumi*genWeight/abs(genWeight)")
  else:
    df_TTTo1L_deno_tree = df_TTTo1L_deno_tree.Define("genweight","puWeight*eff_lumi*PrefireWeight*genWeight/abs(genWeight)")
  df_TTTo1L_deno = df_TTTo1L_deno_tree.Filter(filters_denominator)
  df_TTTo1L_deno_trigger = trigger(df_TTTo1L_deno)
  if opts.era == "2017":
    df_TTTo1L_deno_histo = df_TTTo1L_deno_trigger.Histo2D(h2_nume_model,"abs_l1eta","l1_conept",'genweight')
  else:
    df_TTTo1L_deno_histo = df_TTTo1L_deno_trigger.Histo2D(h2_nume_model,"abs_l1eta","l1_pt",'genweight')

  df_TTTo1L_nume_tree = ROOT.RDataFrame("Events",TTTo1L_list)
  df_TTTo1L_nume_tree = df_TTTo1L_nume_tree.Define("abs_l1eta","abs(l1_eta)")
  if opts.era == "2017":
    df_TTTo1L_nume_tree = df_TTTo1L_nume_tree.Define("eff_lumi","MC_eff_lumi_"+opts.era+"(l1_conept)")
  else:
    df_TTTo1L_nume_tree = df_TTTo1L_nume_tree.Define("eff_lumi","MC_eff_lumi_"+opts.era+"(l1_pt)")
  
  if opts.era == "2018":
    df_TTTo1L_nume_tree = df_TTTo1L_nume_tree.Define("genweight","puWeight*eff_lumi*genWeight/abs(genWeight)")
  else:
    df_TTTo1L_nume_tree = df_TTTo1L_nume_tree.Define("genweight","puWeight*eff_lumi*PrefireWeight*genWeight/abs(genWeight)")
  df_TTTo1L_nume = df_TTTo1L_nume_tree.Filter(filters_numerator)
  df_TTTo1L_nume_trigger = trigger(df_TTTo1L_nume)
  if opts.era == "2017":
    df_TTTo1L_nume_histo = df_TTTo1L_nume_trigger.Histo2D(h2_nume_model,"abs_l1eta","l1_conept",'genweight')
  else:
    df_TTTo1L_nume_histo = df_TTTo1L_nume_trigger.Histo2D(h2_nume_model,"abs_l1eta","l1_pt",'genweight')

  df_TTTo2L_deno_tree = ROOT.RDataFrame("Events",TTTo2L_list)
  df_TTTo2L_deno_tree = df_TTTo2L_deno_tree.Define("abs_l1eta","abs(l1_eta)")
  if opts.era == "2017":
    df_TTTo2L_deno_tree = df_TTTo2L_deno_tree.Define("eff_lumi","MC_eff_lumi_"+opts.era+"(l1_conept)")
  else:
    df_TTTo2L_deno_tree = df_TTTo2L_deno_tree.Define("eff_lumi","MC_eff_lumi_"+opts.era+"(l1_pt)")
  
  if opts.era == "2018":
    df_TTTo2L_deno_tree = df_TTTo2L_deno_tree.Define("genweight","puWeight*eff_lumi*genWeight/abs(genWeight)")
  else:
    df_TTTo2L_deno_tree = df_TTTo2L_deno_tree.Define("genweight","puWeight*eff_lumi*PrefireWeight*genWeight/abs(genWeight)")
  df_TTTo2L_deno = df_TTTo2L_deno_tree.Filter(filters_denominator)
  df_TTTo2L_deno_trigger = trigger(df_TTTo2L_deno)
  if opts.era == "2017":
    df_TTTo2L_deno_histo = df_TTTo2L_deno_trigger.Histo2D(h2_nume_model,"abs_l1eta","l1_conept",'genweight')
  else:
    df_TTTo2L_deno_histo = df_TTTo2L_deno_trigger.Histo2D(h2_nume_model,"abs_l1eta","l1_pt",'genweight')

  df_TTTo2L_nume_tree = ROOT.RDataFrame("Events",TTTo2L_list)
  df_TTTo2L_nume_tree = df_TTTo2L_nume_tree.Define("abs_l1eta","abs(l1_eta)")
  if opts.era == "2017":
    df_TTTo2L_nume_tree = df_TTTo2L_nume_tree.Define("eff_lumi","MC_eff_lumi_"+opts.era+"(l1_conept)")
  else:
    df_TTTo2L_nume_tree = df_TTTo2L_nume_tree.Define("eff_lumi","MC_eff_lumi_"+opts.era+"(l1_pt)")
  
  if opts.era == "2018":
    df_TTTo2L_nume_tree = df_TTTo2L_nume_tree.Define("genweight","puWeight*eff_lumi*genWeight/abs(genWeight)")
  else:
    df_TTTo2L_nume_tree = df_TTTo2L_nume_tree.Define("genweight","puWeight*eff_lumi*PrefireWeight*genWeight/abs(genWeight)")
  df_TTTo2L_nume = df_TTTo2L_nume_tree.Filter(filters_numerator)
  df_TTTo2L_nume_trigger = trigger(df_TTTo2L_nume)
  if opts.era == "2017":
    df_TTTo2L_nume_histo = df_TTTo2L_nume_trigger.Histo2D(h2_nume_model,"abs_l1eta","l1_conept",'genweight')
  else:
    df_TTTo2L_nume_histo = df_TTTo2L_nume_trigger.Histo2D(h2_nume_model,"abs_l1eta","l1_pt",'genweight')


  df_DoubleMu_deno_histo.Draw()
  df_DoubleMu_nume_histo.Draw()
  df_DY_deno_histo.Draw()
  df_DY_nume_histo.Draw()
  df_WJet_deno_histo.Draw()
  df_WJet_nume_histo.Draw()
  df_TTTo1L_deno_histo.Draw()
  df_TTTo1L_nume_histo.Draw()
  df_TTTo2L_deno_histo.Draw()
  df_TTTo2L_nume_histo.Draw()


  # ROOT version 6.14 don;t have function "ROOT.RDF.RunGraphs"
  #  ROOT.RDF.RunGraphs({df_ZZG_histo, df_ZZ_histo, df_ggZZ_4e_histo,df_ggZZ_4mu_histo, df_ggZZ_4tau_histo, df_ggZZ_2e2mu_histo,df_ggZZ_2e2tau_histo, df_ggZZ_2mu2tau_histo, df_TTZ_histo,df_TTG_histo, df_WWZ_histo, df_WZG_histo,df_WZZ_histo, df_ZZZ_histo, df_WZTo3L_histo,df_WZTo2L_histo, df_ZG_histo})

  h_DoubleMu_deno=df_DoubleMu_deno_histo.GetValue()
  h_DoubleMu_nume=df_DoubleMu_nume_histo.GetValue()
  h_DY_deno=df_DY_deno_histo.GetValue()
  h_DY_nume=df_DY_nume_histo.GetValue()
  h_WJet_deno=df_WJet_deno_histo.GetValue()
  h_WJet_nume=df_WJet_nume_histo.GetValue()
  h_TTTo1L_deno=df_TTTo1L_deno_histo.GetValue()
  h_TTTo1L_nume=df_TTTo1L_nume_histo.GetValue()
  h_TTTo2L_deno=df_TTTo2L_deno_histo.GetValue()
  h_TTTo2L_nume=df_TTTo2L_nume_histo.GetValue()

  h_DY_deno.Scale(-1.*DY_xs/DY_ev)
  h_DY_nume.Scale(-1.*DY_xs/DY_ev)
  h_WJet_deno.Scale(-1.*WJet_xs/WJet_ev)
  h_WJet_nume.Scale(-1.*WJet_xs/WJet_ev)
  h_TTTo1L_deno.Scale(-1.*TTTo1L_xs/TTTo1L_ev)
  h_TTTo1L_nume.Scale(-1.*TTTo1L_xs/TTTo1L_ev)
  h_TTTo2L_deno.Scale(-1.*TTTo2L_xs/TTTo2L_ev)
  h_TTTo2L_nume.Scale(-1.*TTTo2L_xs/TTTo2L_ev)

  histos_deno.append(h_DoubleMu_deno.Clone()) 
  histos_deno.append(h_DY_deno.Clone())
  histos_deno.append(h_WJet_deno.Clone())
  histos_deno.append(h_TTTo1L_deno.Clone())
  histos_deno.append(h_TTTo2L_deno.Clone())

  histos_nume.append(h_DoubleMu_nume.Clone())
  histos_nume.append(h_DY_nume.Clone())
  histos_nume.append(h_WJet_nume.Clone())
  histos_nume.append(h_TTTo1L_nume.Clone())
  histos_nume.append(h_TTTo2L_nume.Clone())

  for i in range(0,5):
    #  for i in range(0,1):
    histos_deno[i]=overunder_flowbin(histos_deno[i])
    histos_nume[i]=overunder_flowbin(histos_nume[i])

  c1 = plot_fakerate.draw_plots(opts, histos_nume, histos_deno, 1)
  del histos_deno[:]
  del histos_nume[:]
 
if __name__ == "__main__":
  start = time.time()
  start1 = time.clock() 

  Fakerate_Analysis(opts)

  end = time.time()
  end1 = time.clock()
  print "wall time:", end-start
  print "process time:", end1-start1
