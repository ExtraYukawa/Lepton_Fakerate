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

def analysis(era, channel,norm):

###################
## Basic Setting ##
###################

  os.system('cat %s | sed "s/EraToBeReplaced/%s/g" > %s'%('script/slim_fake.h',era,'script/slim_fake_%s.h'%era))

  ROOT.gSystem.Load("libGenVector.so")
  TTC_header_path = os.path.join("script/slim_fake_" + era + ".h")
  ROOT.gInterpreter.Declare('#include "{}"'.format(TTC_header_path))

  path = str(inputFile_path[era])

  # Lumi information is stored in plot_TTCregion
  if  (era == '2016apv'): lumi = 1.
  elif(era == '2016postapv'): lumi = 1.
  elif(era == '2017'): lumi = 1.
  else: lumi = 1.
  xsec = 365.4574

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

  if channel == "mm":

    filters="ttc_region==1 && ttc_jets && ttc_l1_pt>30 && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && nHad_tau==0"
    fakeweight_definition = "fake_weight(ttc_region,ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,muon_conePt[ttc_l1_id],ttc_l1_eta,muon_conePt[ttc_l2_id],ttc_l2_eta,0)"
    fakeweight_ele_statUp_definition = "fake_weight(ttc_region,ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,muon_conePt[ttc_l1_id],ttc_l1_eta,muon_conePt[ttc_l2_id],ttc_l2_eta,1)"
    fakeweight_ele_statDo_definition = "fake_weight(ttc_region,ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,muon_conePt[ttc_l1_id],ttc_l1_eta,muon_conePt[ttc_l2_id],ttc_l2_eta,2)"
    fakeweight_mu_statUp_definition = "fake_weight(ttc_region,ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,muon_conePt[ttc_l1_id],ttc_l1_eta,muon_conePt[ttc_l2_id],ttc_l2_eta,3)"
    fakeweight_mu_statDo_definition = "fake_weight(ttc_region,ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,muon_conePt[ttc_l1_id],ttc_l1_eta,muon_conePt[ttc_l2_id],ttc_l2_eta,4)"
    channel_name = 'mm'

  elif channel == "ee":

    filters="ttc_region==3 && ttc_jets && ttc_l1_pt>30 && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && nHad_tau==0 && (ttc_mll<60 || ttc_mll>120)"
    fakeweight_definition = "fake_weight(ttc_region,ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta,0)"
    fakeweight_ele_statUp_definition = "fake_weight(ttc_region,ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta,1)"
    fakeweight_ele_statDo_definition = "fake_weight(ttc_region,ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta,2)"
    fakeweight_mu_statUp_definition = "fake_weight(ttc_region,ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta,3)"
    fakeweight_mu_statDo_definition = "fake_weight(ttc_region,ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta,4)"
    channel_name = 'ee'

  elif channel == "em":
    filters="ttc_region==2 && ttc_jets && (ttc_l1_pt>30 || ttc_l2_pt>30) && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && nHad_tau==0"
    fakeweight_definition = "fake_weight(ttc_region,ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,muon_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta,0)"
    fakeweight_ele_statUp_definition = "fake_weight(ttc_region,ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,muon_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta,1)"
    fakeweight_ele_statDo_definition = "fake_weight(ttc_region,ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,muon_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta,2)"
    fakeweight_mu_statUp_definition = "fake_weight(ttc_region,ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,muon_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta,3)"
    fakeweight_mu_statDo_definition = "fake_weight(ttc_region,ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,muon_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta,4)"
    channel_name = 'em'

  Trigger      = GetTrigger_MC(era)
  MET_filters  = GetMETFilter_MC(era, 'TTTo1L.root')
  filters_mc   = str("(" + filters + ")&&(" + MET_filters + ") && ttc_2P0F")
  filters_fake = str("(" + filters + ")&&(" + MET_filters + ") && ttc_1P1F")
  print(filters)
  print(Trigger)

###################
## Event Process ##
###################

  df_tree = df.Filter(str(Trigger))  
  df_tree = df_tree.Define("fakeweight",str(fakeweight_definition))\
                   .Define("fakeweight_ele_statUp",str(fakeweight_ele_statUp_definition))\
                   .Define("fakeweight_ele_statDo",str(fakeweight_ele_statDo_definition))\
                   .Define("fakeweight_mu_statUp",str(fakeweight_mu_statUp_definition))\
                   .Define("fakeweight_mu_statDo",str(fakeweight_mu_statDo_definition))\
                   .Define("genweight",'puWeight*genWeight/abs(genWeight)')\
                   .Define("l2_conePt",'muon_conePt[ttc_l2_id]')\
                   .Define('fake_id', 'fake_index(ttc_1P1F,ttc_lep1_faketag,ttc_l1_id,ttc_l2_id)')\
                   .Define('ptratio', 'muon_jet_Ptratio[fake_id]')\
                   .Define('mediumID',  'MediumID(Muon_mediumId, fake_id)')\
                   .Define('genPartFlav','Muon_genPartFlav[fake_id]')\
                   .Define('fake_conePt'    , 'muon_conePt[fake_id]')\
                   .Define('fake_iso', 'Muon_miniPFRelIso_all[fake_id]')\
                   .Define('dR_closeJet', 'deltaR_closejet(Jet_pt_nom, Jet_eta, Jet_phi, Jet_mass_nom, Muon_corrected_pt, Muon_eta, Muon_phi, Muon_mass, muon_closest_jetid, fake_id)')\
                   .Define('l1_pt', '(ttc_l1_pt > ttc_l2_pt) ? ttc_l1_pt : ttc_l2_pt')\
                   .Define('l2_pt', '(ttc_l1_pt > ttc_l2_pt) ? ttc_l2_pt : ttc_l1_pt')\
                   .Define('l1_eta','(ttc_l1_pt > ttc_l2_pt) ? ttc_l1_eta : ttc_l2_eta')\
                   .Define('l2_eta','(ttc_l1_pt > ttc_l2_pt) ? ttc_l2_eta : ttc_l1_eta')

  df_tree_TTTo1L      = df_tree.Filter(filters_mc)
  df_tree_TTTo1L_fake = df_tree.Filter(filters_fake)
  df_tree_TTTo1L_fake = df_tree_TTTo1L_fake.Define('fakelepweight','genweight*fakeweight')\
                                           .Define('fakelepweight_ele_statUp','genweight*fakeweight_ele_statUp')\
                                           .Define('fakelepweight_ele_statDo','genweight*fakeweight_ele_statDo')\
                                           .Define('fakelepweight_mu_statUp', 'genweight*fakeweight_mu_statUp')\
                                           .Define('fakelepweight_mu_statDo', 'genweight*fakeweight_mu_statDo')\

###############
## Histogram ##
###############

  ptbin=array('d',[20, 30, 40, 60, 80])
  etabin=array('d',[0, 0.5,1.0,1.5,2.0,2.5])
  lowptbin=array('d', [float(10 + 5*i) for i in range(14)])
  pt_ratio_bin = array('d', [(0.3 + 0.1*i) for i in range(10)])
  mediumID_bin = array('d', [0,1,2])
  genPartFlav_bin  = array('d', [(-0.5 + i*1.0) for i in range(16)])
  iso_bin = array('d', [i*0.05 for i in range(9)])
  dr_bin  = array('d', [i*0.05 for i in range(16)])

  hist_dict = {
    "l1_eta_pt" :["l1_eta", "l1_pt", 5, etabin, 4, ptbin],
    "l2_eta_pt" :["l2_eta", "l2_pt", 5, etabin, 4, ptbin]
#    "conept": ["ttc_l2_pt", "l2_conePt", len(lowptbin)-1, lowptbin, len(lowptbin)-1, lowptbin]
#    "pt_ratioVSID": ["mediumID", "ptratio", len(mediumID_bin)-1, mediumID_bin, len(pt_ratio_bin)-1, pt_ratio_bin],
#    "flavVSID": ["genPartFlav", "ptratio", len(genPartFlav_bin)-1, genPartFlav_bin, len(pt_ratio_bin)-1, pt_ratio_bin],
#    "conePtVspt_ratio": ["fake_conePt", "ptratio", len(lowptbin)-1, lowptbin, len(pt_ratio_bin)-1, pt_ratio_bin],
#    "isovspt_ratio": ["fake_iso", "ptratio", len(iso_bin)-1, iso_bin, len(pt_ratio_bin)-1, pt_ratio_bin]
#   "drvspt_ratio": ["dR_closeJet", "ptratio", len(dr_bin)-1, dr_bin, len(pt_ratio_bin)-1, pt_ratio_bin]
  }

  unc_dict = dict()

  c = ROOT.TCanvas()

  for hist in hist_dict:
    histos = []
    histo = hist_dict[hist]
    unc      = 0.
    unc_nbin = 0.

    h_TTTo1L                = get_hist2D(df_tree_TTTo1L,      hist, histo, 'genweight', norm)
    h_TTTo1L_fake           = get_hist2D(df_tree_TTTo1L_fake, hist, histo, 'fakelepweight', norm)
    h_TTTo1L_fake_eleStatUp = get_hist2D(df_tree_TTTo1L_fake, hist, histo, 'fakelepweight_ele_statUp', norm)
    h_TTTo1L_fake_eleStatDo = get_hist2D(df_tree_TTTo1L_fake, hist, histo, 'fakelepweight_ele_statDo', norm)
    h_TTTo1L_fake_muStatUp  = get_hist2D(df_tree_TTTo1L_fake, hist, histo, 'fakelepweight_mu_statUp', norm)
    h_TTTo1L_fake_muStatDo  = get_hist2D(df_tree_TTTo1L_fake, hist, histo, 'fakelepweight_mu_statDo', norm)

    h_TTTo1L_fake_eleStatUp.Add(h_TTTo1L_fake_eleStatDo,-1.)
    h_TTTo1L_fake_muStatUp.Add(h_TTTo1L_fake_muStatDo,-1.)
    h_intrinsic_syst = h_TTTo1L_fake.Clone()
    h_FakeRate_syst  = h_TTTo1L_fake.Clone()
    h_diff = h_TTTo1L.Clone()

    for i in range(histo[2]):
      for j in range(histo[4]):
        FR_eleStat = h_TTTo1L_fake_eleStatUp.GetBinContent(i+1, j+1)
        FR_muStat  = h_TTTo1L_fake_muStatUp.GetBinContent(i+1, j+1)
        FR_Stat    = sqrt(FR_eleStat**2 + FR_muStat**2)
        Nevt_mc    = h_TTTo1L.GetBinContent(i+1, j+1)
        Nevt_fake  = h_TTTo1L_fake.GetBinContent(i+1, j+1)
        diff       = abs(Nevt_mc - Nevt_fake)
        Bin_Stat   = sqrt(Nevt_fake)
        if Nevt_fake > 0:
          intrinsic_syst = sqrt(max(diff**2 - (Bin_Stat/2.)**2 - (FR_Stat/2.)**2,0))/Nevt_fake + 0.0001
          h_intrinsic_syst.SetBinContent(i+1, j+1, intrinsic_syst)
          h_FakeRate_syst.SetBinContent(i+1,  j+1, sqrt((FR_Stat/2.)**2 + (Bin_Stat/2.)**2)/Nevt_fake)
          unc      += intrinsic_syst * Nevt_fake
          unc_nbin += Nevt_fake
        else:
          h_intrinsic_syst.SetBinContent(i+1, j+1, 1)
          h_FakeRate_syst.SetBinContent(i+1,  j+1, 0)
          intrinsic_syst = 0.
     

    if unc_nbin>0:
      unc = unc/unc_nbin
    else:
      unc = 0.0
    unc_dict[hist] = unc
    print(era, channel, hist + ": " + str(unc))


    tag = ""
    if norm:
      tag = "_norm"
 
    h_TTTo1L.Draw("COLZ TEXT")
    c.SaveAs("plot/" + era + "/" + hist + "_" + channel + "2D_mc" + tag + ".png")
    h_TTTo1L_fake.Draw("COLZ TEXT")
    c.SaveAs("plot/" + era + "/" + hist + "_" + channel + "2D_fake" + tag + ".png")
    h_intrinsic_syst.Draw("COLZ TEXT")
    c.SaveAs("plot/" + era + "/" + hist + "_" + channel + "2D_unc" + tag + ".png")

  with open("result/FR_systematic2D_"+era+"_"+channel+".json", "w") as write_file:
    json.dump(unc_dict, write_file, indent=4)


if __name__ == "__main__":
  start  = time.time()
  start1 = time.clock()

  usage = 'usage: %prog [options]'
  parser = argparse.ArgumentParser(description=usage)
  parser.add_argument('-e','--era',dest='era',default='2018',type=str)
  parser.add_argument('-c','--channel',dest='channel',default='ee',type=str)
  parser.add_argument("--norm", action="store_true")
  args = parser.parse_args()

#  analysis(args.era, args.channel,args.norm)
  for ERA in ['2016postapv']:#,'2016postapv','2017','2018']:
    for CHANNEL in ['ee','em','mm']:
      analysis(ERA,CHANNEL,False)
