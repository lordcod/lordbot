import numpy as np
import pandas as pd


s = pd.Series(np.arange(5),
              index=["a", "b", "c", "d", "e"])
print(s)
print()

df = pd.DataFrame([['Bob', 'Builder'],
                  ['Sally', 'Baker'],
                  ['Scott', 'Candle Stick Maker']],
                  columns=['name', 'occupation'])
print(df)
print()
