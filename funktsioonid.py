import pandas as pd

def aine(aine):
    df = pd.read_excel("andmed.xlsx", sheet_name=aine, header=None)  # header=None, et saaks read indekseerida
    kõik_alampiirid = alampiir = kõik_max_punktid = max_punktid = []

    j=1
    for i in range(len(df)): # i on ridade arv
        cell = df.iat[i, 0]  # veerg A
        if cell == "UUS": #kui tuleb "UUS", siis alustan uut katekooriat
            alampiir = dict(zip(df.iloc[j:i, 0], df.iloc[j:i, 1]))
            max_punktid = dict(zip(df.iloc[j:i, 0], df.iloc[j:i, 2]))
            kõik_alampiirid.append(alampiir)
            kõik_max_punktid.append(max_punktid)
            j = i+1
            continue
    if j < len(df): #viimase plokki lisamine
        alampiir = dict(zip(df.iloc[j:, 0], df.iloc[j:, 1]))
        max_punktid = dict(zip(df.iloc[j:, 0], df.iloc[j:, 2]))
        kõik_alampiirid.append(alampiir) #ühtemassiivi lisamine
        kõik_max_punktid.append(max_punktid) #ühtemassiivi lisamine


    # 12-17 rida, veerud f, g, h -> hinded ja punktid
    hinded = df.iloc[1:5, 5].tolist()     # veerg f
    punktid_hindeks = df.iloc[1:6, 7].tolist() # veerg h

    return kõik_alampiirid, kõik_max_punktid, hinded, punktid_hindeks

def küsi_punktid(max_punktid):
    grades = {}
    #for i in max_punktid:  # Iga kategooria kohta
    while True:
        sisend = (f"{i}: ")
        if sisend != "-":
            try:
                punkt = int(sisend)
                if 0 <= punkt <= max_punktid[i]:
                    grades[i] = (punkt)
                    break
                else:
                    print(f"Palun sisesta punktid vahemikus 0 kuni {max_punktid[i]}.")
            except ValueError:
                print("Palun sisesta kehtiv arv või '-'.")
        else:
            grades[i] = None
            break
    return grades

def arvuta_hinne(kokku_punkte, punktid_hindeks, hinded):
    for i in range(len(hinded)):
        if i != len(hinded) - 1:
            if kokku_punkte < punktid_hindeks[i]:
                saadud_hinne = hinded[i + 1]
                break
        elif kokku_punkte >= punktid_hindeks[i]:
            saadud_hinne = hinded[i]
            break
    return saadud_hinne