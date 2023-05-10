import ROOT
import time
import os
import math
import json
from math import sqrt
from array import array
import optparse, argparse
from common import inputFile_path, GetTrigger_MC, GetMETFilter_MC, get_mcEventnumber, overunder_flowbin, get_hist2D
import plot_TTCregion
import numpy as np

ROOT.gROOT.SetBatch(True)

def analysis(era, channel, norm):

###################
## Basic Setting ##
###################

  os.system('cat %s | sed "s/EraToBeReplaced/%s/g" > %s'%('script/slim_fake.h',era,'script/slim_fake_%s.h'%era))

  ROOT.gSystem.Load("libGenVector.so")
  TTC_header_path = os.path.join("script/slim_fake_" + era + ".h")
  ROOT.gInterpreter.Declare('#include "{}"'.format(TTC_header_path))

  path = str("/eos/cms/store/group/phys_top/ExtraYukawa/Fakerate_dataset_looseFake/2017/")

  # Lumi information is stored in plot_TTCregion
  if  (era == '2016apv'): lumi = 1.
  elif(era == '2016postapv'): lumi = 1.
  elif(era == '2017'): lumi = 1.
  else: lumi = 1.
#  xsec = 365.4574

##########
## READ ##
##########

  f_list = ROOT.std.vector('string')()
  f_list.push_back(path + "TTTo1L.root")
  ev = get_mcEventnumber(f_list)

  filters = ""
  df = ROOT.RDataFrame("Events", f_list)

############
## Filter ##
############

  filters_fake   = "n_fakeable_muon==1 && met<30 && mt<30 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && jet_selection_30" 
  filters_prompt = "n_tight_muon==1 && met<30 && mt<30 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter &&     Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter &&  Flag_eeBadScFilter && Flag_ecalBadCalibFilter && jet_selection_30"
###################
## Event Process ##
###################

  df             = df.Define("genweight","puWeight*PrefireWeight*genWeight/abs(genWeight)")

  df_tree_prompt = df.Filter(str(filters_prompt))
  df_tree_prompt = df_tree_prompt.Define("pt_ratio_prompt", "muon_jet_Ptratio[tightMuons_id[0]]")\
                                 .Define("mediumID_prompt", "MediumID(Muon_mediumId, tightMuons_id[0])")\
                                 .Define("genPartFlav_prompt", "Muon_genPartFlav[tightMuons_id[0]]")\
                                 .Define("miniIso_prompt", "Muon_miniPFRelIso_all[tightMuons_id[0]]")\
                                 .Define('dR_closeJet_prompt', 'deltaR_closejet(Jet_pt_nom, Jet_eta, Jet_phi, Jet_mass_nom, Muon_corrected_pt, Muon_eta, Muon_phi, Muon_mass, muon_closest_jetid, tightMuons_id[0])')\
                                 .Define('conePt_prompt' , 'l1_pt')

  df_tree_fake   = df.Filter(str(filters_fake))
  df_tree_fake   = df_tree_fake.Define("pt_ratio_fake", "muon_jet_Ptratio[fakeable_Muons_id[0]]")\
                               .Define("mediumID_fake", "MediumID(Muon_mediumId, fakeable_Muons_id[0])")\
                               .Define("genPartFlav_fake","Muon_genPartFlav[fakeable_Muons_id[0]]")\
                               .Define("miniIso_fake", "Muon_miniPFRelIso_all[fakeable_Muons_id[0]]")\
                               .Define('dR_closeJet_fake', 'deltaR_closejet(Jet_pt_nom, Jet_eta, Jet_phi, Jet_mass_nom, Muon_corrected_pt, Muon_eta, Muon_phi, Muon_mass, muon_closest_jetid, fakeable_Muons_id[0])')\
                               .Define('conePt_fake', 'l1_pt')

###############
## Histogram ##
###############

  ptbin=array('d',[20, 30, 40, 60, 80])
  etabin=array('d',[0, 0.5,1.0,1.5,2.0,2.5])
#  fakeweightbin = array('d',[-5,-3, -1, 1, 3, 5])
  lowptbin=array('d', [float(10 + 5*i) for i in range(14)])
  pt_ratio_bin = array('d', [(0.3 + 0.1*i) for i in range(10)])
  mediumID_bin = array('d', [0,1,2])
  genPartFlav_bin  = array('d', [(-0.5 + i*1.0) for i in range(16)])
  iso_bin = array('d', [i*0.05 for i in range(9)])
  dr_bin  = array('d', [i*0.05 for i in range(16)])


#  print(fakeweightbin)
  print(lowptbin)

  hist_dict = {
#    "pt_ratio": ["mediumID_TYPE", "pt_ratio_TYPE", len(mediumID_bin)-1, mediumID_bin, len(pt_ratio_bin)-1, pt_ratio_bin],
#    "flavVSpt": ["genPartFlav_TYPE","pt_ratio_TYPE", len(genPartFlav_bin)-1, genPartFlav_bin, len(pt_ratio_bin)-1, pt_ratio_bin],
#    "isoVsPtratio": ["miniIso_TYPE", "pt_ratio_TYPE", len(iso_bin)-1, iso_bin, len(pt_ratio_bin)-1, pt_ratio_bin]
#   "drvspt_ratio": ["dR_closeJet_TYPE", "pt_ratio_TYPE", len(dr_bin)-1, dr_bin, len(pt_ratio_bin)-1, pt_ratio_bin]
    "conePtVspt_ratio": ["conePt_TYPE", "pt_ratio_TYPE", len(lowptbin)-1, lowptbin, len(pt_ratio_bin)-1, pt_ratio_bin]
  }


  c = ROOT.TCanvas()

  for hist in hist_dict:

    histo = hist_dict[hist]

    histo[0] = histo[0].replace("TYPE", "prompt")
    histo[1] = histo[1].replace("TYPE", "prompt")
    print(histo)
    h_prompt = get_hist2D(df_tree_prompt, hist, histo, 'genweight', norm)

    histo[0] = histo[0].replace("prompt", "fake")
    histo[1] = histo[1].replace("prompt", "fake")
    print(histo)
    h_fake   = get_hist2D(df_tree_fake,   hist, histo, 'genweight', norm)
 

    tag = ""
    if norm:
      tag = "_norm"
    h_prompt.Draw("COLZ TEXT")
    c.SaveAs("plot_TTTo1L_mea/" + hist + "_" + "2D_prompt" + tag + ".png")
    h_fake.Draw("COLZ TEXT")
    c.SaveAs("plot_TTTo1L_mea/" + hist + "_" + "2D_fake" + tag + ".png")


if __name__ == "__main__":
  start  = time.time()
  start1 = time.clock()

  usage = 'usage: %prog [options]'
  parser = argparse.ArgumentParser(description=usage)
  parser.add_argument('-e','--era',dest='era',default='2018',type=str)
  parser.add_argument('-c','--channel',dest='channel',default='ee',type=str)
  parser.add_argument("--norm", action="store_true")
  args = parser.parse_args()


  analysis(args.era, args.channel, args.norm)
#  for ERA in ['2016apv','2016postapv','2017','2018']:
#    for CHANNEL in ['ee','em','mm']:
#      analysis(ERA,CHANNEL)
