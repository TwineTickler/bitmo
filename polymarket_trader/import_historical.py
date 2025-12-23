# use pd.set_option('display.max_rows', None) -- min_rows as well
# default is 10, None will show all rows, or you can use a larger number

# use df.head(200).copy(deep=True) to make clean copy of your df

# get 1 hour of data from df_filtered2
# t = df_analysis.loc[0]['hour_floored']
# df_filtered2[df_filtered2['hour'] == t]

# to select a specific column, pass in a list [] of column names

import pandas as pd
from datetime import datetime

column_names = ['Datetime', 'Price', 'Volume']

print('\nImporting data from CSV...')
df = pd.read_csv('/Users/sean/Downloads/Kraken_trading_history/XBTUSD.csv', names=column_names, header=None)
print('Import complete')

print('formatting dates...')
df['Datetime'] = pd.to_datetime(df['Datetime'], unit='s')

# Sort the DataFrame by 'datetime' to ensure chronological order
print('sorting data...')
df = df.sort_values('Datetime')

# Create a 'minute' column by flooring the datetime to the start of each minute
print('creating minute column...')
df['minute'] = df['Datetime'].dt.floor('min')

# Group by 'minute' and select the first row in each group (which is the earliest timestamp in that minute due to sorting)
# This first row will have the smallest seconds value in that minute
df_grouped = df.groupby('minute').first()

# Extract the seconds from the 'datetime' in the grouped DataFrame
df_grouped['seconds'] = df_grouped['Datetime'].dt.second

# Filter to keep only those minutes where the smallest seconds <= 5
df_filtered = df_grouped[df_grouped['seconds'] <= 30]

# Optionally, drop the helper columns if you don't need them
df_filtered = df_filtered.drop(columns=['minute', 'seconds'])

# Reset the index if you want 'datetime' back as a column (minute was the index)
df_filtered = df_filtered.reset_index(drop=True)

# filter down minutes that have at least 30 entries

# create hour column in filtered DF
df_filtered['hour'] = df_filtered['Datetime'].dt.floor('h')

# add column with count of minutes per hour
df_filtered['hour_count'] = df_filtered.groupby('hour').transform('size')

# remove any hours which have less than 30 minute rows of data per hour
df_filtered2 = df_filtered[df_filtered['hour_count'] >= 30]

# mark any hours which we have a next hour time and price for

# get a list of unique hours
unique_hours = df_filtered2['hour'].unique()

# create a set for O(1) lookups
unique_set = set(pd.to_datetime(unique_hours))

# Dictionary to map each hour to whether the next hour exists
has_next = {}
for hour in unique_hours:
    next_hour = hour + pd.Timedelta(hours=1)
    has_next[pd.to_datetime(hour)] = next_hour in unique_set

# Add the new column by mapping the floored_hour values
df_filtered2.loc[:, 'has_next_hour'] = df_filtered2['hour'].map(has_next)




# data is clean, ready to analyse.

df_analysis = pd.DataFrame(columns=[
    'hour_floored',
    'df_filtered2_min_id',
    'df_filtered2_next_id',
    'start_time',
    'end_time',
    'start_price',
    'end_price',
    'end_direction',
    'end_delta',
    '15-30-45_data_not_available',
    '15_min_price',
    '15_min_avg',
    '15_min_delta',
    '15_min_direction',
    '15_min_avg_direction',
    '30_min_price',
    '30_min_avg',
    '30_min_delta',
    '30_min_direction',
    '30_min_avg_direction',
    '15-30_min_avg',
    '15-30_min_avg_direction',
    '45_min_price',
    '45_min_avg',
    '45_min_delta',
    '45_min_direction',
    '45_min_avg_direction',
    '30-45_min_avg',
    '30-45_min_avg_direction',
    ])

# loop through each hour
t = datetime.now()
print('analysing data... current time: {}'.format(t))
c = 0
for h, b in has_next.items():
    if c > 40:
        break
    if b == True:
        min_id = df_filtered2[df_filtered2['hour'] == h].index.min()
        next_id = df_filtered2[df_filtered2['hour'] == h].index.max() + 1
        end_price = df_filtered2.loc[next_id]['Price']
        start_price = df_filtered2.loc[min_id]['Price']
        if end_price >= start_price:
            end_direction = 'up'
        else:
            end_direction = 'down'
        end_delta = ((end_price/start_price)*100)-100
        t15 = h + pd.Timedelta(minutes=15)
        t30 = h + pd.Timedelta(minutes=30)
        t45 = h + pd.Timedelta(minutes=45)
        if (df_filtered2[df_filtered2['minute'] == t15]['minute'].any() and df_filtered2[df_filtered2['minute'] == t30]['minute'].any() and df_filtered2[df_filtered2['minute'] == t45]['minute'].any()):
            data_not_available = False
        else:
            data_not_available = True
        new_row_data = {
            'hour_floored': h,
            'df_filtered2_min_id': min_id,
            'df_filtered2_next_id': next_id,
            'start_time': df_filtered2.loc[min_id]['Datetime'],
            'end_time': df_filtered2.loc[next_id]['Datetime'],
            'start_price': start_price,
            'end_price': end_price,
            'end_direction': end_direction,
            'end_delta': end_delta,
            '15-30-45_data_not_available': data_not_available
            }
        df_analysis.loc[len(df_analysis)] = new_row_data
        c = c+1
print('analysis complete. Time to complete: {}'.format(datetime.now()-t))
