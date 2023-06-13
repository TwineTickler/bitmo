# Execute this command to run the program
print('Beginning Program...')

# Currently we are assuming the following:
#    1. Checking CMC API for ALL currencies, once per day.
#       This is why we'll use the /v1/cryptocurrency/listings/latest endpoint.
#    2. If we'd like to check specific currencies later on, then we should use the /v2/cryptocurrency/quotes/latest
#       And we will need to write NEW functionality to account for this.

# import all the needed files

import config
import log
import get_quote

# If log path doesn't exist, then create it.
log.check_log_path()

# TODO
# create a loop that cycles through the start parameters until we don't find any more results (use any credits)
# first loop should retrieve 5,000 results
# next should retrieve the 5,001 - 10,000
# final loop should get the remaining ~300 or so, but more could be added daily. (or possibly less)
# loop should also only iterate once if config.all_or_some is set to 0. If set to 1 then loop through all.

parameters = config.parameters
loop_iteration = 1 # tracks the number of times through the loop
stop_loop = False

log.log('beginning loop')
while not stop_loop:

    s = 'loop iteration: {}, start parameter: {}'.format(loop_iteration, parameters['start'])
    log.log(s)
    print(s)

    # TODO Connect to the API and grab the data.

    parameters['start'] = str(int(parameters['limit']) + int(parameters['start']))

    loop_iteration += 1
    if (loop_iteration == 5):
        stop_loop = True

    # if loop is only supposed to occur once based off config settings:
    if (config.all_or_some == 0):
        stop_loop = True

# TODO: move out API call to a separate file to make things easier to read in this new loop

# TODO: move this inside the loop
get_quote.get_quote() # will need to send start and limit parameters based off the loop (possibly more)

# End program
s = 'Program Complete'
log.log(s)
print(s)

