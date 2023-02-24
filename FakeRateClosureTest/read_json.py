import json
from collections import OrderedDict
import os

ERA = ["2016apv", "2016postapv", "2017", "2018"]
CHANNEL = ["ee", "em", "mm"]

for era in ERA:
  for channel in CHANNEL:
    jsonfile = open(os.path.join('result/FR_systematic2D_' + era + '_' + channel + '.json'))
    samples  = json.load(jsonfile, encoding='utf-8', object_pairs_hook=OrderedDict).items()
    jsonfile.close()
    for name, desc in samples:
      print(era, channel,str(name), desc)

