## Fake rate closure test
To run on this project, you need to worked under CMSSW_11_X_X for certain function. (TODO: modify it to be constistent with the rest part of analysis)

Then download the necessary files through,
```
python setup.py
```

To run on 2D fake rate closure test
```
python fakerate_plot2D.py --era [ERA] --channel [CHANNEL] 
```

To run on 1D fake rate closure test
```
python fakerate_plot.py --era [ERA] --channel [CHANNEL]
```
