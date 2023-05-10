## Fake rate closure test
To set up the environment and download necessary files.
```
python setup.py
```

To run on 2D fake rate closure test (The one used for extract uncertainty)
```
python fakerate_plot2D.py --era [ERA] --channel [CHANNEL] 
```

To run on 1D fake rate closure test (The one used fore demonstration plot)
```
python fakerate_plot.py --era [ERA] --channel [CHANNEL]
```

To summarize the uncertainty
```
python read_json.py 
```
