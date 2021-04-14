from blaseball_mike import reference
from pandas import DataFrame
import pybaseball

def get_datablase_stats(player_id):
    data = reference.get_stats(player_id=player_id)
    player = data[0]
    splits = player['splits']
    records = ({'name': x['player']['fullName'], 'season': x['season'], **x['stat']} for x in splits)
    frame = DataFrame.from_records(records, index=['name', 'season'])
    return frame

def get_fangraphs_stats():
    data = pybaseball.batting_stats(2021)
    reindexed = data.reindex([
        'Name',
        'Season',
        'PA',
        'H',
        '2B',
        '3B',
        'HR',
        'SB',
        'CS',
        'BB',
        'SO',
        'AVG',
        'SLG',
        'OBP'
    ], axis='columns')
    renamed = reindexed.rename({
        'Name': 'name',
        'Season': 'season',
        'PA': 'plate_appearances',
        'H': 'hits',
        '2B': 'doubles',
        '3B': 'triples',
        'HR': 'home_runs',
        'SB': 'stolen_bases',
        'CS': 'caught_stealing',
        'BB': 'walks',
        'SO': 'strikeouts',
        'AVG': 'batting_average',
        'SLG': 'slugging',
        'OBP': 'on_base_percentage',
    }, axis='columns')
    indexed = renamed.set_index(['name', 'season'])
    return indexed

def make_relative(data):
    absolute_columns = [
        'hits',
        'doubles',
        'triples',
        'home_runs',
        'stolen_bases',
        'caught_stealing',
        'walks',
        'strikeouts',
    ]
    data.loc[:, absolute_columns] = data.loc[:, absolute_columns].div(data['plate_appearances'], axis='index')
    data.drop('plate_appearances', inplace=True, axis='columns')

tot = get_datablase_stats('90c2cec7-0ed5-426a-9de8-754f34d59b39')
mlb = get_fangraphs_stats()

tot, mlb = tot.align(mlb, join='inner', axis='columns')

make_relative(tot)
make_relative(mlb)

residuals = mlb - tot.iloc[0]
print(residuals)

squared = residuals ** 2
print(squared)

rss = squared.sum(axis='columns')
print(rss)

closest = rss.idxmin()
print(rss.idxmin())

print(tot)
print(mlb.loc[rss.idxmin()])
