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
            alampiir = {k: v for k, v in alampiir.items() if k == k}  # k==k on tõsi ainult kui k ei ole NaN
            max_punktid = {k: v for k, v in max_punktid.items() if k == k}
            kõik_alampiirid.append(alampiir)
            kõik_max_punktid.append(max_punktid)
            j = i+1
            continue
    if j < len(df): #viimase plokki lisamine
        alampiir = dict(zip(df.iloc[j:, 0], df.iloc[j:, 1]))
        max_punktid = dict(zip(df.iloc[j:, 0], df.iloc[j:, 2]))
        alampiir = {k: v for k, v in alampiir.items() if k == k}  # k==k on tõsi ainult kui k ei ole NaN
        max_punktid = {k: v for k, v in max_punktid.items() if k == k}
        kõik_alampiirid.append(alampiir) #ühtemassiivi lisamine
        kõik_max_punktid.append(max_punktid) #ühtemassiivi lisamine


    # 12-17 rida, veerud f, g, h -> hinded ja punktid
    hinded = df.iloc[1:5, 5].tolist()     # veerg f
    punktid_hindeks = df.iloc[1:6, 7].tolist() # veerg h

    return kõik_alampiirid, kõik_max_punktid, hinded, punktid_hindeks


def local_save(data, location="Desktop"): #<-- Muuda asukohta vastavalt vajadusele kuhu salvestada
    location = os.path.join(os.path.expanduser("~"), location+"/Kasutaja_hinded.json")
    if not os.path.exists(location):
        with open(location, 'w', encoding='utf-8') as f:
            f.write("{}")
    with open(location, 'w', encoding='utf-8') as f:
        js.dump(data, f, ensure_ascii=False, indent=4)

def get_local_data(location="Desktop"):#<-- Muuda asukohta vastavalt vajadusele kuhu salvestada
    location = os.path.join(os.path.expanduser("~"), location+"/Kasutaja_hinded.json")
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

def arvuta_hinne(grades, alampiir, punktid_hindeks, hinded, max_punktid): # Lisada täielik hinnde arvutus
    choice = input("Kas soovid kokkuvõtvad või täielikku ülevaadet (kokk/täie): ").strip().lower()
    if choice == "kokk":
        kokku_punkte = 0
        läbitud = True
        läbikukkudud = {}
        for i in grades.keys(): #iga kategooria kohta
            punkti_kontroll = 0
            for j in grades[i]:
                if j != None:
                    kokku_punkte += j
                    punkti_kontroll += j
            if punkti_kontroll < alampiir[0][i] and len(alampiir) == 1:
                läbitud = False
                print(f"Kategoorias '{i}' ei ole saavutatud minimaalset punktide arvu, sull on {punkti_kontroll} vaja on {alampiir[0][i]}.")
            elif len(alampiir) > 1: #kui on mitu alampiiri
                läbikukkudud = {i: []}
                for j in range(len(alampiir)):
                    if punkti_kontroll < alampiir[j][i]:
                        läbitud = False
                        läbikukkudud[i].append([alampiir[j][i], False, punkti_kontroll])
                    elif punkti_kontroll >= alampiir[j][i]:
                        läbikukkudud[i].append([alampiir[j][i], True])
                                      
        saadud_hinne = None
        if len(alampiir) == 1:
            for i in range(len(hinded)):
                if i != len(hinded) - 1:
                    if kokku_punkte < punktid_hindeks[i]:
                        saadud_hinne = hinded[i + 1]
                        break
                elif kokku_punkte >= punktid_hindeks[i]:
                    saadud_hinne = hinded[i]
                    break
        else:
            tulemus = []
            for i in range(len(next(iter(läbikukkudud.values())))):
                for j in läbikukkudud.keys():
                    if läbikukkudud[j][i][1] == False:
                        tulemus.append(False)
                        break
            if True not in tulemus: #kui kõik alampiirid on false
                print(f"Selles aines on mittu võimalikut alampiiri.")
                for i in range(len(next(iter(läbikukkudud.values())))):
                    print(f"Võimalik alampiir {i+1}:")
                    for j in läbikukkudud.keys():
                        print(f"  Kategooria '{j}': vaja {läbikukkudud[j][i][0]} punkti, said {round(läbikukkudud[j][i][2],2)} punkti.")
                läbitud = False
            for i in range(len(hinded)):
                if i != len(hinded) - 1:
                    if kokku_punkte < punktid_hindeks[i]:
                        saadud_hinne = hinded[i + 1]
                        break
                elif kokku_punkte >= punktid_hindeks[i]:
                    saadud_hinne = hinded[i]
                    break
        
        if läbitud:
            print(f"Kokku on punkte: {round(kokku_punkte,2)}\nSaadud hinne {saadud_hinne}.")
        else:
            print(f"Kokku saaksid punkte: {round(kokku_punkte, 2)}. Millega saaksid {saadud_hinne}.\nAga kuna ülaltoodud aine/ainede alampiir pole läbitud on hinne F.")
    elif choice == "täie":
        print("Täielik ülevaade pole veel valmis.")

def kuva_andmed(grades):
    for aine, kategooriad in grades.items():
        print(f"\nAine: {aine}")
        for kategooria, punktid in kategooriad.items():
            if kategooria == "UUS":
                print("  Uus kategooria, andmed puuduvad.")
                continue
            print(f"  Kategooria: {kategooria}")
            for i, punkt in enumerate(punktid, 1):
                if punkt is None:
                    print(f"    Ülesanne {i}: Puudub")
                else:
                    print(f"    Ülesanne {i}: {punkt} punkti")

def õppe_aine(subject_list,subjects):
    print("Mis õppeainel: ")
    for i, subj in enumerate(subject_list, 1): #aine küsimine
        print(f"{i}. {subj}")
    while True:
        choice = int(input("Sisesta õppeaine number: "))
        if 1 <= choice <= len(subject_list):
            subject_key = subject_list[choice - 1]
            subject = subjects[subject_key]
            print(f"Valisid: {subject_key}")
            break
        else:
            print(f"Palun vali number 1-{len(subject_list)}.")
            continue
    return subject

""" Näide andmetest
andemd = {
    "Programmeerimine 1": {
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

"""