import pickle
import pandas as pd

def find_question_length(tree, row):
    node = tree
    count = 0
    while isinstance(node, dict):
        answer = row[node['question']]
        node = node[answer]    
        count += 1
    return count

with open("tree.pkl", "rb") as f:
    tree = pickle.load(f)
df = pd.read_csv("features.csv")

def count_collisions(node):
    if not isinstance(node, dict):
        return 1 if len(node) > 1 else 0
    return count_collisions(node[True]) + count_collisions(node[False])

def count_trapped(node):
    if not isinstance(node, dict):
        return len(node) if len(node) > 1 else 0
    return count_trapped(node[True]) + count_trapped(node[False])

counts = [find_question_length(tree, row) for _, row in df.iterrows()]
print("average:", sum(counts) / len(counts))
print("max:", max(counts), " min:", min(counts))

print(count_collisions(tree))
print(count_trapped(tree))

def collect_groups(node):
    if not isinstance(node, dict):
        return [node] if len(node) > 1 else []
    return collect_groups(node[True]) + collect_groups(node[False])

groups = collect_groups(tree)
groups.sort(key=len, reverse=True)

for g in groups[:3]:
    print(len(g), "stuck together — e.g.", g[0])