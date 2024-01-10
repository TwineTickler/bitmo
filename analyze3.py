#
#
#   
#   Here are some ideas of how we can experiment with this analyses:
#
#   For example:
#      How do the top 200 coins behave if Bitcoins moves up by 1% ?
#
#      When ever the majority of the top 200 coins move up by X %:
#         - How do they perform the following day?
#         - How do they perform in 3 days?
#         - How do they perform in 1 week?
#         - How do the others that did not move perform the following day?
#         - ect...
#


import validRecords as vr

validRecords = vr.findValidRecords()

for k, v in validRecords.items():
    print('KEY: {} VALUE: {}'.format(k, v))