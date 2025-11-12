import pandas as pd

def read_excel_data(aine):
    # Loe kogu tööleht
    df = pd.read_excel("andmed.xlsx", sheet_name=0, header=None)  # header=None, et saaks read indekseerida

    # 2-8 rida, veerud B ja C -> alampiirid ja maks punktid
    alim_punktid = df.iloc[1:8, 1].tolist()  # veerg B (Pythonis index=1)
    maks_punktid = df.iloc[1:8, 2].tolist()  # veerg C (Pythonis index=2)

    # 9 rida, veerg C -> aine maks punktid kokku
    aine_max = df.iloc[8, 2]  # 9. rida index=8

    # 12-17 rida, veerud B, C, D -> hinded ja punktid
    hinded = df.iloc[11:17, 1].tolist()     # veerg B
    hinded_vordlus = df.iloc[11:17, 2].tolist()  # veerg C
    punktid_hindeks = df.iloc[11:17, 3].tolist() # veerg D
    # tagasta tulemusi
    return alim_punktid, maks_punktid, aine_max, hinded, hinded_vordlus, punktid_hindeks