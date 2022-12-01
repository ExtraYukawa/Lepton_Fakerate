import ROOT
import numpy as np
from ROOT import kFALSE
import datetime
import os, sys
sys.path.append('../python')

import CMSTDRStyle
CMSTDRStyle.setTDRStyle().cd()
import CMSstyle
from array import array

def draw_plots(opts, hist_nume =[], hist_deno =[], data=1):

	if data:
	  h_data_denominator=hist_deno[0]
	  h_DY_denominator=hist_deno[1]
	  h_WJet_denominator=hist_deno[2]
	  h_TTTo1L_denominator=hist_deno[3]
	  h_TTTo2L_denominator=hist_deno[4]

	  h_data_numerator=hist_nume[0]
	  h_DY_numerator=hist_nume[1]
	  h_WJet_numerator=hist_nume[2]
	  h_TTTo1L_numerator=hist_nume[3]
	  h_TTTo2L_numerator=hist_nume[4]
	
	else:
	  h_QCD15to20_deno=hist_deno[0]
	  h_QCD20to30_deno=hist_deno[1]
	  h_QCD30to50_deno=hist_deno[2]
	  h_QCD50to80_deno=hist_deno[3]
	  h_QCD80to120_deno=hist_deno[4]
	  h_QCD120to170_deno=hist_deno[5]
	  h_QCD170to300_deno=hist_deno[6]
	  h_QCD300toInf_deno=hist_deno[7]
	  h_bctoe_QCD15to20_deno=hist_deno[8]
	  h_bctoe_QCD20to30_deno=hist_deno[9]
	  h_bctoe_QCD30to80_deno=hist_deno[10]
	  h_bctoe_QCD80to170_deno=hist_deno[11]
	  h_bctoe_QCD170to250_deno=hist_deno[12]
	  h_bctoe_QCD250toInf_deno=hist_deno[13]

	  h_QCD15to20_nume=hist_nume[0]
	  h_QCD20to30_nume=hist_nume[1]
	  h_QCD30to50_nume=hist_nume[2]
	  h_QCD50to80_nume=hist_nume[3]
	  h_QCD80to120_nume=hist_nume[4]
	  h_QCD120to170_nume=hist_nume[5]
	  h_QCD170to300_nume=hist_nume[6]
	  h_QCD300toInf_nume=hist_nume[7]
	  h_bctoe_QCD15to20_nume=hist_nume[8]
	  h_bctoe_QCD20to30_nume=hist_nume[9]
	  h_bctoe_QCD30to80_nume=hist_nume[10]
	  h_bctoe_QCD80to170_nume=hist_nume[11]
	  h_bctoe_QCD170to250_nume=hist_nume[12]
	  h_bctoe_QCD250toInf_nume=hist_nume[13]

        # save all output inside a directory
        if opts.saveDir == None:
                opts.saveDir = '%s_%s_%s' % ("Ele_FR", opts.era, datetime.datetime.now().strftime("%d%b%YT%H%M"))

        if not os.path.exists(opts.saveDir):
                print ("save direcotry does not exits! so creating", opts.saveDir)
                os.mkdir(opts.saveDir)

        fileo1 = ROOT.TFile(opts.saveDir+'/histos_ele_'+opts.era+'.root', 'RECREATE')
	fileo1.cd()
        
	if data:
	  h_data_denominator.Write()
	  h_DY_denominator.Write()
	  h_WJet_denominator.Write()
	  h_TTTo1L_denominator.Write()
	  h_TTTo2L_denominator.Write()
	  h_data_numerator.Write()
	  h_DY_numerator.Write()
	  h_WJet_numerator.Write()
	  h_TTTo1L_numerator.Write()
	  h_TTTo2L_numerator.Write()
	
	else:
	  h_QCD15to20_deno.Write()
	  h_QCD20to30_deno.Write()
	  h_QCD30to50_deno.Write()
	  h_QCD50to80_deno.Write()
	  h_QCD80to120_deno.Write()
	  h_QCD120to170_deno.Write()
	  h_QCD170to300_deno.Write()
	  h_QCD300toInf_deno.Write()
	  h_bctoe_QCD15to20_deno.Write()
	  h_bctoe_QCD20to30_deno.Write()
	  h_bctoe_QCD30to80_deno.Write()
	  h_bctoe_QCD80to170_deno.Write()
	  h_bctoe_QCD170to250_deno.Write()
	  h_bctoe_QCD250toInf_deno.Write()
	  h_QCD15to20_nume.Write()
	  h_QCD20to30_nume.Write()
	  h_QCD30to50_nume.Write()
	  h_QCD50to80_nume.Write()
	  h_QCD80to120_nume.Write()
	  h_QCD120to170_nume.Write()
	  h_QCD170to300_nume.Write()
	  h_QCD300toInf_nume.Write()
	  h_bctoe_QCD15to20_nume.Write()
	  h_bctoe_QCD20to30_nume.Write()
	  h_bctoe_QCD30to80_nume.Write()
	  h_bctoe_QCD80to170_nume.Write()
	  h_bctoe_QCD170to250_nume.Write()
	  h_bctoe_QCD250toInf_nume.Write()
	fileo1.Close()

	c1 = ROOT.TCanvas('','',800,600)
	pad = ROOT.TPad()
	pad.Draw()

	if data:
	  h_nume=h_data_numerator.Clone()
	  h_nume.Add(h_DY_numerator)
	  h_nume.Add(h_WJet_numerator)
	  h_nume.Add(h_TTTo1L_numerator)
	  h_nume.Add(h_TTTo2L_numerator)
	  
	  h_deno=h_data_denominator.Clone()
	  h_deno.Add(h_DY_denominator)
	  h_deno.Add(h_WJet_denominator)
	  h_deno.Add(h_TTTo1L_denominator)
	  h_deno.Add(h_TTTo2L_denominator)

	else:
	  h_nume=h_QCD15to20_nume.Clone()
	  h_nume.Add(h_QCD20to30_nume)
	  h_nume.Add(h_QCD30to50_nume)
	  h_nume.Add(h_QCD50to80_nume)
	  h_nume.Add(h_QCD80to120_nume)
	  h_nume.Add(h_QCD120to170_nume)
	  h_nume.Add(h_QCD170to300_nume)
	  h_nume.Add(h_QCD300toInf_nume)
	  h_nume.Add(h_bctoe_QCD15to20_nume)
	  h_nume.Add(h_bctoe_QCD20to30_nume)
	  h_nume.Add(h_bctoe_QCD30to80_nume)
	  h_nume.Add(h_bctoe_QCD80to170_nume)
	  h_nume.Add(h_bctoe_QCD170to250_nume)
	  h_nume.Add(h_bctoe_QCD250toInf_nume)

	  h_deno=h_QCD15to20_deno.Clone()
	  h_deno.Add(h_QCD20to30_deno)
	  h_deno.Add(h_QCD30to50_deno)
	  h_deno.Add(h_QCD50to80_deno)
	  h_deno.Add(h_QCD80to120_deno)
	  h_deno.Add(h_QCD120to170_deno)
	  h_deno.Add(h_QCD170to300_deno)
	  h_deno.Add(h_QCD300toInf_deno)
	  h_deno.Add(h_bctoe_QCD20to30_deno)
	  h_deno.Add(h_bctoe_QCD15to20_deno)
	  h_deno.Add(h_bctoe_QCD30to80_deno)
	  h_deno.Add(h_bctoe_QCD80to170_deno)
	  h_deno.Add(h_bctoe_QCD170to250_deno)
	  h_deno.Add(h_bctoe_QCD250toInf_deno)

	h_nume.SetName('fakerate')
	h_nume.GetXaxis().SetTitle("#||{#eta}")
	h_nume.GetYaxis().SetTitle("cone-P_{T} [GeV]")
	h_nume.GetXaxis().SetTitleSize(0.05)
	h_nume.GetYaxis().SetTitleSize(0.05)
	h_nume.Divide(h_deno)
	h_nume.Draw('COL TEXT E')

	fileout = ROOT.TFile(opts.saveDir+'/fr_data_ele_'+opts.era+'.root', 'RECREATE')
	#fileout = ROOT.TFile('fr.root', 'RECREATE')
	fileout.cd()
	h_nume.Write()
	fileout.Close()


	CMSstyle.SetStyle(pad, opts.era)
	pad.SetRightMargin(0.15)
	c1.SetGridx(False);
	c1.SetGridy(False);
	c1.Update()
	c1.SaveAs(opts.saveDir+'/fakerate_data_ele_'+opts.era+'.pdf')
	c1.SaveAs(opts.saveDir+'/fakerate_data_ele_'+opts.era+'.png')
	#c1.SaveAs('fakerate.pdf')
	#c1.SaveAs('fakerate.png')
	return c1
	pad.Close()
	del hist_nume
	del hist_deno
