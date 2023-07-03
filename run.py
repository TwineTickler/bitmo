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

log.check_log_path() # If log path doesn't exist, then create it.

# print(target_run_time) # can python access a variable from within the script that is calling another file?

# create a loop that cycles through the start parameters until we don't find any more results (use any credits)
# first loop should retrieve 5,000 results
# next should retrieve the 5,001 - 10,000
# final loop should get the remaining ~300 or so, but more could be added daily. (or possibly less)
# loop should also only iterate once if config.all_or_some is set to 0. If set to 1 then loop through all.

parameters = config.parameters
loop_iteration = 1 # tracks the number of times through the loop
stop_loop = False
# going to essentially SAVE the start parameter, so that once we complete the loop, we can reset it back to what it was befor we ran through the loop. (since it gets updated each time)
# because when running timer.py, it was remembering the last value that it had. (15001)
initial_start_parameter = parameters['start']

log.log('beginning loop')
while not stop_loop:

    s = 'loop iteration: {}, start parameter: {}'.format(loop_iteration, parameters['start'])
    log.log(s)
    print(s)

    # Connect to the API and grab the data.
    credit_count = get_quote.get_quote(parameters['start'])
    s = 'credits used for last API call: {}'.format(credit_count)
    log.log(s)
    print(s)

    # in prod: when credit_count = 0, then we can stop.
    # in sandbox: credit_count IS ALWAYS 1, so we'll have to simulate it changing to 0.
    # ALSO, I just learned that there is an undocumented key called 'total_count' we could use. #FacePalm

    if (loop_iteration == 3 and (config.environment == 'sandbox' or config.environment == 'offline')):  # using for sandbox, to stop the loop
        s = 'manually setting credit_count to 0 for sandbox environment to stop the loop'
        log.log(s)
        credit_count = 0

    # stop the loop if we reach the end of currency list
    if (credit_count == 0):
        log.log('credit_count set to 0, ending the loop')
        stop_loop = True
    
    # if (loop_iteration == 7): # using only for DEV for when starting prod testing. (scared to go over)
    #    stop_loop = True

    # set the start parameter for next loop iteration.
    parameters['start'] = str(int(parameters['limit']) + int(parameters['start']))

    if (loop_iteration == 10): # using this as a fail safe to stop an infinite loop
        s = 'ERROR: Infinite Loop fail safe triggered. Investigate to find the cause.'
        log.log(s)
        print(s)
        stop_loop = True

    # if loop is only supposed to occur once based off config settings:
    if (config.all_or_some == 0):
        s = 'WARNING: config.all_or_some is set to 0, so only running the loop once.'
        log.log(s)
        print(s)
        stop_loop = True

    loop_iteration += 1

# reset the parameter start back to initial value (if using timer.py)
ending_start_parameter = parameters['start']
parameters['start'] = initial_start_parameter
s = 'parameter[start] reinitialized from: {} --> to: {}'.format(ending_start_parameter, parameters['start'])
log.log(s)
print(s)

# End program
s = 'Program Complete'
log.log(s)
print(s)

