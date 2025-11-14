import pandas as pd

def aine(aine):
    df = pd.read_excel("andmed.xlsx", sheet_name=0, header=None)  # header=None, et saaks read indekseerida

    # 2-8 rida, veerud B ja C -> alampiirid ja maks punktid
    alampiir = dict(zip(df.iloc[1:, 0], df.iloc[1:, 1]))  # veerg B (Pythonis index=1)
    maks_punktid = dict(zip(df.iloc[1:, 0], df.iloc[1:, 2]))  # veerg C (Pythonis index=2)

    # 9 rida, veerg C -> aine maks punktid kokku
    #aine_max = df.iloc[8, 2]  # 9. rida index=8 #exeli tapeli ülesehituse taga kinni

    # 12-17 rida, veerud B, C, D -> hinded ja punktid
    hinded = df.iloc[:5, 7].tolist()     # veerg B
    hinded_vordlus = df.iloc[:5, 8].tolist()  # veerg C 
    punktid_hindeks = df.iloc[:5, 9].tolist() # veerg D

    return alampiir, maks_punktid, hinded, hinded_vordlus, punktid_hindeks