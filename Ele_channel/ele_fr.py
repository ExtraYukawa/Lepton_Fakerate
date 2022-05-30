#==============
# Last used:
# python ele_fr.py --era 2016APV
# python ele_fr.py --era 2016postAPV
# python ele_fr.py --era 2017
# python ele_fr.py --era 2018
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

from argparse import ArgumentParser
parser = ArgumentParser()

parser.add_argument("--era", dest="era", default="2016APV",
                    help="When making the plots, read the files with this era(years), default: 2016APV")
opts = parser.parse_args()

TTC_header_path = os.path.join("TTC.h")
ROOT.gInterpreter.Declare('#include "{}"'.format(TTC_header_path))


# the EnableImplicitMT option should only use in cluster, at lxplus, it will make the code slower(my experience)
#ROOT.ROOT.EnableImplicitMT()

def overunder_flowbin(h2):
  binx=h2.GetNbinsX()
  biny=h2.GetNbinsY()
  for i in range(1,1+binx):
  #  h2.SetBinContent(i,1,h2.GetBinContent(i,0)+h2.GetBinContent(i,1))
  #  h2.SetBinError(i,1,sqrt(h2.GetBinError(i,0)*h2.GetBinError(i,0)+h2.GetBinError(i,1)*h2.GetBinError(i,1)))
    h2.SetBinContent(i,biny,h2.GetBinContent(i,biny)+h2.GetBinContent(i,biny+1))
    h2.SetBinError(i,biny,sqrt(h2.GetBinError(i,biny)*h2.GetBinError(i,biny)+h2.GetBinError(i,biny+1)*h2.GetBinError(i,biny+1)))
#  for i in range(1,1+biny):
#    h2.SetBinContent(1,i,h2.GetBinContent(0,i)+h2.GetBinContent(1,i))
#    h2.SetBinError(1,i,sqrt(h2.GetBinError(0,i)*h2.GetBinError(0,i)+h2.GetBinError(1,i)*h2.GetBinError(1,i)))
#    h2.SetBinContent(binx,i,h2.GetBinContent(binx,i)+h2.GetBinContent(binx+1,i))
#    h2.SetBinError(binx,i,sqrt(h2.GetBinError(binx,i)*h2.GetBinError(binx,i)+h2.GetBinError(binx+1,i)*h2.GetBinError(binx+1,i)))
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
    all_trigger = df.Filter("(HLT_Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30 && l1_conept< 30) || (HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30 && l1_conept > 30)")
  else:
    all_trigger = df.Filter("(HLT_Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30 && l1_pt< 30) || (HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30 && l1_pt > 30)")
  return all_trigger


def histos_book(opts, flist, filters, h2_model, isData = "False"):
  df_xyz_tree = ROOT.RDataFrame("Events",flist)
  df_xyz_tree = df_xyz_tree.Define("abs_l1eta","abs(l1_eta)")
  
  if not isData:
    if opts.era == "2017":
      df_xyz_tree = df_xyz_tree.Define("eff_lumi","MC_eff_lumi_"+opts.era+"(l1_conept)")
    else:
      df_xyz_tree = df_xyz_tree.Define("eff_lumi","MC_eff_lumi_"+opts.era+"(l1_pt)")
    if opts.era == "2018":
      df_xyz_tree = df_xyz_tree.Define("genweight","puWeight*eff_lumi*genWeight/abs(genWeight)") 
    else:
      df_xyz_tree = df_xyz_tree.Define("genweight","puWeight*eff_lumi*PrefireWeight*genWeight/abs(genWeight)") 

  # common for data/MC
  df_xyz = df_xyz_tree.Filter(filters)
  df_xyz_trigger = trigger(df_xyz)
  if not isData:
    df_xyz_histo = df_xyz_trigger.Histo2D(h2_model,"abs_l1eta","l1_pt",'genweight')
  else:
    if opts.era == "2017":
      df_xyz_histo = df_xyz_trigger.Histo2D(h2_model,"abs_l1eta","l1_conept")
    else:
      df_xyz_histo = df_xyz_trigger.Histo2D(h2_model,"abs_l1eta","l1_pt")

  df_xyz_histos = []
  h = df_xyz_histo.GetValue()
  df_xyz_histos.append(h.Clone())
  ROOT.TH1.AddDirectory(0)
  
  return df_xyz_histos


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


singleEG_names = ROOT.std.vector('string')()
if opts.era == "2016APV":
  print ("Reading 2016 APV files \n")
  for f in ["DoubleEG_B2.root","DoubleEG_C.root","DoubleEG_D.root", "DoubleEG_E.root", "DoubleEG_F.root"]:
    singleEG_names.push_back(path+f) #NOTE for 2016 we have DoubleEG
elif opts.era == "2016postAPV":
  print ("Reading 2016 postAPV files \n")
  for f in ["DoubleEGF.root", "DoubleEGG.root", "DoubleEGH.root"]:
    singleEG_names.push_back(path+f) #NOTE for 2016 we have DoubleEG
elif opts.era == "2017":
  print ("Reading 2017 files \n")
  for f in ["SingleEGC.root","SingleEGD.root","SingleEGE.root","SingleEGF.root"]:
    singleEG_names.push_back(path+f)
elif opts.era == "2018":
  print ("Reading 2018 files \n")
  for f in ["EGammaA.root","EGammaB.root","EGammaC.root","EGammaD.root"]:
    singleEG_names.push_back(path+f)
else:
  raise Exception ("select correct era!")

DY_list = ROOT.std.vector('string')()
for f in ['DYnlo.root']: #keep in mind for DYnlo.root
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
  filters_numerator="n_tight_ele==1 &&met<30 &&mt<30 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && jet_selection_30_dr07"
  filters_denominator="(n_tight_ele==1 ||n_fakeable_ele==1)&&met<30 && mt<30 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && jet_selection_30_dr07"

  h2_deno=ROOT.TH2D('','',5,etabin,4,ptbin)
  h2_nume=ROOT.TH2D('','',5,etabin,4,ptbin)
  h2_deno_model=ROOT.RDF.TH2DModel(h2_deno)
  h2_nume_model=ROOT.RDF.TH2DModel(h2_nume)


  SingleEG_deno_histo = histos_book(opts, singleEG_names, filters_denominator, h2_deno_model, True) #fixme def histos_book(opts, flist, filters, h2_model, isData = "False"):
  SingleEG_nume_histo = histos_book(opts, singleEG_names, filters_numerator, h2_nume_model, True)
  print ("SingleEG_deno_histo definition complete")
  # print "integral", SingleEG_deno_histo[0].Integral()
  # sys.exit(1)
  
  DY_deno_histo = histos_book(opts, DY_list, filters_denominator, h2_deno_model, False)
  DY_nume_histo = histos_book(opts, DY_list, filters_numerator, h2_nume_model, False)
  print ("DY definition complete!")
  
  WJet_deno_histo = histos_book(opts, WJet_list, filters_denominator, h2_deno_model, False)
  WJet_nume_histo = histos_book(opts, WJet_list, filters_numerator, h2_nume_model, False)
  print ("WJet definition complete!")
  
  TTTo1L_deno_histo = histos_book(opts, TTTo1L_list, filters_denominator, h2_deno_model, False)
  TTTo1L_nume_histo = histos_book(opts, TTTo1L_list, filters_numerator, h2_nume_model, False)
  print ("TTTo1L definition complete!")

  TTTo2L_deno_histo = histos_book(opts, TTTo2L_list, filters_denominator, h2_deno_model, False)
  TTTo2L_nume_histo = histos_book(opts, TTTo2L_list, filters_numerator, h2_nume_model, False)
  print ("TTTo2L definition complete!")
  
#  df_tsch_tree = ROOT.RDataFrame("Events",tsch_list)
#  df_tsch_tree = df_tsch_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
#  df_tsch_tree = df_tsch_tree.Define("genweight","puWeight*PrefireWeight*Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*Electron_CutBased_TightID_SF[ttc_l1_id]*Electron_CutBased_TightID_SF[ttc_l2_id]*trigger_SF*genWeight/abs(genWeight)")
#  df_tsch = df_tsch_tree.Filter(filters)
#  df_tsch_trigger = all_trigger(df_tsch)
#  df_tsch_histos=[]
#  for i in hists_name:
#    df_tsch_histo = df_tsch_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
#    df_tsch_histos.append(df_tsch_histo)
#
#  df_t_tch_tree = ROOT.RDataFrame("Events",t_tch_list)
#  df_t_tch_tree = df_t_tch_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
#  df_t_tch_tree = df_t_tch_tree.Define("genweight","puWeight*PrefireWeight*Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*Electron_CutBased_TightID_SF[ttc_l1_id]*Electron_CutBased_TightID_SF[ttc_l2_id]*trigger_SF*genWeight/abs(genWeight)")
#  df_t_tch = df_t_tch_tree.Filter(filters)
#  df_t_tch_trigger = all_trigger(df_t_tch)
#  df_t_tch_histos=[]
#  for i in hists_name:
#    df_t_tch_histo = df_t_tch_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
#    df_t_tch_histos.append(df_t_tch_histo)
#
#  df_tbar_tch_tree = ROOT.RDataFrame("Events",tbar_tch_list)
#  df_tbar_tch_tree = df_tbar_tch_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
#  df_tbar_tch_tree = df_tbar_tch_tree.Define("genweight","puWeight*PrefireWeight*Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*Electron_CutBased_TightID_SF[ttc_l1_id]*Electron_CutBased_TightID_SF[ttc_l2_id]*trigger_SF*genWeight/abs(genWeight)")
#  df_tbar_tch = df_tbar_tch_tree.Filter(filters)
#  df_tbar_tch_trigger = all_trigger(df_tbar_tch)
#  df_tbar_tch_histos=[]
#  for i in hists_name:
#    df_tbar_tch_histo = df_tbar_tch_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
#    df_tbar_tch_histos.append(df_tbar_tch_histo)
#
#  df_tW_tree = ROOT.RDataFrame("Events",tW_list)
#  df_tW_tree = df_tW_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
#  df_tW_tree = df_tW_tree.Define("genweight","puWeight*PrefireWeight*Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*Electron_CutBased_TightID_SF[ttc_l1_id]*Electron_CutBased_TightID_SF[ttc_l2_id]*trigger_SF*genWeight/abs(genWeight)")
#  df_tW = df_tW_tree.Filter(filters)
#  df_tW_trigger = all_trigger(df_tW)
#  df_tW_histos=[]
#  for i in hists_name:
#    df_tW_histo = df_tW_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
#    df_tW_histos.append(df_tW_histo)
#
#  df_tbarW_tree = ROOT.RDataFrame("Events",tbarW_list)
#  df_tbarW_tree = df_tbarW_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
#  df_tbarW_tree = df_tbarW_tree.Define("genweight","puWeight*PrefireWeight*Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*Electron_CutBased_TightID_SF[ttc_l1_id]*Electron_CutBased_TightID_SF[ttc_l2_id]*trigger_SF*genWeight/abs(genWeight)")
#  df_tbarW = df_tbarW_tree.Filter(filters)
#  df_tbarW_trigger = all_trigger(df_tbarW)
#  df_tbarW_histos=[]
#  for i in hists_name:
#    df_tbarW_histo = df_tbarW_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
#    df_tbarW_histos.append(df_tbarW_histo)
#
#  df_ttWtoLNu_tree = ROOT.RDataFrame("Events",ttWtoLNu_list)
#  df_ttWtoLNu_tree = df_ttWtoLNu_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
#  df_ttWtoLNu_tree = df_ttWtoLNu_tree.Define("genweight","puWeight*PrefireWeight*Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*Electron_CutBased_TightID_SF[ttc_l1_id]*Electron_CutBased_TightID_SF[ttc_l2_id]*trigger_SF*genWeight/abs(genWeight)")
#  df_ttWtoLNu = df_ttWtoLNu_tree.Filter(filters)
#  df_ttWtoLNu_trigger = all_trigger(df_ttWtoLNu)
#  df_ttWtoLNu_histos=[]
#  for i in hists_name:
#    df_ttWtoLNu_histo = df_ttWtoLNu_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
#    df_ttWtoLNu_histos.append(df_ttWtoLNu_histo)
#
#  df_ttWtoQQ_tree = ROOT.RDataFrame("Events",ttWtoQQ_list)
#  df_ttWtoQQ_tree = df_ttWtoQQ_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
#  df_ttWtoQQ_tree = df_ttWtoQQ_tree.Define("genweight","puWeight*PrefireWeight*Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*Electron_CutBased_TightID_SF[ttc_l1_id]*Electron_CutBased_TightID_SF[ttc_l2_id]*trigger_SF*genWeight/abs(genWeight)")
#  df_ttWtoQQ = df_ttWtoQQ_tree.Filter(filters)
#  df_ttWtoQQ_trigger = all_trigger(df_ttWtoQQ)
#  df_ttWtoQQ_histos=[]
#  for i in hists_name:
#    df_ttWtoQQ_histo = df_ttWtoQQ_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
#    df_ttWtoQQ_histos.append(df_ttWtoQQ_histo)
#
#  df_TTTo2L_tree = ROOT.RDataFrame("Events",TTTo2L_list)
#  df_TTTo2L_tree = df_TTTo2L_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
#  df_TTTo2L_tree = df_TTTo2L_tree.Define("genweight","puWeight*PrefireWeight*Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*Electron_CutBased_TightID_SF[ttc_l1_id]*Electron_CutBased_TightID_SF[ttc_l2_id]*trigger_SF*genWeight/abs(genWeight)")
#  df_TTTo2L = df_TTTo2L_tree.Filter(filters)
#  df_TTTo2L_trigger = all_trigger(df_TTTo2L)
#  df_TTTo2L_histos=[]
#  for i in hists_name:
#    df_TTTo2L_histo = df_TTTo2L_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
#    df_TTTo2L_histos.append(df_TTTo2L_histo)
#
#  df_TTTo1L_tree = ROOT.RDataFrame("Events",TTTo1L_list)
#  df_TTTo1L_tree = df_TTTo1L_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
#  df_TTTo1L_tree = df_TTTo1L_tree.Define("genweight","puWeight*PrefireWeight*Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*Electron_CutBased_TightID_SF[ttc_l1_id]*Electron_CutBased_TightID_SF[ttc_l2_id]*trigger_SF*genWeight/abs(genWeight)")
#  df_TTTo1L = df_TTTo1L_tree.Filter(filters)
#  df_TTTo1L_trigger = all_trigger(df_TTTo1L)
#  df_TTTo1L_histos=[]
#  for i in hists_name:
#    df_TTTo1L_histo = df_TTTo1L_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
#    df_TTTo1L_histos.append(df_TTTo1L_histo)


# ROOT version 6.14 don;t have function "ROOT.RDF.RunGraphs"
#  ROOT.RDF.RunGraphs({df_ZZG_histo, df_ZZ_histo, df_ggZZ_4e_histo,df_ggZZ_4mu_histo, df_ggZZ_4tau_histo, df_ggZZ_2e2mu_histo,df_ggZZ_2e2tau_histo, df_ggZZ_2mu2tau_histo, df_TTZ_histo,df_TTG_histo, df_WWZ_histo, df_WZG_histo,df_WZZ_histo, df_ZZZ_histo, df_WZTo3L_histo,df_WZTo2L_histo, df_ZG_histo})

  h_SingleEG_deno=SingleEG_deno_histo[0].Clone()
  h_SingleEG_nume=SingleEG_nume_histo[0].Clone()
  h_DY_deno=DY_deno_histo[0].Clone()
  h_DY_nume=DY_nume_histo[0].Clone()
  h_WJet_deno=WJet_deno_histo[0].Clone()
  h_WJet_nume=WJet_nume_histo[0].Clone()
  h_TTTo1L_deno=TTTo1L_deno_histo[0].Clone()
  h_TTTo1L_nume=TTTo1L_nume_histo[0].Clone()
  h_TTTo2L_deno=TTTo2L_deno_histo[0].Clone()
  h_TTTo2L_nume=TTTo2L_nume_histo[0].Clone()

  h_DY_deno.Scale(-1.*DY_xs/DY_ev)
  h_DY_nume.Scale(-1.*DY_xs/DY_ev)
  h_WJet_deno.Scale(-1.*WJet_xs/WJet_ev)
  h_WJet_nume.Scale(-1.*WJet_xs/WJet_ev)
  h_TTTo1L_deno.Scale(-1.*TTTo1L_xs/TTTo1L_ev)
  h_TTTo1L_nume.Scale(-1.*TTTo1L_xs/TTTo1L_ev)
  h_TTTo2L_deno.Scale(-1.*TTTo2L_xs/TTTo2L_ev)
  h_TTTo2L_nume.Scale(-1.*TTTo2L_xs/TTTo2L_ev)

  histos_deno.append(h_SingleEG_deno.Clone()) 
  histos_deno.append(h_DY_deno.Clone())
  histos_deno.append(h_WJet_deno.Clone())
  histos_deno.append(h_TTTo1L_deno.Clone())
  histos_deno.append(h_TTTo2L_deno.Clone())

  histos_nume.append(h_SingleEG_nume.Clone())
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
