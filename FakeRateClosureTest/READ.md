## Fake rate closure test
To run on this project, you need to worked under CMSSW_11_X_X for certain function.
```
cmsrel CMSSW_11_1_2_patch3
cd CMSSW_11_1_2_patch3/src
cmsenv
git clone 
```

To run on 2D fake rate closure test
```
python fakerate_plot2D.py --era [ERA] --channel [CHANNEL] 
```

To run on 1D fake rate closure test
```
python fakerate_plot.py --era [ERA] --channel [CHANNEL]
```
