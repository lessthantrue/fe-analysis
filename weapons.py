import pandas as pd
import os
import functools

weapon_csv_cols = [
    'name1', 'name2', 'rank', 'range', 
    'weight', 'might', 'hit', 'crit', 
    'uses', 'value', 'notes'
]

weapons = ['bow', 'axe', 'lance', 'sword']

keep_cols = [
    'name', 'rank', 'range', 'weight',
    'might', 'hit', 'crit', 'uses', 'type'
]

weapon_data_array = []

for w in weapons:
    csv_path = os.path.join('fe6_weapon_data', w + '.csv')
    df = pd.read_csv(csv_path, header=None, sep='\t', comment="#")
    df.set_axis(weapon_csv_cols, axis=1)
    df['type'] = w
    df = df.set_index('name1').rename({'name2':'name'}, axis=1)[keep_cols]
    weapon_data_array.append(df)

weapon_data = pd.concat(weapon_data_array)

if __name__ == "__main__":
    print(weapon_data)