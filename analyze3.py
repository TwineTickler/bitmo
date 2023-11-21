#
#
#   


import validRecords as vr

validRecords = vr.findValidRecords()

for k, v in validRecords.items():
    print('KEY: {} VALUE: {}'.format(k, v))