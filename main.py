import pandas as pd

df = pd.read_excel("andmed.xlsx", sheet_name="Sheet1")
df['Hinded'] = df['Hinded'].apply(lambda x: list(map(int, x.split(','))))
print(df)
