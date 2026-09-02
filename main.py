import pickle
from id3 import classify
with open("tree.pkl", "rb") as f:
    tree = pickle.load(f)
print(classify(tree))