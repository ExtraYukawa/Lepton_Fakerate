#ifndef SLIM_FAKE_EraToBeReplaced_H
#define SLIM_FAKE_EraToBeReplaced_H

#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "TCanvas.h"
#include "TH1D.h"
#include "TLatex.h"
#include "Math/Vector4D.h"
#include "TStyle.h"
#include "TString.h"

using namespace ROOT;
using namespace std;
using namespace ROOT::VecOps;

TString era = "EraToBeReplaced";


TFile*f_mu=TFile::Open("./data/fr_data_mu_"+era+".root");
TFile*f_ele=TFile::Open("./data/fr_data_ele_"+era+".root");


TH2D*h_m=(TH2D*)f_mu->Get("fakerate");
TH2D*h_e=(TH2D*)f_ele->Get("fakerate");

float fake_weight(int ttc_region, bool ttc_1P1F, bool ttc_0P2F, bool ttc_lep1_faketag, float l1_pt, float l1_eta, float l2_pt, float l2_eta, int iw){
  if (l1_pt>70.) l1_pt=70.;
  if (l2_pt>70.) l2_pt=70.;
  if (fabs(l1_eta)>2.3) l1_eta=2.3;
  if (fabs(l2_eta)>2.3) l2_eta=2.3;
  float w_temp=1.0;
  float fakerate1=1.0;
  float fakerate2=1.0;
  float sigma_e = 0.0;
  float sigma_m = 0.0;
  // iw = 0: nominal, 1: Electron_StatUp, 2: Electron_StatDown, 3: Muon_StatUp, 4: Muon_StatDown
  if(iw == 1)      sigma_e =  1.0;
  else if(iw == 2) sigma_e = -1.0;
  else if(iw == 3) sigma_m =  1.0;
  else if(iw == 4) sigma_m = -1.0;

  if (ttc_region==1){
    if(ttc_1P1F){
      if(ttc_lep1_faketag) fakerate1 = h_m->GetBinContent(h_m->FindBin(fabs(l1_eta), l1_pt)) + sigma_m*h_m->GetBinError(h_m->FindBin(fabs(l1_eta), l1_pt));
      else fakerate1 = h_m->GetBinContent(h_m->FindBin(fabs(l2_eta), l2_pt)) + sigma_m*h_m->GetBinError(h_m->FindBin(fabs(l2_eta), l2_pt));
      w_temp = fakerate1/(1-fakerate1);
    }
    if(ttc_0P2F){
          fakerate1 = h_m->GetBinContent(h_m->FindBin(fabs(l1_eta), l1_pt)) + sigma_m*h_m->GetBinError(h_m->FindBin(fabs(l1_eta), l1_pt));
          fakerate2 = h_m->GetBinContent(h_m->FindBin(fabs(l2_eta), l2_pt)) + sigma_m*h_m->GetBinError(h_m->FindBin(fabs(l2_eta), l2_pt));
          w_temp = -1.*fakerate1*fakerate2/((1-fakerate1)*(1-fakerate2));
    }
  }
  if (ttc_region==2){
    if(ttc_1P1F){
      if(ttc_lep1_faketag) fakerate1 = h_m->GetBinContent(h_m->FindBin(fabs(l1_eta), l1_pt)) + sigma_m*h_m->GetBinError(h_m->FindBin(fabs(l1_eta), l1_pt));
      else fakerate1 = h_e->GetBinContent(h_e->FindBin(fabs(l2_eta), l2_pt)) + sigma_e*h_e->GetBinError(h_e->FindBin(fabs(l2_eta), l2_pt));
      w_temp = fakerate1/(1-fakerate1);
    }
    if(ttc_0P2F){
          fakerate1 = h_m->GetBinContent(h_m->FindBin(fabs(l1_eta), l1_pt)) + sigma_m*h_m->GetBinError(h_m->FindBin(fabs(l1_eta), l1_pt));
          fakerate2 = h_e->GetBinContent(h_e->FindBin(fabs(l2_eta), l2_pt)) + sigma_e*h_e->GetBinError(h_e->FindBin(fabs(l2_eta), l2_pt));
          w_temp = -1.*fakerate1*fakerate2/((1-fakerate1)*(1-fakerate2));
    }
  }
  if (ttc_region==3){
    if(ttc_1P1F){
      if(ttc_lep1_faketag) fakerate1 = h_e->GetBinContent(h_e->FindBin(fabs(l1_eta), l1_pt)) + sigma_e*h_e->GetBinError(h_e->FindBin(fabs(l1_eta), l1_pt));
      else fakerate1 = h_e->GetBinContent(h_e->FindBin(fabs(l2_eta), l2_pt)) + sigma_e*h_e->GetBinError(h_e->FindBin(fabs(l2_eta), l2_pt));
      w_temp = fakerate1/(1-fakerate1);
    }
    if(ttc_0P2F){
          fakerate1 = h_e->GetBinContent(h_e->FindBin(fabs(l1_eta), l1_pt)) + sigma_e*h_e->GetBinError(h_e->FindBin(fabs(l1_eta), l1_pt));
          fakerate2 = h_e->GetBinContent(h_e->FindBin(fabs(l2_eta), l2_pt)) + sigma_e*h_e->GetBinError(h_e->FindBin(fabs(l2_eta), l2_pt));
          w_temp = -1.*fakerate1*fakerate2/((1-fakerate1)*(1-fakerate2));
    }
  }
  return w_temp;
}



float deltaR_jet( ROOT::VecOps::RVec<float> jet_pt, ROOT::VecOps::RVec<float> jet_eta, ROOT::VecOps::RVec<float> jet_phi, ROOT::VecOps::RVec<float> jet_mass, ROOT::VecOps::RVec<Int_t> jet_id, int id)
{
  float deltar=0.;
  ROOT::Math::PtEtaPhiMVector j1(jet_pt[jet_id[0]],jet_eta[jet_id[0]],jet_phi[jet_id[0]],jet_mass[jet_id[0]]);
  ROOT::Math::PtEtaPhiMVector j2(jet_pt[jet_id[1]],jet_eta[jet_id[1]],jet_phi[jet_id[1]],jet_mass[jet_id[1]]);
  ROOT::Math::PtEtaPhiMVector j3(jet_pt[jet_id[2]],jet_eta[jet_id[2]],jet_phi[jet_id[2]],jet_mass[jet_id[2]]);
  if(id==1) deltar= ROOT::Math::VectorUtil::DeltaR(j1,j2);
  if(id==2) deltar= ROOT::Math::VectorUtil::DeltaR(j1,j3);
  if(id==3) deltar= ROOT::Math::VectorUtil::DeltaR(j2,j3);
  return deltar;
}

bool Triggers(int run, bool triggers, std::vector<int> vec){
    if(!triggers || vec.at(0) == -1 ){
        return triggers;
    }
    for(auto v : vec){
        if(run == v){
            return triggers;
        }
    }
    return false;
}

int fake_index(bool ttc_1P1F, bool ttc_lep1_faketag, int ttc_l1_id, int ttc_l2_id)
{
  if (!ttc_1P1F)              return 0;
  else{
    if (ttc_lep1_faketag) return ttc_l1_id;
    else                  return ttc_l2_id;
  } 
}

float deltaR_closejet(ROOT::VecOps::RVec<float> jet_pt, ROOT::VecOps::RVec<float> jet_eta, ROOT::VecOps::RVec<float> jet_phi, ROOT::VecOps::RVec<float> jet_mass, ROOT::VecOps::RVec<float> muon_pt, ROOT::VecOps::RVec<float> muon_eta, ROOT::VecOps::RVec<float> muon_phi, ROOT::VecOps::RVec<float> muon_mass, ROOT::VecOps::RVec<int>  muon_closest_jetid, int muon_id)
{
  int jet_id = muon_closest_jetid[muon_id];
  if (jet_id == -1) return 99;
  else{
    ROOT::Math::PtEtaPhiMVector j1(jet_pt[jet_id],jet_eta[jet_id],jet_phi[jet_id],jet_mass[jet_id]);
    ROOT::Math::PtEtaPhiMVector m1(muon_pt[muon_id],muon_eta[muon_id],muon_phi[muon_id],muon_mass[muon_id]);
    float deltar= ROOT::Math::VectorUtil::DeltaR(j1,m1);
    return deltar;
  }
}

#endif
