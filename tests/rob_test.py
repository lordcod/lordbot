import unittest
import random
from typing import Optional, Union


def randfloat(a: float | int, b: float | int, scope: int = 14) -> float:
    return random.randint(int(a*10**scope), int(b*10**scope)) / 10**scope


def clamp(val: Union[int, float],
          minv: Union[int, float],
          maxv: Union[int, float]) -> Union[int, float]:
    return min(maxv, max(minv, val))


def rob(thief_account: dict, victim_account: dict, chance: Optional[int] = None):
    print(thief_account['balance'], victim_account['balance'] +
          thief_account['balance']+thief_account['bank'])
    win_chance = clamp(
        0.1, thief_account['balance']/(victim_account['balance']+thief_account['balance']+thief_account['bank']), 0.75)
    if not chance:
        chance = random.random()
    print(win_chance, chance)
    if win_chance > chance:
        debt = win_chance * \
            victim_account['balance'] * 1/2
        if debt >= thief_account['balance']:
            calculated_debt = (
                thief_account['balance'] * .6
                                         * debt * .2
                                         * randfloat(.8, 1.2)
            )
            thief_account['balance'] += calculated_debt
            victim_account['balance'] -= debt
            print('Not enough on the balance sheet', calculated_debt, debt)
        else:
            thief_account['balance'] += debt
            victim_account['balance'] -= debt
            print('Successful robbery', debt)
    else:
        debt = (1-win_chance) * thief_account['balance'] * 1/2
        thief_account['balance'] -= debt
        print('A complete failure', debt)
    print()


class RobTests(unittest.TestCase):
    def test_rob_equal_bal_only(self):
        # Chance: 0.25 Win: 0.375 Lost: 0.25
        print('test_rob_equal_bal_only')
        print('Win')
        rob(
            {"balance": 500, "bank": 500},
            {"balance": 1000, "bank": 0},
            0.001
        )
        print('Lost')
        rob(
            {"balance": 500, "bank": 500},
            {"balance": 1000, "bank": 0},
            0.999
        )
        print()

    def test_rob_thief_more_bal_only(self):
        # Chance: 0.75 Win: 0.375 Lost: 0.125
        print('test_rob_thief_more_bal_only')
        print('Win')
        rob(
            {"balance": 10000, "bank": 2000},
            {"balance": 1000, "bank": 0},
            0.001
        )
        print('Lost')
        rob(
            {"balance": 10000, "bank": 2000},
            {"balance": 1000, "bank": 0},
            0.999
        )
        print()

    def test_rob_victim_more_bal_only(self):
        # Chance: 0.2 Win: 0.1 Lost: 0.4
        print('test_rob_victim_more_bal_only')
        print('Win')
        rob(
            {"balance": 500, "bank": 500},
            {"balance": 4000, "bank": 0},
            0.001
        )
        print('Lost')
        rob(
            {"balance": 500, "bank": 500},
            {"balance": 4000, "bank": 0},
            0.999
        )
        print()


if __name__ == "__main__":
    unittest.main()
