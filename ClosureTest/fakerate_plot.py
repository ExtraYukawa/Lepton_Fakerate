import ROOT
import time
import os
import math
import json
from math import sqrt
import optparse
from common import inputFile_path, GetTrigger_MC, GetMETFilter_MC, get_mcEventnumber, overunder_flowbin, get_hist
import plot_TTCregion

ROOT.gROOT.SetBatch(True)

def analysis(era, channel):

###################
## Basic Setting ##
###################

  os.system('cat %s | sed "s/EraToBeReplaced/%s/g" > %s'%('script/slim_fake.h',era,'script/slim_fake_%s.h'%era))
  os.system('mkdir -p plot/%s'%era)


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
                   .Define('l1_pt', '(ttc_l1_pt > ttc_l2_pt) ? ttc_l1_pt : ttc_l2_pt')\
                   .Define('l2_pt', '(ttc_l1_pt > ttc_l2_pt) ? ttc_l2_pt : ttc_l1_pt')\
                   .Define('l1_eta','(ttc_l1_pt > ttc_l2_pt) ? ttc_l1_eta : ttc_l2_eta')\
                   .Define('l2_eta','(ttc_l1_pt > ttc_l2_pt) ? ttc_l2_eta : ttc_l1_eta')
  if (era == '2018'):
    df_tree = df_tree.Define("genweight",'puWeight*genWeight/abs(genWeight)')
  else:
    df_tree = df_tree.Define("genweight",'puWeight*PrefireWeight*genWeight/abs(genWeight)')
  df_tree_TTTo1L      = df_tree.Filter(filters_mc)
  df_tree_TTTo1L_fake = df_tree.Filter(filters_fake)
  df_tree_TTTo1L_fake = df_tree_TTTo1L_fake.Define('fakelepweight','genweight*fakeweight')\
                                           .Define('fakelepweight_ele_statUp','genweight*fakeweight_ele_statUp')\
                                           .Define('fakelepweight_ele_statDo','genweight*fakeweight_ele_statDo')\
                                           .Define('fakelepweight_mu_statUp', 'genweight*fakeweight_mu_statUp')\
                                           .Define('fakelepweight_mu_statDo', 'genweight*fakeweight_mu_statDo')


###############
## Histogram ##
###############

  hist_dict = {
    "l1_pt" :[0,200,20],
    "l2_pt" :[0,200,20],
    "l1_eta":[-2.5,2.5,20],
    "l2_eta":[-2.5,2.5,20]
  }

  unc_dict = dict()

  for hist in hist_dict:
    print(hist)
    histos = []
    histo = hist_dict[hist]
    unc      = 0.
    unc_nbin = 0.

    h_TTTo1L      = get_hist(df_tree_TTTo1L, hist, histo, 'genweight')
    h_TTTo1L_fake = get_hist(df_tree_TTTo1L_fake, hist, histo, 'fakelepweight')
    h_TTTo1L_fake_eleStatUp = get_hist(df_tree_TTTo1L_fake, hist, histo, 'fakelepweight_ele_statUp')
    h_TTTo1L_fake_eleStatDo = get_hist(df_tree_TTTo1L_fake, hist, histo, 'fakelepweight_ele_statDo')
    h_TTTo1L_fake_muStatUp  = get_hist(df_tree_TTTo1L_fake, hist, histo, 'fakelepweight_mu_statUp')
    h_TTTo1L_fake_muStatDo  = get_hist(df_tree_TTTo1L_fake, hist, histo, 'fakelepweight_mu_statDo')

    h_TTTo1L_fake_eleStatUp.Add(h_TTTo1L_fake_eleStatDo,-1.)
    h_TTTo1L_fake_muStatUp.Add(h_TTTo1L_fake_muStatDo,-1.)
    h_intrinsic_syst = h_TTTo1L_fake.Clone()
    h_FakeRate_syst  = h_TTTo1L_fake.Clone()
    h_diff = h_TTTo1L.Clone()

    for i in range(histo[2]):
      FR_eleStat = h_TTTo1L_fake_eleStatUp.GetBinContent(i+1)
      FR_muStat  = h_TTTo1L_fake_muStatUp.GetBinContent(i+1)
      FR_Stat    = sqrt(FR_eleStat**2 + FR_muStat**2)
      Nevt_mc    = h_TTTo1L.GetBinContent(i+1)
      Nevt_fake  = h_TTTo1L_fake.GetBinContent(i+1)
      diff       = abs(Nevt_mc - Nevt_fake)
      Bin_Stat   = sqrt(Nevt_fake)
      if Nevt_fake > 0:
        intrinsic_syst = sqrt(max(diff**2 - (Bin_Stat)**2 - (FR_Stat/2.)**2,0))/Nevt_fake
        h_intrinsic_syst.SetBinContent(i+1, intrinsic_syst)
        h_FakeRate_syst.SetBinContent(i+1, sqrt((FR_Stat/2.)**2 + (Bin_Stat)**2)/Nevt_fake)
        unc      += intrinsic_syst * Nevt_fake
        unc_nbin += Nevt_fake
      else:
        h_intrinsic_syst.SetBinContent(i+1, Nevt_mc)
        h_FakeRate_syst.SetBinContent(i+1, 0)

    if unc_nbin>0:
      unc = unc/unc_nbin # Note this is only 1D unc. We will use more dedicated one in 2D for the final purpose --> See fakerate_plot2D.py
    else:
      unc = 0.0
    unc_dict[hist] = unc
 
    histos.append(h_TTTo1L)
    histos.append(h_TTTo1L_fake)
    for i in range(len(histos)):
     histos[i].Scale(lumi*xsec/ev)
#     histos[i] = overunder_flowbin(histos[i])
    c1 = plot_TTCregion.draw_plots(histos, 1, hist ,0, h_FakeRate_syst, h_intrinsic_syst, era, channel)
    del histos[:]  

  with open("FR_systematic_"+era+"_"+channel+".json", "w") as write_file:
    json.dump(unc_dict, write_file, indent=4)


if __name__ == "__main__":
  start  = time.time()
  start1 = time.clock()

  usage = 'usage: %prog [options]'
  parser = optparse.OptionParser(usage)
  parser.add_option('-e','--era',dest='era',default='2017',type='string')
  parser.add_option('-c','--channel',dest='channel',default='mm',type='string')
  (args,opt) = parser.parse_args()

  analysis(args.era, args.channel)
#  for ERA in ['2016postapv']:#,'2016postapv','2017','2018']:
#    for CHANNEL in ['ee','em','mm']:
#      analysis(ERA,CHANNEL)
