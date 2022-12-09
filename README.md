# Lepton_Fakerate

The input ntuples are produced using module 
https://github.com/ExtraYukawa/ttc_bar/blob/lep_mvaID/modules/FakeRateProducer.py, in which the leptons id and corresponding selections are defined.


# Instruction to run the fakerate estimation codes:
```
cmsrel CMSSW_10_6_27
cd CMSSW_10_6_27/src
cmsenv
git clone git@github.com:ExtraYukawa/Lepton_Fakerate.git
```


mu_fr.py/ele_fr.py is used for nominal fakerate calculation.

# For Muon channel
```
cd Lepton_Fakerate/Mu_channel
python mu_fr.py --era 2016APV --saveDir Mu_config1
```

# For Electron channel
```
cd Lepton_Fakerate/Ele_channel
python ele_fr.py --era 2016APV --saveDir Ele_config1
```


The QCD.py is used for MC closuretest (NOT updated recently Probably we need to write another script)
Meng might know better.
