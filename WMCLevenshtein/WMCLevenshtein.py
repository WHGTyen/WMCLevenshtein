from typing import Dict, Tuple, Optional
import re


class WMCLevenshtein:
    def __init__(
        self,
        weights: Dict[Tuple[str, str], float],
        insert_cost: float = 1.0,
        delete_cost: float = 1.0,
        substitute_cost: float = 1.0,
        repeat_character_cost: Optional[float] = None,
        one_way_substitution: bool = False,
    ):
        """
        :param weights: A dictionary of substitution weights. Keys are tuples of strings that can be substituted for each other. Values are floats indicating the cost of substitution.
        :param insert_cost: The cost of inserting a character.
        :param delete_cost: The cost of deleting a character.
        :param substitute_cost: The cost of substituting a character.
        :param repeat_character_cost: The cost of repeating a character. If None, this feature is disabled.
        :param one_way_substitution: If True, substitutions in the weights dictionary only applies in the specified order.
        """
        self.weights = weights.copy()
        self.insert_cost = insert_cost
        self.delete_cost = delete_cost
        self.substitute_cost = substitute_cost
        self.repeat_character_cost = repeat_character_cost

        if not one_way_substitution:
            for (a, b), w in weights.items():
                if (b, a) not in weights:
                    self.weights[(b, a)] = w

        self.a_endings, self.b_endings = zip(*self.weights.keys())

    def distance(self, a: str, b: str) -> float:
        matrix = [[0.0 for _ in range(len(b) + 1)] for _ in range(len(a) + 1)]

        for i in range(len(a) + 1):
            matrix[i][0] = i * self.delete_cost

        for j in range(len(b) + 1):
            matrix[0][j] = j * self.insert_cost

        for i in range(1, len(a) + 1):
            for j in range(1, len(b) + 1):
                costs = []

                if a[i - 1] == b[j - 1]:
                    substitute_cost = 0.0
                else:
                    substitute_cost = self.substitute_cost

                costs.append(matrix[i - 1][j] + self.delete_cost)
                costs.append(matrix[i][j - 1] + self.insert_cost)
                costs.append(matrix[i - 1][j - 1] + substitute_cost)

                a_prefix = a[:i]
                b_prefix = b[:j]

                # Check for weighted substitutions
                a_matches = filter(a_prefix.endswith, self.a_endings)
                b_matches = filter(b_prefix.endswith, self.b_endings)
                if a_matches and b_matches:
                    for a_match in a_matches:
                        for b_match in b_matches:
                            if (a_match, b_match) in self.weights:
                                costs.append(
                                    matrix[i - len(a_match)][j - len(b_match)]
                                    + self.weights[(a_match, b_match)]
                                )

                # Check for repeated characters
                if self.repeat_character_cost is not None:
                    a_repeat = re.search(r"(.)\1+$", a_prefix)
                    if a_repeat and b_prefix.endswith(a_repeat.group(1)):
                        a_repeat_match = a_repeat.group(0)
                        b_repeat_match = re.search(
                            f"{a_repeat.group(1)}+$", b_prefix
                        ).group(0)
                        costs.append(
                            matrix[i - len(a_repeat_match)][j - len(b_repeat_match)]
                            + self.repeat_character_cost
                        )

                    b_repeat = re.search(r"(.)\1+$", b_prefix)
                    if b_repeat and a_prefix.endswith(b_repeat.group(1)):
                        b_repeat_match = b_repeat.group(0)
                        a_repeat_match = re.search(
                            f"{b_repeat.group(1)}+$", a_prefix
                        ).group(0)
                        costs.append(
                            matrix[i - len(a_repeat_match)][j - len(b_repeat_match)]
                            + self.repeat_character_cost
                        )

                matrix[i][j] = min(costs)

        return matrix[-1][-1]
