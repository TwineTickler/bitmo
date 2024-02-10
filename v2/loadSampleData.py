# This is only used for my personal testing and debug purposes. 
# This is not used by the program at all.
# This allows me to load in a sample API response directly into the python console.
#
# TO USE type this in python console type these two lines:
#
#   import loadSampleData as LSD
#   q = LSD.loadData()
#
#   q is now assigned the dictionary that holds a valid API response

import config
import json

def loadData():

    f = open('{}/sampleData.json'.format(config.absolutePath))
    data = json.load(f)

    return data