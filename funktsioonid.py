import pandas as pd
import json as js
import os

def aine_exel(aine):
    df = pd.read_excel("andmed.xlsx", sheet_name=aine, header=None)  # header=None, et saaks read indekseerida
    kõik_alampiirid, alampiir, kõik_max_punktid, max_punktid = [],[],[],[]

    j=1
    for i in range(len(df)): # i on ridade arv
        cell = df.iat[i, 0]  # veerg A
        if cell == "UUS": #kui tuleb "UUS", siis alustan uut katekooriat
            alampiir = dict(zip(df.iloc[j:i, 0], df.iloc[j:i, 1])) #Veerg B
            max_punktid = dict(zip(df.iloc[j:i, 0], df.iloc[j:i, 2])) #veerg C
            kõik_alampiirid.append(alampiir)
            kõik_max_punktid.append(max_punktid)
            kõik_max_punktid.append("UUS")
            kõik_alampiirid.append("UUS")
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


def local_save(data, location=""):
    location = location + "Kasutaja_hinded.json"
    if not os.path.exists(location):
        with open(location, 'w', encoding='utf-8') as f:
            f.write("{}")
    with open(location, 'w', encoding='utf-8') as f:
        js.dump(data, f, ensure_ascii=False, indent=4)

def get_local_data(location=""):
    location = location + "Kasutaja_hinded.json"
    if os.path.exists(location) == False:
        return None
    with open(location, 'r', encoding='utf-8') as f:
        data = js.load(f)
    return data

def küsi_punktid(max_punktid,andmed=None):
    grades = {}
    for i in max_punktid:  # Iga kategooria kohta
        grades[i] = []
        if i == "UUS":
            return grades
            break
        elif andmed != None: #kui uuendatakse
                print(f"Praegu on {andmed.get(i)} punkti kategoorias '{i}'.\nMax punktid on {max_punktid[i]}\nSisesta uued punktid, '-' kui ei tea veel või 'X' kui tahad lõpetada punktide sisestamise:")
                x = 1
                punktid=0
                while True:
                    sisend = input(f"{x}: ").strip()
                    if sisend.upper() == "X":
                        break
                    elif sisend != "-":
                        try:
                            punkt = float(sisend)
                            if 0 <= punkt:
                                punktid+=punkt
                                if punktid <= max_punktid[i]:
                                    grades[i].append(punkt)
                                    x+=1
                                else:
                                    print(f"Sisestatud punktid ({punkt} + {punktid}) ületavad maksimaalseid punkte {max_punktid[i]} selles kategoorias.")

                            else:
                                print(f"Palun sisesta punktid 0 või suurem.")
                        except ValueError:
                            print("Palun sisesta kehtiv arv, '-' või 'X'.")
                    elif sisend == "-":
                        grades[i].append(None)
                        x+=1
        elif andmed == None: #kui sisestatakse esimest korda
            print(f"Praegu on '{i}' kategooria. Max punktid on {max_punktid[i]}.\nSisesta uued punktid, '-' kui ei tea veel või 'X' kui tahad lõpetada punktide sisestamise:")
            x = 1
            punktid=0
            while True:
                sisend = input(f"{x}: ").strip()
                if sisend.upper() == "X":
                    break
                elif sisend != "-":
                    try:
                        punkt = float(sisend)
                        if 0 <= punkt:
                            punktid+=punkt
                            if punktid <= max_punktid[i]:
                                grades[i].append(punkt)
                                x+=1
                            else:
                                print(f"Sisestatud punktid ({punkt} + {punktid}) ületavad maksimaalseid punkte {max_punktid[i]} selles kategoorias.")
                                    
                        else:
                            print(f"Palun sisesta punktid 0 või suurem.")
                    except ValueError:
                        print("Palun sisesta kehtiv arv, '-' või 'X'.")
                elif sisend == "-":
                    grades[i].append(None)
                    x+=1
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

"""
andemd = {
    "Programeerimine 1": {
        "testid":[1, 0, 0.5, 0.25],
        "kodutöö": [2, 1, 0.5, 3],
        "praktikum": "-",
        "projekt": "-",
        "1.kontrolltöö": 19,
        "2.kontrolltöö": "-",
        "Eksam": "-",
        "Lisapunktid": [1,2]
    },
    "AAR 1": {
        "kontrolltööd": [3, 10, 5, "-"],
        "eksam": "-",
        "praktikum": 90
    }
}

local_save(andemd)
"""