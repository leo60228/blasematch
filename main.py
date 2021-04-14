from blaseball_mike import reference
from pandas import DataFrame

def get_datablase_stats(player_id):
    data = reference.get_stats(player_id=player_id)
    player = data[0]
    splits = player["splits"]
    frame = DataFrame.from_records(
        ({"season": x["season"], **x["stat"]} for x in splits), index="season"
    )
    return frame

print(get_datablase_stats("90c2cec7-0ed5-426a-9de8-754f34d59b39"))
