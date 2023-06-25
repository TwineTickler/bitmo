# Purpose of this file is to connect to the database and reveal any currency trends
#
#

# first trend I'd like to check are upward trends
# defined as:
# 
# quote table entities:
# - price
#      - continues to increase in value
# - percent_change_24h
#      - I would expect this to also be positive, following the price values


# First we need to find valid currencies to analyze against
# They should have the following:
# at least 3 entries with 3 days, but possibly more.
# What is concidered a valid day?
#
# There will be at least 3 days.
# There will be a day 1:
#    - day 1 does not have a valid day preceeding it.
# There will be an X number of middle days
#    - middle days must have a valid day before and after it.
# There will be an end day:
#    - end day will not have any valid day after it.

# for days to qualify or be considered to be before or after another, they need to be within 24 hours + 8 hours before or after.
# This gives leway for when times are slightly off, or when running the program ran into problems, and was delayed.

# First thing we will need to do is establish our valid days.

