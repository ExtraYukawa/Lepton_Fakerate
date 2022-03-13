import ROOT
import time
import os
import math
from array import array
from math import sqrt
import plot_fakerate

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
  all_trigger = df.Filter("(HLT_Mu8 && l1_pt<30) || (HLT_Mu17 && l1_pt>30)")
  return all_trigger

path='/eos/user/m/melu/TTC_fakerate_newLepID_1129/'

#doubleMu_names = ROOT.std.vector('string')()
#for f in ["DoubleMuonB.root","DoubleMuonC.root","DoubleMuonD.root","DoubleMuonE.root","DoubleMuonF.root"]:
#  doubleMu_names.push_back(path+f)
#
#DY_list = ROOT.std.vector('string')()
#for f in ['DY.root']:
#  DY_list.push_back(path+f)
#
#WJet_list = ROOT.std.vector('string')()
#for f in ['WJets.root']:
#  WJet_list.push_back(path+f)

#TTTo1L_list = ROOT.std.vector('string')()
#for f in ['TTTo1L.root']:
#  TTTo1L_list.push_back(path+f)

QCD_15to20_list = ROOT.std.vector('string')()
for f in ['QCD15to20.root']:
  QCD_15to20_list.push_back(path+f)

QCD_20to30_list = ROOT.std.vector('string')()
for f in ['QCD20to30.root']:
  QCD_20to30_list.push_back(path+f)

QCD_30to50_list = ROOT.std.vector('string')()
for f in ['QCD30to50.root']:
  QCD_30to50_list.push_back(path+f)

QCD_50to80_list = ROOT.std.vector('string')()
for f in ['QCD50to80.root']:
  QCD_50to80_list.push_back(path+f)

QCD_80to120_list = ROOT.std.vector('string')()
for f in ['QCD80to120.root']:
  QCD_80to120_list.push_back(path+f)

QCD_120to170_list = ROOT.std.vector('string')()
for f in ['QCD120to170.root']:
  QCD_120to170_list.push_back(path+f)

QCD_170to300_list = ROOT.std.vector('string')()
for f in ['QCD170to300.root']:
  QCD_170to300_list.push_back(path+f)

QCD_300to470_list = ROOT.std.vector('string')()
for f in ['QCD300to470.root']:
  QCD_300to470_list.push_back(path+f)

QCD_470to600_list = ROOT.std.vector('string')()
for f in ['QCD470to600.root']:
  QCD_470to600_list.push_back(path+f)

QCD_600to800_list = ROOT.std.vector('string')()
for f in ['QCD600to800.root']:
  QCD_600to800_list.push_back(path+f)

QCD_800to1000_list = ROOT.std.vector('string')()
for f in ['QCD800to1000.root']:
  QCD_800to1000_list.push_back(path+f)

QCD_1000toInf_list = ROOT.std.vector('string')()
for f in ['QCD1000toInf.root']:
  QCD_1000toInf_list.push_back(path+f)

def Fakerate_Analysis():

  histos_deno = []
  histos_nume = []

#  lumi = 65.647

  ptbin=array('d',[20, 30, 40, 60, 80])
  #ptbin=array('d',[20, 25, 30, 35, 45, 60])
  etabin=array('d',[0, 0.5,1.0,1.5,2.0,2.5])

#  DY_xs = 6077.22
#  DY_ev = get_mcEventnumber(DY_list)
#
#  WJet_xs = 61526.7
#  WJet_ev = get_mcEventnumber(WJet_list)

#  TTTo1L_xs = 365.4574
#  TTTo1L_ev = get_mcEventnumber(TTTo1L_list)

  QCD_15to20_xs = 2799000.
  QCD_15to20_ev = get_mcEventnumber(QCD_15to20_list)

  QCD_20to30_xs = 2526000.
  QCD_20to30_ev = get_mcEventnumber(QCD_20to30_list)

  QCD_30to50_xs = 1362000.
  QCD_30to50_ev = get_mcEventnumber(QCD_30to50_list)

  QCD_50to80_xs = 376600.
  QCD_50to80_ev = get_mcEventnumber(QCD_50to80_list)

  QCD_80to120_xs = 88930.
  QCD_80to120_ev = get_mcEventnumber(QCD_80to120_list)

  QCD_120to170_xs = 21230.
  QCD_120to170_ev = get_mcEventnumber(QCD_120to170_list)

  QCD_170to300_xs = 7055.
  QCD_170to300_ev = get_mcEventnumber(QCD_170to300_list)

  QCD_300to470_xs = 619.3
  QCD_300to470_ev = get_mcEventnumber(QCD_300to470_list)

  QCD_470to600_xs = 59.24
  QCD_470to600_ev = get_mcEventnumber(QCD_470to600_list)

  QCD_600to800_xs = 18.21
  QCD_600to800_ev = get_mcEventnumber(QCD_600to800_list)

  QCD_800to1000_xs = 3.275
  QCD_800to1000_ev = get_mcEventnumber(QCD_800to1000_list)

  QCD_1000toInf_xs = 1.078
  QCD_1000toInf_ev = get_mcEventnumber(QCD_1000toInf_list)

  # define the filters here, 1:2mu, 2:1e1m, 3:2ele
  filters_numerator="n_tight_muon==1 &&met<30&&mt<30 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && jet_selection_30"
  filters_denominator="(n_tight_muon==1 ||n_fakeable_muon==1)&&met<30&&mt<30 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && jet_selection_30"

  h2_deno=ROOT.TH2D('','',5,etabin,4,ptbin)
  h2_nume=ROOT.TH2D('','',5,etabin,4,ptbin)
  h2_deno_model=ROOT.RDF.TH2DModel(h2_deno)
  h2_nume_model=ROOT.RDF.TH2DModel(h2_nume)

#  df_DoubleMu_deno_tree = ROOT.RDataFrame("Events", doubleMu_names)
#  df_DoubleMu_deno_tree = df_DoubleMu_deno_tree.Define("abs_l1eta","abs(l1_eta)")
#  df_DoubleMu_deno = df_DoubleMu_deno_tree.Filter(filters_denominator)
#  df_DoubleMu_deno_trigger = trigger(df_DoubleMu_deno)
#  df_DoubleMu_deno_histo = df_DoubleMu_deno_trigger.Histo2D(h2_deno_model,"abs_l1eta","l1_pt")
#
#  df_DoubleMu_nume_tree = ROOT.RDataFrame("Events", doubleMu_names)
#  df_DoubleMu_nume_tree = df_DoubleMu_nume_tree.Define("abs_l1eta","abs(l1_eta)")
#  df_DoubleMu_nume = df_DoubleMu_nume_tree.Filter(filters_numerator)
#  df_DoubleMu_nume_trigger = trigger(df_DoubleMu_nume)
#  df_DoubleMu_nume_histo = df_DoubleMu_nume_trigger.Histo2D(h2_nume_model,"abs_l1eta","l1_pt")
#
#  df_DY_deno_tree = ROOT.RDataFrame("Events",DY_list)
#  df_DY_deno_tree = df_DY_deno_tree.Define("abs_l1eta","abs(l1_eta)")
#  df_DY_deno_tree = df_DY_deno_tree.Define("genweight","puWeight*PrefireWeight*genWeight/abs(genWeight)")
#  df_DY_deno = df_DY_deno_tree.Filter(filters_denominator)
#  df_DY_deno_trigger = trigger(df_DY_deno)
#  df_DY_deno_histo = df_DY_deno_trigger.Histo2D(h2_deno_model,"abs_l1eta","l1_pt",'genweight')
#
#  df_DY_nume_tree = ROOT.RDataFrame("Events",DY_list)
#  df_DY_nume_tree = df_DY_nume_tree.Define("abs_l1eta","abs(l1_eta)")
#  df_DY_nume_tree = df_DY_nume_tree.Define("genweight","puWeight*PrefireWeight*genWeight/abs(genWeight)")
#  df_DY_nume = df_DY_nume_tree.Filter(filters_numerator)
#  df_DY_nume_trigger = trigger(df_DY_nume)
#  df_DY_nume_histo = df_DY_nume_trigger.Histo2D(h2_nume_model,"abs_l1eta","l1_pt",'genweight')
#
#  df_WJet_deno_tree = ROOT.RDataFrame("Events",WJet_list)
#  df_WJet_deno_tree = df_WJet_deno_tree.Define("abs_l1eta","abs(l1_eta)")
#  df_WJet_deno_tree = df_WJet_deno_tree.Define("genweight","puWeight*PrefireWeight*genWeight/abs(genWeight)")
#  df_WJet_deno = df_WJet_deno_tree.Filter(filters_denominator)
#  df_WJet_deno_trigger = trigger(df_WJet_deno)
#  df_WJet_deno_histo = df_WJet_deno_trigger.Histo2D(h2_deno_model,"abs_l1eta","l1_pt",'genweight')
#
#  df_WJet_nume_tree = ROOT.RDataFrame("Events",WJet_list)
#  df_WJet_nume_tree = df_WJet_nume_tree.Define("abs_l1eta","abs(l1_eta)")
#  df_WJet_nume_tree = df_WJet_nume_tree.Define("genweight","puWeight*PrefireWeight*genWeight/abs(genWeight)")
#  df_WJet_nume = df_WJet_nume_tree.Filter(filters_numerator)
#  df_WJet_nume_trigger = trigger(df_WJet_nume)
#  df_WJet_nume_histo = df_WJet_nume_trigger.Histo2D(h2_nume_model,"abs_l1eta","l1_pt",'genweight')

#  df_TTTo1L_deno_tree = ROOT.RDataFrame("Events",TTTo1L_list)
#  df_TTTo1L_deno_tree = df_TTTo1L_deno_tree.Define("abs_l1eta","abs(l1_eta)")
#  df_TTTo1L_deno_tree = df_TTTo1L_deno_tree.Define("genweight","puWeight*PrefireWeight*genWeight/abs(genWeight)")
#  df_TTTo1L_deno = df_TTTo1L_deno_tree.Filter(filters_denominator)
#  df_TTTo1L_deno_trigger = trigger(df_TTTo1L_deno)
#  df_TTTo1L_deno_histo = df_TTTo1L_deno_trigger.Histo2D(h2_nume_model,"abs_l1eta","l1_pt",'genweight')
#
#  df_TTTo1L_nume_tree = ROOT.RDataFrame("Events",TTTo1L_list)
#  df_TTTo1L_nume_tree = df_TTTo1L_nume_tree.Define("abs_l1eta","abs(l1_eta)")
#  df_TTTo1L_nume_tree = df_TTTo1L_nume_tree.Define("genweight","puWeight*PrefireWeight*genWeight/abs(genWeight)")
#  df_TTTo1L_nume = df_TTTo1L_nume_tree.Filter(filters_numerator)
#  df_TTTo1L_nume_trigger = trigger(df_TTTo1L_nume)
#  df_TTTo1L_nume_histo = df_TTTo1L_nume_trigger.Histo2D(h2_nume_model,"abs_l1eta","l1_pt",'genweight')

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

  df_QCD_15to20_list_deno_tree = ROOT.RDataFrame("Events",QCD_15to20_list)
  df_QCD_15to20_list_deno_tree = df_QCD_15to20_list_deno_tree.Define("abs_l1eta","abs(l1_eta)")
  df_QCD_15to20_list_deno_tree = df_QCD_15to20_list_deno_tree.Define("eff_lumi","MC_eff_lumi(l1_pt)")
  df_QCD_15to20_list_deno_tree = df_QCD_15to20_list_deno_tree.Define("genweight","puWeight*eff_lumi*PrefireWeight*genWeight/abs(genWeight)")
  df_QCD_15to20_list_deno = df_QCD_15to20_list_deno_tree.Filter(filters_denominator)
  df_QCD_15to20_list_deno_trigger = trigger(df_QCD_15to20_list_deno)
  df_QCD_15to20_list_deno_histo = df_QCD_15to20_list_deno_trigger.Histo2D(h2_deno_model,"abs_l1eta","l1_pt",'genweight')

  df_QCD_15to20_list_nume_tree = ROOT.RDataFrame("Events",QCD_15to20_list)
  df_QCD_15to20_list_nume_tree = df_QCD_15to20_list_nume_tree.Define("abs_l1eta","abs(l1_eta)")
  df_QCD_15to20_list_nume_tree = df_QCD_15to20_list_nume_tree.Define("eff_lumi","MC_eff_lumi(l1_pt)")
  df_QCD_15to20_list_nume_tree = df_QCD_15to20_list_nume_tree.Define("genweight","puWeight*eff_lumi*PrefireWeight*genWeight/abs(genWeight)")
  df_QCD_15to20_list_nume = df_QCD_15to20_list_nume_tree.Filter(filters_numerator)
  df_QCD_15to20_list_nume_trigger = trigger(df_QCD_15to20_list_nume)
  df_QCD_15to20_list_nume_histo = df_QCD_15to20_list_nume_trigger.Histo2D(h2_nume_model,"abs_l1eta","l1_pt",'genweight')

  df_QCD_20to30_list_deno_tree = ROOT.RDataFrame("Events",QCD_20to30_list)
  df_QCD_20to30_list_deno_tree = df_QCD_20to30_list_deno_tree.Define("abs_l1eta","abs(l1_eta)")
  df_QCD_20to30_list_deno_tree = df_QCD_20to30_list_deno_tree.Define("eff_lumi","MC_eff_lumi(l1_pt)")
  df_QCD_20to30_list_deno_tree = df_QCD_20to30_list_deno_tree.Define("genweight","puWeight*eff_lumi*PrefireWeight*genWeight/abs(genWeight)")
  df_QCD_20to30_list_deno = df_QCD_20to30_list_deno_tree.Filter(filters_denominator)
  df_QCD_20to30_list_deno_trigger = trigger(df_QCD_20to30_list_deno)
  df_QCD_20to30_list_deno_histo = df_QCD_20to30_list_deno_trigger.Histo2D(h2_deno_model,"abs_l1eta","l1_pt",'genweight')

  df_QCD_20to30_list_nume_tree = ROOT.RDataFrame("Events",QCD_20to30_list)
  df_QCD_20to30_list_nume_tree = df_QCD_20to30_list_nume_tree.Define("abs_l1eta","abs(l1_eta)")
  df_QCD_20to30_list_nume_tree = df_QCD_20to30_list_nume_tree.Define("eff_lumi","MC_eff_lumi(l1_pt)")
  df_QCD_20to30_list_nume_tree = df_QCD_20to30_list_nume_tree.Define("genweight","puWeight*eff_lumi*PrefireWeight*genWeight/abs(genWeight)")
  df_QCD_20to30_list_nume = df_QCD_20to30_list_nume_tree.Filter(filters_numerator)
  df_QCD_20to30_list_nume_trigger = trigger(df_QCD_20to30_list_nume)
  df_QCD_20to30_list_nume_histo = df_QCD_20to30_list_nume_trigger.Histo2D(h2_nume_model,"abs_l1eta","l1_pt",'genweight')

  df_QCD_30to50_list_deno_tree = ROOT.RDataFrame("Events",QCD_30to50_list)
  df_QCD_30to50_list_deno_tree = df_QCD_30to50_list_deno_tree.Define("abs_l1eta","abs(l1_eta)")
  df_QCD_30to50_list_deno_tree = df_QCD_30to50_list_deno_tree.Define("eff_lumi","MC_eff_lumi(l1_pt)")
  df_QCD_30to50_list_deno_tree = df_QCD_30to50_list_deno_tree.Define("genweight","puWeight*eff_lumi*PrefireWeight*genWeight/abs(genWeight)")
  df_QCD_30to50_list_deno = df_QCD_30to50_list_deno_tree.Filter(filters_denominator)
  df_QCD_30to50_list_deno_trigger = trigger(df_QCD_30to50_list_deno)
  df_QCD_30to50_list_deno_histo = df_QCD_30to50_list_deno_trigger.Histo2D(h2_deno_model,"abs_l1eta","l1_pt",'genweight')

  df_QCD_30to50_list_nume_tree = ROOT.RDataFrame("Events",QCD_30to50_list)
  df_QCD_30to50_list_nume_tree = df_QCD_30to50_list_nume_tree.Define("abs_l1eta","abs(l1_eta)")
  df_QCD_30to50_list_nume_tree = df_QCD_30to50_list_nume_tree.Define("eff_lumi","MC_eff_lumi(l1_pt)")
  df_QCD_30to50_list_nume_tree = df_QCD_30to50_list_nume_tree.Define("genweight","puWeight*eff_lumi*PrefireWeight*genWeight/abs(genWeight)")
  df_QCD_30to50_list_nume = df_QCD_30to50_list_nume_tree.Filter(filters_numerator)
  df_QCD_30to50_list_nume_trigger = trigger(df_QCD_30to50_list_nume)
  df_QCD_30to50_list_nume_histo = df_QCD_30to50_list_nume_trigger.Histo2D(h2_nume_model,"abs_l1eta","l1_pt",'genweight')

  df_QCD_50to80_list_deno_tree = ROOT.RDataFrame("Events",QCD_50to80_list)
  df_QCD_50to80_list_deno_tree = df_QCD_50to80_list_deno_tree.Define("abs_l1eta","abs(l1_eta)")
  df_QCD_50to80_list_deno_tree = df_QCD_50to80_list_deno_tree.Define("eff_lumi","MC_eff_lumi(l1_pt)")
  df_QCD_50to80_list_deno_tree = df_QCD_50to80_list_deno_tree.Define("genweight","puWeight*eff_lumi*PrefireWeight*genWeight/abs(genWeight)")
  df_QCD_50to80_list_deno = df_QCD_50to80_list_deno_tree.Filter(filters_denominator)
  df_QCD_50to80_list_deno_trigger = trigger(df_QCD_50to80_list_deno)
  df_QCD_50to80_list_deno_histo = df_QCD_50to80_list_deno_trigger.Histo2D(h2_deno_model,"abs_l1eta","l1_pt",'genweight')

  df_QCD_50to80_list_nume_tree = ROOT.RDataFrame("Events",QCD_50to80_list)
  df_QCD_50to80_list_nume_tree = df_QCD_50to80_list_nume_tree.Define("abs_l1eta","abs(l1_eta)")
  df_QCD_50to80_list_nume_tree = df_QCD_50to80_list_nume_tree.Define("eff_lumi","MC_eff_lumi(l1_pt)")
  df_QCD_50to80_list_nume_tree = df_QCD_50to80_list_nume_tree.Define("genweight","puWeight*eff_lumi*PrefireWeight*genWeight/abs(genWeight)")
  df_QCD_50to80_list_nume = df_QCD_50to80_list_nume_tree.Filter(filters_numerator)
  df_QCD_50to80_list_nume_trigger = trigger(df_QCD_50to80_list_nume)
  df_QCD_50to80_list_nume_histo = df_QCD_50to80_list_nume_trigger.Histo2D(h2_nume_model,"abs_l1eta","l1_pt",'genweight')

  df_QCD_80to120_list_deno_tree = ROOT.RDataFrame("Events",QCD_80to120_list)
  df_QCD_80to120_list_deno_tree = df_QCD_80to120_list_deno_tree.Define("abs_l1eta","abs(l1_eta)")
  df_QCD_80to120_list_deno_tree = df_QCD_80to120_list_deno_tree.Define("eff_lumi","MC_eff_lumi(l1_pt)")
  df_QCD_80to120_list_deno_tree = df_QCD_80to120_list_deno_tree.Define("genweight","puWeight*eff_lumi*PrefireWeight*genWeight/abs(genWeight)")
  df_QCD_80to120_list_deno = df_QCD_80to120_list_deno_tree.Filter(filters_denominator)
  df_QCD_80to120_list_deno_trigger = trigger(df_QCD_80to120_list_deno)
  df_QCD_80to120_list_deno_histo = df_QCD_80to120_list_deno_trigger.Histo2D(h2_deno_model,"abs_l1eta","l1_pt",'genweight')

  df_QCD_80to120_list_nume_tree = ROOT.RDataFrame("Events",QCD_80to120_list)
  df_QCD_80to120_list_nume_tree = df_QCD_80to120_list_nume_tree.Define("abs_l1eta","abs(l1_eta)")
  df_QCD_80to120_list_nume_tree = df_QCD_80to120_list_nume_tree.Define("eff_lumi","MC_eff_lumi(l1_pt)")
  df_QCD_80to120_list_nume_tree = df_QCD_80to120_list_nume_tree.Define("genweight","puWeight*eff_lumi*PrefireWeight*genWeight/abs(genWeight)")
  df_QCD_80to120_list_nume = df_QCD_80to120_list_nume_tree.Filter(filters_numerator)
  df_QCD_80to120_list_nume_trigger = trigger(df_QCD_80to120_list_nume)
  df_QCD_80to120_list_nume_histo = df_QCD_80to120_list_nume_trigger.Histo2D(h2_nume_model,"abs_l1eta","l1_pt",'genweight')

  df_QCD_120to170_list_deno_tree = ROOT.RDataFrame("Events",QCD_120to170_list)
  df_QCD_120to170_list_deno_tree = df_QCD_120to170_list_deno_tree.Define("abs_l1eta","abs(l1_eta)")
  df_QCD_120to170_list_deno_tree = df_QCD_120to170_list_deno_tree.Define("eff_lumi","MC_eff_lumi(l1_pt)")
  df_QCD_120to170_list_deno_tree = df_QCD_120to170_list_deno_tree.Define("genweight","puWeight*eff_lumi*PrefireWeight*genWeight/abs(genWeight)")
  df_QCD_120to170_list_deno = df_QCD_120to170_list_deno_tree.Filter(filters_denominator)
  df_QCD_120to170_list_deno_trigger = trigger(df_QCD_120to170_list_deno)
  df_QCD_120to170_list_deno_histo = df_QCD_120to170_list_deno_trigger.Histo2D(h2_deno_model,"abs_l1eta","l1_pt",'genweight')

  df_QCD_120to170_list_nume_tree = ROOT.RDataFrame("Events",QCD_120to170_list)
  df_QCD_120to170_list_nume_tree = df_QCD_120to170_list_nume_tree.Define("abs_l1eta","abs(l1_eta)")
  df_QCD_120to170_list_nume_tree = df_QCD_120to170_list_nume_tree.Define("eff_lumi","MC_eff_lumi(l1_pt)")
  df_QCD_120to170_list_nume_tree = df_QCD_120to170_list_nume_tree.Define("genweight","puWeight*eff_lumi*PrefireWeight*genWeight/abs(genWeight)")
  df_QCD_120to170_list_nume = df_QCD_120to170_list_nume_tree.Filter(filters_numerator)
  df_QCD_120to170_list_nume_trigger = trigger(df_QCD_120to170_list_nume)
  df_QCD_120to170_list_nume_histo = df_QCD_120to170_list_nume_trigger.Histo2D(h2_nume_model,"abs_l1eta","l1_pt",'genweight')

  df_QCD_170to300_list_deno_tree = ROOT.RDataFrame("Events",QCD_170to300_list)
  df_QCD_170to300_list_deno_tree = df_QCD_170to300_list_deno_tree.Define("abs_l1eta","abs(l1_eta)")
  df_QCD_170to300_list_deno_tree = df_QCD_170to300_list_deno_tree.Define("eff_lumi","MC_eff_lumi(l1_pt)")
  df_QCD_170to300_list_deno_tree = df_QCD_170to300_list_deno_tree.Define("genweight","puWeight*eff_lumi*PrefireWeight*genWeight/abs(genWeight)")
  df_QCD_170to300_list_deno = df_QCD_170to300_list_deno_tree.Filter(filters_denominator)
  df_QCD_170to300_list_deno_trigger = trigger(df_QCD_170to300_list_deno)
  df_QCD_170to300_list_deno_histo = df_QCD_170to300_list_deno_trigger.Histo2D(h2_deno_model,"abs_l1eta","l1_pt",'genweight')

  df_QCD_170to300_list_nume_tree = ROOT.RDataFrame("Events",QCD_170to300_list)
  df_QCD_170to300_list_nume_tree = df_QCD_170to300_list_nume_tree.Define("abs_l1eta","abs(l1_eta)")
  df_QCD_170to300_list_nume_tree = df_QCD_170to300_list_nume_tree.Define("eff_lumi","MC_eff_lumi(l1_pt)")
  df_QCD_170to300_list_nume_tree = df_QCD_170to300_list_nume_tree.Define("genweight","puWeight*eff_lumi*PrefireWeight*genWeight/abs(genWeight)")
  df_QCD_170to300_list_nume = df_QCD_170to300_list_nume_tree.Filter(filters_numerator)
  df_QCD_170to300_list_nume_trigger = trigger(df_QCD_170to300_list_nume)
  df_QCD_170to300_list_nume_histo = df_QCD_170to300_list_nume_trigger.Histo2D(h2_nume_model,"abs_l1eta","l1_pt",'genweight')

  df_QCD_300to470_list_deno_tree = ROOT.RDataFrame("Events",QCD_300to470_list)
  df_QCD_300to470_list_deno_tree = df_QCD_300to470_list_deno_tree.Define("abs_l1eta","abs(l1_eta)")
  df_QCD_300to470_list_deno_tree = df_QCD_300to470_list_deno_tree.Define("eff_lumi","MC_eff_lumi(l1_pt)")
  df_QCD_300to470_list_deno_tree = df_QCD_300to470_list_deno_tree.Define("genweight","puWeight*eff_lumi*PrefireWeight*genWeight/abs(genWeight)")
  df_QCD_300to470_list_deno = df_QCD_300to470_list_deno_tree.Filter(filters_denominator)
  df_QCD_300to470_list_deno_trigger = trigger(df_QCD_300to470_list_deno)
  df_QCD_300to470_list_deno_histo = df_QCD_300to470_list_deno_trigger.Histo2D(h2_deno_model,"abs_l1eta","l1_pt",'genweight')

  df_QCD_300to470_list_nume_tree = ROOT.RDataFrame("Events",QCD_300to470_list)
  df_QCD_300to470_list_nume_tree = df_QCD_300to470_list_nume_tree.Define("abs_l1eta","abs(l1_eta)")
  df_QCD_300to470_list_nume_tree = df_QCD_300to470_list_nume_tree.Define("eff_lumi","MC_eff_lumi(l1_pt)")
  df_QCD_300to470_list_nume_tree = df_QCD_300to470_list_nume_tree.Define("genweight","puWeight*eff_lumi*PrefireWeight*genWeight/abs(genWeight)")
  df_QCD_300to470_list_nume = df_QCD_300to470_list_nume_tree.Filter(filters_numerator)
  df_QCD_300to470_list_nume_trigger = trigger(df_QCD_300to470_list_nume)
  df_QCD_300to470_list_nume_histo = df_QCD_300to470_list_nume_trigger.Histo2D(h2_nume_model,"abs_l1eta","l1_pt",'genweight')

  df_QCD_470to600_list_deno_tree = ROOT.RDataFrame("Events",QCD_470to600_list)
  df_QCD_470to600_list_deno_tree = df_QCD_470to600_list_deno_tree.Define("abs_l1eta","abs(l1_eta)")
  df_QCD_470to600_list_deno_tree = df_QCD_470to600_list_deno_tree.Define("eff_lumi","MC_eff_lumi(l1_pt)")
  df_QCD_470to600_list_deno_tree = df_QCD_470to600_list_deno_tree.Define("genweight","puWeight*eff_lumi*PrefireWeight*genWeight/abs(genWeight)")
  df_QCD_470to600_list_deno = df_QCD_470to600_list_deno_tree.Filter(filters_denominator)
  df_QCD_470to600_list_deno_trigger = trigger(df_QCD_470to600_list_deno)
  df_QCD_470to600_list_deno_histo = df_QCD_470to600_list_deno_trigger.Histo2D(h2_deno_model,"abs_l1eta","l1_pt",'genweight')

  df_QCD_470to600_list_nume_tree = ROOT.RDataFrame("Events",QCD_470to600_list)
  df_QCD_470to600_list_nume_tree = df_QCD_470to600_list_nume_tree.Define("abs_l1eta","abs(l1_eta)")
  df_QCD_470to600_list_nume_tree = df_QCD_470to600_list_nume_tree.Define("eff_lumi","MC_eff_lumi(l1_pt)")
  df_QCD_470to600_list_nume_tree = df_QCD_470to600_list_nume_tree.Define("genweight","puWeight*eff_lumi*PrefireWeight*genWeight/abs(genWeight)")
  df_QCD_470to600_list_nume = df_QCD_470to600_list_nume_tree.Filter(filters_numerator)
  df_QCD_470to600_list_nume_trigger = trigger(df_QCD_470to600_list_nume)
  df_QCD_470to600_list_nume_histo = df_QCD_470to600_list_nume_trigger.Histo2D(h2_nume_model,"abs_l1eta","l1_pt",'genweight')

  df_QCD_600to800_list_deno_tree = ROOT.RDataFrame("Events",QCD_600to800_list)
  df_QCD_600to800_list_deno_tree = df_QCD_600to800_list_deno_tree.Define("abs_l1eta","abs(l1_eta)")
  df_QCD_600to800_list_deno_tree = df_QCD_600to800_list_deno_tree.Define("eff_lumi","MC_eff_lumi(l1_pt)")
  df_QCD_600to800_list_deno_tree = df_QCD_600to800_list_deno_tree.Define("genweight","puWeight*eff_lumi*PrefireWeight*genWeight/abs(genWeight)")
  df_QCD_600to800_list_deno = df_QCD_600to800_list_deno_tree.Filter(filters_denominator)
  df_QCD_600to800_list_deno_trigger = trigger(df_QCD_600to800_list_deno)
  df_QCD_600to800_list_deno_histo = df_QCD_600to800_list_deno_trigger.Histo2D(h2_deno_model,"abs_l1eta","l1_pt",'genweight')

  df_QCD_600to800_list_nume_tree = ROOT.RDataFrame("Events",QCD_600to800_list)
  df_QCD_600to800_list_nume_tree = df_QCD_600to800_list_nume_tree.Define("abs_l1eta","abs(l1_eta)")
  df_QCD_600to800_list_nume_tree = df_QCD_600to800_list_nume_tree.Define("eff_lumi","MC_eff_lumi(l1_pt)")
  df_QCD_600to800_list_nume_tree = df_QCD_600to800_list_nume_tree.Define("genweight","puWeight*eff_lumi*PrefireWeight*genWeight/abs(genWeight)")
  df_QCD_600to800_list_nume = df_QCD_600to800_list_nume_tree.Filter(filters_numerator)
  df_QCD_600to800_list_nume_trigger = trigger(df_QCD_600to800_list_nume)
  df_QCD_600to800_list_nume_histo = df_QCD_600to800_list_nume_trigger.Histo2D(h2_nume_model,"abs_l1eta","l1_pt",'genweight')

  df_QCD_800to1000_list_deno_tree = ROOT.RDataFrame("Events",QCD_800to1000_list)
  df_QCD_800to1000_list_deno_tree = df_QCD_800to1000_list_deno_tree.Define("abs_l1eta","abs(l1_eta)")
  df_QCD_800to1000_list_deno_tree = df_QCD_800to1000_list_deno_tree.Define("eff_lumi","MC_eff_lumi(l1_pt)")
  df_QCD_800to1000_list_deno_tree = df_QCD_800to1000_list_deno_tree.Define("genweight","puWeight*eff_lumi*PrefireWeight*genWeight/abs(genWeight)")
  df_QCD_800to1000_list_deno = df_QCD_800to1000_list_deno_tree.Filter(filters_denominator)
  df_QCD_800to1000_list_deno_trigger = trigger(df_QCD_800to1000_list_deno)
  df_QCD_800to1000_list_deno_histo = df_QCD_800to1000_list_deno_trigger.Histo2D(h2_deno_model,"abs_l1eta","l1_pt",'genweight')

  df_QCD_800to1000_list_nume_tree = ROOT.RDataFrame("Events",QCD_800to1000_list)
  df_QCD_800to1000_list_nume_tree = df_QCD_800to1000_list_nume_tree.Define("abs_l1eta","abs(l1_eta)")
  df_QCD_800to1000_list_nume_tree = df_QCD_800to1000_list_nume_tree.Define("eff_lumi","MC_eff_lumi(l1_pt)")
  df_QCD_800to1000_list_nume_tree = df_QCD_800to1000_list_nume_tree.Define("genweight","puWeight*eff_lumi*PrefireWeight*genWeight/abs(genWeight)")
  df_QCD_800to1000_list_nume = df_QCD_800to1000_list_nume_tree.Filter(filters_numerator)
  df_QCD_800to1000_list_nume_trigger = trigger(df_QCD_800to1000_list_nume)
  df_QCD_800to1000_list_nume_histo = df_QCD_800to1000_list_nume_trigger.Histo2D(h2_nume_model,"abs_l1eta","l1_pt",'genweight')

  df_QCD_1000toInf_list_deno_tree = ROOT.RDataFrame("Events",QCD_1000toInf_list)
  df_QCD_1000toInf_list_deno_tree = df_QCD_1000toInf_list_deno_tree.Define("abs_l1eta","abs(l1_eta)")
  df_QCD_1000toInf_list_deno_tree = df_QCD_1000toInf_list_deno_tree.Define("eff_lumi","MC_eff_lumi(l1_pt)")
  df_QCD_1000toInf_list_deno_tree = df_QCD_1000toInf_list_deno_tree.Define("genweight","puWeight*eff_lumi*PrefireWeight*genWeight/abs(genWeight)")
  df_QCD_1000toInf_list_deno = df_QCD_1000toInf_list_deno_tree.Filter(filters_denominator)
  df_QCD_1000toInf_list_deno_trigger = trigger(df_QCD_1000toInf_list_deno)
  df_QCD_1000toInf_list_deno_histo = df_QCD_1000toInf_list_deno_trigger.Histo2D(h2_deno_model,"abs_l1eta","l1_pt",'genweight')

  df_QCD_1000toInf_list_nume_tree = ROOT.RDataFrame("Events",QCD_1000toInf_list)
  df_QCD_1000toInf_list_nume_tree = df_QCD_1000toInf_list_nume_tree.Define("abs_l1eta","abs(l1_eta)")
  df_QCD_1000toInf_list_nume_tree = df_QCD_1000toInf_list_nume_tree.Define("eff_lumi","MC_eff_lumi(l1_pt)")
  df_QCD_1000toInf_list_nume_tree = df_QCD_1000toInf_list_nume_tree.Define("genweight","puWeight*eff_lumi*PrefireWeight*genWeight/abs(genWeight)")
  df_QCD_1000toInf_list_nume = df_QCD_1000toInf_list_nume_tree.Filter(filters_numerator)
  df_QCD_1000toInf_list_nume_trigger = trigger(df_QCD_1000toInf_list_nume)
  df_QCD_1000toInf_list_nume_histo = df_QCD_1000toInf_list_nume_trigger.Histo2D(h2_nume_model,"abs_l1eta","l1_pt",'genweight')

#  df_DoubleMu_deno_histo.Draw()
#  df_DoubleMu_nume_histo.Draw()
#  df_DY_deno_histo.Draw()
#  df_DY_nume_histo.Draw()
#  df_WJet_deno_histo.Draw()
#  df_WJet_nume_histo.Draw()
#  df_TTTo1L_deno_histo.Draw()
#  df_TTTo1L_nume_histo.Draw()
  df_QCD_15to20_list_deno_histo.Draw()
  df_QCD_15to20_list_nume_histo.Draw()
  df_QCD_20to30_list_deno_histo.Draw()
  df_QCD_20to30_list_nume_histo.Draw()
  df_QCD_30to50_list_deno_histo.Draw()
  df_QCD_30to50_list_nume_histo.Draw()
  df_QCD_50to80_list_deno_histo.Draw()
  df_QCD_50to80_list_nume_histo.Draw()
  df_QCD_80to120_list_deno_histo.Draw()
  df_QCD_80to120_list_nume_histo.Draw()
  df_QCD_120to170_list_deno_histo.Draw()
  df_QCD_120to170_list_nume_histo.Draw()
  df_QCD_170to300_list_deno_histo.Draw()
  df_QCD_170to300_list_nume_histo.Draw()
  df_QCD_300to470_list_deno_histo.Draw()
  df_QCD_300to470_list_nume_histo.Draw()
  df_QCD_470to600_list_deno_histo.Draw()
  df_QCD_470to600_list_nume_histo.Draw()
  df_QCD_600to800_list_deno_histo.Draw()
  df_QCD_600to800_list_nume_histo.Draw()
  df_QCD_1000toInf_list_deno_histo.Draw()
  df_QCD_1000toInf_list_nume_histo.Draw()

# ROOT version 6.14 don;t have function "ROOT.RDF.RunGraphs"
#  ROOT.RDF.RunGraphs({df_ZZG_histo, df_ZZ_histo, df_ggZZ_4e_histo,df_ggZZ_4mu_histo, df_ggZZ_4tau_histo, df_ggZZ_2e2mu_histo,df_ggZZ_2e2tau_histo, df_ggZZ_2mu2tau_histo, df_TTZ_histo,df_TTG_histo, df_WWZ_histo, df_WZG_histo,df_WZZ_histo, df_ZZZ_histo, df_WZTo3L_histo,df_WZTo2L_histo, df_ZG_histo})

#  h_DoubleMu_deno=df_DoubleMu_deno_histo.GetValue()
#  h_DoubleMu_nume=df_DoubleMu_nume_histo.GetValue()
#  h_DY_deno=df_DY_deno_histo.GetValue()
#  h_DY_nume=df_DY_nume_histo.GetValue()
#  h_WJet_deno=df_WJet_deno_histo.GetValue()
#  h_WJet_nume=df_WJet_nume_histo.GetValue()
#  h_TTTo1L_deno=df_TTTo1L_deno_histo.GetValue()
#  h_TTTo1L_nume=df_TTTo1L_nume_histo.GetValue()

  h_15to20_deno=df_QCD_15to20_list_deno_histo.GetValue()
  h_15to20_nume=df_QCD_15to20_list_nume_histo.GetValue()
  h_20to30_deno=df_QCD_20to30_list_deno_histo.GetValue()
  h_20to30_nume=df_QCD_20to30_list_nume_histo.GetValue()
  h_30to50_deno=df_QCD_30to50_list_deno_histo.GetValue()
  h_30to50_nume=df_QCD_30to50_list_nume_histo.GetValue()
  h_50to80_deno=df_QCD_50to80_list_deno_histo.GetValue()
  h_50to80_nume=df_QCD_50to80_list_nume_histo.GetValue()
  h_80to120_deno=df_QCD_80to120_list_deno_histo.GetValue()
  h_80to120_nume=df_QCD_80to120_list_nume_histo.GetValue()
  h_120to170_deno=df_QCD_120to170_list_deno_histo.GetValue()
  h_120to170_nume=df_QCD_120to170_list_nume_histo.GetValue()
  h_170to300_deno=df_QCD_170to300_list_deno_histo.GetValue()
  h_170to300_nume=df_QCD_170to300_list_nume_histo.GetValue()
  h_300to470_deno=df_QCD_300to470_list_deno_histo.GetValue()
  h_300to470_nume=df_QCD_300to470_list_nume_histo.GetValue()
  h_470to600_deno=df_QCD_470to600_list_deno_histo.GetValue()
  h_470to600_nume=df_QCD_470to600_list_nume_histo.GetValue()
  h_600to800_deno=df_QCD_600to800_list_deno_histo.GetValue()
  h_600to800_nume=df_QCD_600to800_list_nume_histo.GetValue()
  h_800to1000_deno=df_QCD_800to1000_list_deno_histo.GetValue()
  h_800to1000_nume=df_QCD_800to1000_list_nume_histo.GetValue()
  h_1000toInf_deno=df_QCD_1000toInf_list_deno_histo.GetValue()
  h_1000toInf_nume=df_QCD_1000toInf_list_nume_histo.GetValue()

  h_15to20_deno.Scale(QCD_15to20_xs/QCD_15to20_ev)
  h_15to20_nume.Scale(QCD_15to20_xs/QCD_15to20_ev)
  h_20to30_deno.Scale(QCD_20to30_xs/QCD_20to30_ev)
  h_20to30_nume.Scale(QCD_20to30_xs/QCD_20to30_ev)
  h_30to50_deno.Scale(QCD_30to50_xs/QCD_30to50_ev)
  h_30to50_nume.Scale(QCD_30to50_xs/QCD_30to50_ev)
  h_50to80_deno.Scale(QCD_50to80_xs/QCD_50to80_ev)
  h_50to80_nume.Scale(QCD_50to80_xs/QCD_50to80_ev)
  h_80to120_deno.Scale(QCD_80to120_xs/QCD_80to120_ev)
  h_80to120_nume.Scale(QCD_80to120_xs/QCD_80to120_ev)
  h_120to170_deno.Scale(QCD_120to170_xs/QCD_120to170_ev)
  h_120to170_nume.Scale(QCD_120to170_xs/QCD_120to170_ev)
  h_170to300_deno.Scale(QCD_170to300_xs/QCD_170to300_ev)
  h_170to300_nume.Scale(QCD_170to300_xs/QCD_170to300_ev)
  h_300to470_deno.Scale(QCD_300to470_xs/QCD_300to470_ev)
  h_300to470_nume.Scale(QCD_300to470_xs/QCD_300to470_ev)
  h_470to600_deno.Scale(QCD_470to600_xs/QCD_470to600_ev)
  h_470to600_nume.Scale(QCD_470to600_xs/QCD_470to600_ev)
  h_600to800_deno.Scale(QCD_600to800_xs/QCD_600to800_ev)
  h_600to800_nume.Scale(QCD_600to800_xs/QCD_600to800_ev)
  h_800to1000_deno.Scale(QCD_800to1000_xs/QCD_800to1000_ev)
  h_800to1000_nume.Scale(QCD_800to1000_xs/QCD_800to1000_ev)
  h_1000toInf_deno.Scale(QCD_1000toInf_xs/QCD_1000toInf_ev)
  h_1000toInf_nume.Scale(QCD_1000toInf_xs/QCD_1000toInf_ev)

#  h_DY_deno.Scale(-1.*DY_xs/DY_ev)
#  h_DY_nume.Scale(-1.*DY_xs/DY_ev)
#  h_WJet_deno.Scale(-1.*lumi*WJet_xs/WJet_ev)
#  h_WJet_nume.Scale(-1.*lumi*WJet_xs/WJet_ev)
#  h_TTTo1L_deno.Scale(-1.*lumi*TTTo1L_xs/TTTo1L_ev)
#  h_TTTo1L_nume.Scale(-1.*lumi*TTTo1L_xs/TTTo1L_ev)

#  histos_deno.append(h_DoubleMu_deno.Clone()) 
#  histos_deno.append(h_DY_deno.Clone())
#  histos_deno.append(h_WJet_deno.Clone())
#  histos_deno.append(h_TTTo1L_deno.Clone())
  histos_deno.append(h_15to20_deno.Clone())
  histos_deno.append(h_20to30_deno.Clone())
  histos_deno.append(h_30to50_deno.Clone())
  histos_deno.append(h_50to80_deno.Clone())
  histos_deno.append(h_80to120_deno.Clone())
  histos_deno.append(h_120to170_deno.Clone())
  histos_deno.append(h_170to300_deno.Clone())
  histos_deno.append(h_300to470_deno.Clone())
  histos_deno.append(h_470to600_deno.Clone())
  histos_deno.append(h_600to800_deno.Clone())
  histos_deno.append(h_800to1000_deno.Clone())
  histos_deno.append(h_1000toInf_deno.Clone())

#  histos_nume.append(h_DoubleMu_nume.Clone())
#  histos_nume.append(h_DY_nume.Clone())
#  histos_nume.append(h_WJet_nume.Clone())
#  histos_nume.append(h_TTTo1L_nume.Clone())
  histos_nume.append(h_15to20_nume.Clone())
  histos_nume.append(h_20to30_nume.Clone())
  histos_nume.append(h_30to50_nume.Clone())
  histos_nume.append(h_50to80_nume.Clone())
  histos_nume.append(h_80to120_nume.Clone())
  histos_nume.append(h_120to170_nume.Clone())
  histos_nume.append(h_170to300_nume.Clone())
  histos_nume.append(h_300to470_nume.Clone())
  histos_nume.append(h_470to600_nume.Clone())
  histos_nume.append(h_600to800_nume.Clone())
  histos_nume.append(h_800to1000_nume.Clone())
  histos_nume.append(h_1000toInf_nume.Clone())

  for i in range(0,12):
#  for i in range(0,1):
    histos_deno[i]=overunder_flowbin(histos_deno[i])
    histos_nume[i]=overunder_flowbin(histos_nume[i])

  c1 = plot_fakerate.draw_plots(histos_nume, histos_deno, 0)
  del histos_deno[:]
  del histos_nume[:]
 
if __name__ == "__main__":
  start = time.time()
  start1 = time.clock() 
  Fakerate_Analysis()
  end = time.time()
  end1 = time.clock()
  print "wall time:", end-start
  print "process time:", end1-start1
