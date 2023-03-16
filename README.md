# Weighted Multi-Character Levenshtein Edit Distance

This is an implementation of the Wagner-Fischer algorithm that also allows:
* Assigning weights to different substitutions
* Defining multi-character substitutions
* Ignoring or specifying a weight for character repetitions

## Usage

```python
from WMCLevenshtein import WMCLevenshtein

weights = {
    ("o", "ou"): 0.1,
    ("z", "s"): 0.1,
}

lev = WMCLevenshtein(weights)
print(lev.distance("colourise", "colorize"))
>>> 0.2

lev = WMCLevenshtein(weights, one_way_substitution=True)
print(lev.distance("colourise", "colorize"))
>>> 2.0

lev = WMCLevenshtein(weights, repeat_character_cost=0.1)
print(lev.distance("colorize", "colorizeeee"))
>>> 0.1
```

### Notes
1. One-way substitution and character repetition are disabled by default.
2. The algorithm always tries to find the minimum cost, so if the specified weight is higher than the original cost, it will be ignored.