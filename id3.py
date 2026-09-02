import math
import pandas as pd
def entropy(group):
    map = {}
    for pokemon in group:
        map[pokemon] = map.get(pokemon, 0) + 1
    result = 0
    for poke in map:
        ratio = map.get(poke)/len(group)
        result = result - (ratio * math.log2(ratio))
    return result

def information_gain(df, feature):
    parent = entropy(df['name'].tolist())
    true_pile  = df[df[feature]]
    false_pile = df[~df[feature]]
    n = len(df)

    after = 0
    if len(true_pile) > 0:
        after += len(true_pile)/n * entropy(true_pile['name'].tolist())
    if len(false_pile) > 0:
        after += len(false_pile)/n * entropy(false_pile['name'].tolist())

    return parent - after

def best_feature(df, features):
    best_gain = -1
    for feature in features:
        gain = information_gain(df, feature)
        if gain > best_gain:
            winner = feature
            best_gain = gain
    return winner, best_gain

def build_tree(df, features):
    if len(df) == 1:
        return df['name'].tolist()
    winner, gain = best_feature(df, features)
    if gain <= 0:
        return df['name'].tolist()
    return {'question': winner, True: build_tree(df[df[winner]], features), False: build_tree(df[~df[winner]], features)}

df = pd.read_csv("features.csv")
exclude = {'name', 'type_1', 'type_2', 'generation'}
features = [c for c in df.columns if c not in exclude]
tree = build_tree(df, features)

print(tree['question'])              # the root question ID3 chose