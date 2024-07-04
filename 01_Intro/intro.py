"""
Script de la clase introductoria, para recordar uso de librería Pandas.
"""


import pandas as pd


countries: list[str] = ['Russia', 'USA', 'UK', 'Germany', 'France', 'India']
population: list[int] = [143, 33, 28, 83, 65, 138]  # random data, not real!

df: pd.DataFrame = pd.DataFrame.from_dict(
    dict({'Country': countries, 'Population': population}),
)
print(df)  # dbg

df.to_csv('./01_Intro/res/intro.csv', index=False)
