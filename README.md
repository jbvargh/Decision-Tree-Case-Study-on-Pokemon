# Pokémon Decision Tree Case Study

A from-scratch ID3 implementation that identifies Pokémon by categorical features, compared head-to-head against a decision tree I built by hand across ~626 leaves and 1,025 species.

## The Question

When I was younger, I remember seeing a video that could narrow down any Pokémon in a specific generation (Johto) in under 10 questions. I found this so fascinating and, in middle school, I finally ended up building a Pokémon guesser for my favorite generation (Sinnoh). Once I completed the elementary level guesser, I wanted to expand on this and find a way to guess any Pokémon. To do this, I spent a couple of years, on and off, hand-building a decision tree in a spreadsheet that identifies any of the 1,025 Pokémon through yes/no questions about type, generation, regional form, weaknesses, and evolution structure. It averages 9.84 questions per identification, but was never formally verified. This project builds the algorithmic counterpart — ID3 from scratch, no scikit-learn — and asks:

- Does information gain beat human intuition on the same problem?
- Where does the algorithm win, where does the hand-tree win, and why?

## Results

After fully creating the tree and measuring the average amount of questions needed to guess any Pokémon, I found that the computer generated tree was able to narrow it down in 8.813 questions outperforming my hand-built tree by roughly one question (9.84). That looks like a clean win, but the number is misleading. The issue is shown further in (`analysis.py`). We can see that, since there are 237 groups with 778 Pokémon in them. Which means that out of the 1025 Pokémon, only 247 of them are actually able to be guessed. The rest of them are stuck in groups that have no features to tell them apart such as Squirtle and Poliwag (both Generation 1 Water Type Pokemon). We can see the 3 largest groups as well, one group has 18 Pokémon in it (with Squirtle being one of those), one group has 14, and another has 12. The pattern is consistent: the largest collision groups are generic-fingerprint Pokémon — mono-type, non-legendary, common weaknesses. Boolean features encode category, not identity, and most Pokémon aren't categorically unique. This is why the hand-tree relied on evolution-structure questions and identity fallbacks that ID3 can't produce.

## How It Works

**Pipeline:** raw Pokémon dataset → feature engineering (`data_cleaning.py`) → `features.csv` → ID3 tree build (`id3.py`) → evaluation (`analysis.py`) → interactive play (`main.py`).

**Feature engineering.** The raw dataset provides base stats, type, generation, and legendary flags. I derive:
- 18 boolean type columns (`is_fire`, `is_water`, …) from `type_1` and `type_2`.
- 18 weakness columns (`weak_to_fire`, …) computed from the full Gen-6+ type effectiveness chart, multiplying attacker effectiveness against both defending types.
- `quad_weak` and `is_immune` flags for any 4× or 0× multiplier.
- Generation one-hot encoding and range buckets to mirror the hand-tree's generation questions.

**ID3 algorithm.** Standard entropy / information gain / recursive splitting, implemented from first principles in ~40 lines:
- `entropy(labels)` — Shannon entropy of a label distribution.
- `information_gain(df, feature)` — parent entropy minus size-weighted average child entropy.
- `best_feature(df, features)` — argmax of information gain across all features.
- `build_tree(df, features)` — recursive; base cases are single-Pokémon leaves and gain-0 stops (attribute-identical clusters).

The tree is a nested dict with `{'question': feature, True: subtree, False: subtree}` for branches, and a name-list for leaves. Group leaves (length > 1) represent Pokémon ID3 cannot separate.

## Design Decisions

The guiding rule: every feature ID3 gets should be one the hand-tree could have used, and vice versa. Otherwise, the comparison stops measuring what it claims to. I excluded base stats because the hand-tree used only one stat question out of ~134, and because vanilla ID3 doesn't split on continuous features (that's C4.5 territory). I excluded abilities because with 150+ near-unique values, ID3 would score huge information gain for the wrong reason — memorizing the ability instead of reasoning about categories, the classic overfitting trap. Generation is used, but as derived booleans (`gen1` or `gen_5_to_9`) rather than the raw numeric column, keeping the splitter categorical. The target set is the 1,025 base species — no regional forms, since the dataset doesn't include them.

## Limitations & Future Work

The biggest gap in v1 is evolution data. The 778 collisions cluster on same-type Pokémon that differ mainly in evolution stage or line which is why my hand-tree leaned on "able to evolve" as its 4th-heaviest question. The dataset I used doesn't include evolution structure, so ID3 has no way to see it. v2 will source evolution data (via PokéAPI or a join against a stage/line dataset on pokedex_id) and rebuild the tree. I expect a large fraction of the 778 collisions to break apart once ID3 can ask about stage and line.

The second gap is regional and alternate forms. The dataset covers only the 1,025 base species, so ID3 can't identify Alolan Marowak, Galarian Darmanitan, Rotom's appliance forms, and so on — even though my hand-tree does. The comparison in v1 runs on the base-species intersection. Extending the dataset to include forms is a smaller v2 task and pairs naturally with the evolution work.

## Running It

```bash
pip install pandas
python data_cleaning.py    # builds features.csv
python id3.py              # builds and pickles the tree
python analysis.py         # prints comparison metrics
python main.py             # play 20-questions against the tree
```

## Files

- `data_cleaning.py` — feature engineering, writes `features.csv`.
- `id3.py` — the algorithm (entropy, gain, best-feature, tree building).
- `analysis.py` — per-Pokémon depth, collision counting, largest-group inspection.
- `main.py` — interactive classifier.

## Changelog

### v1 (initial release)
- ID3 from scratch (entropy, information gain, recursive tree building)
- Feature set: type one-hots, weakness computation, quad-weak/immune flags, generation buckets, legendary/mythical/baby, dual-type
- Analysis: per-Pokémon question depth, collision counting, largest-group inspection
- Compared against hand-built 626-leaf reference tree

### Planned for v2
- Evolution data (stage, line, can-evolve) via PokéAPI join
- Hypothesis: shatters a large fraction of the 778 attribute-identical collisions