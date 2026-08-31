import pandas as pd

def multipliers(type_1, type_2):
    out = {}
    for t in types:
        m = TYPE_CHART[t].get(type_1, 1.0)
        if pd.notna(type_2):
            m *= TYPE_CHART[t].get(type_2, 1.0)
        out[t] = m
    return out

df = pd.read_csv("pokemon_dataset/pokemon_complete_2025.csv")

keep = ['name', 'generation', 'type_1', 'type_2', 'is_dual_type', 'is_legendary', 'is_mythical']
df = df[keep]

roman = {'I':1,'II':2,'III':3,'IV':4,'V':5,'VI':6,'VII':7,'VIII':8,'IX':9}
df['generation'] = df['generation'].map(roman)

types = sorted(set(df['type_1']) | set(df['type_2'].dropna()))   # the 18, straight from the data
for t in types:
    df[f'is_{t}'] = (df['type_1'] == t) | (df['type_2'] == t)

TYPE_CHART = {
    'normal':   {'rock':0.5,'ghost':0.0,'steel':0.5},
    'fire':     {'fire':0.5,'water':0.5,'grass':2.0,'ice':2.0,'bug':2.0,'rock':0.5,'dragon':0.5,'steel':2.0},
    'water':    {'fire':2.0,'water':0.5,'grass':0.5,'ground':2.0,'rock':2.0,'dragon':0.5},
    'electric': {'water':2.0,'electric':0.5,'grass':0.5,'ground':0.0,'flying':2.0,'dragon':0.5},
    'grass':    {'fire':0.5,'water':2.0,'grass':0.5,'poison':0.5,'ground':2.0,'flying':0.5,'bug':0.5,'rock':2.0,'dragon':0.5,'steel':0.5},
    'ice':      {'fire':0.5,'water':0.5,'grass':2.0,'ice':0.5,'ground':2.0,'flying':2.0,'dragon':2.0,'steel':0.5},
    'fighting': {'normal':2.0,'ice':2.0,'poison':0.5,'flying':0.5,'psychic':0.5,'bug':0.5,'rock':2.0,'ghost':0.0,'dark':2.0,'steel':2.0,'fairy':0.5},
    'poison':   {'grass':2.0,'poison':0.5,'ground':0.5,'rock':0.5,'ghost':0.5,'steel':0.0,'fairy':2.0},
    'ground':   {'fire':2.0,'electric':2.0,'grass':0.5,'poison':2.0,'flying':0.0,'bug':0.5,'rock':2.0,'steel':2.0},
    'flying':   {'electric':0.5,'grass':2.0,'fighting':2.0,'bug':2.0,'rock':0.5,'steel':0.5},
    'psychic':  {'fighting':2.0,'poison':2.0,'psychic':0.5,'dark':0.0,'steel':0.5},
    'bug':      {'fire':0.5,'grass':2.0,'fighting':0.5,'poison':0.5,'flying':0.5,'psychic':2.0,'ghost':0.5,'dark':2.0,'steel':0.5,'fairy':0.5},
    'rock':     {'fire':2.0,'ice':2.0,'fighting':0.5,'ground':0.5,'flying':2.0,'bug':2.0,'steel':0.5},
    'ghost':    {'normal':0.0,'psychic':2.0,'ghost':2.0,'dark':0.5},
    'dragon':   {'dragon':2.0,'steel':0.5,'fairy':0.0},
    'dark':     {'fighting':0.5,'psychic':2.0,'ghost':2.0,'dark':0.5,'fairy':0.5},
    'steel':    {'fire':0.5,'water':0.5,'electric':0.5,'ice':2.0,'rock':2.0,'steel':0.5,'fairy':2.0},
    'fairy':    {'fire':0.5,'fighting':2.0,'poison':0.5,'dragon':2.0,'dark':2.0,'steel':0.5},
}

mult_df = df.apply(lambda row: multipliers(row['type_1'], row['type_2']), axis=1)
mult_df = pd.DataFrame(mult_df.tolist(), index=df.index)

for t in types:
    df[f'weak_to_{t}'] = mult_df[t] > 1

df['quad_weak'] = (mult_df == 4).any(axis=1)
df['is_immune'] = (mult_df == 0).any(axis=1)

df.to_csv("features.csv", index=False)
print(df.shape)