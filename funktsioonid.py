import pandas as pd
import json as js
import os


def loe_aine_fail(aine):
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


def salvesta_kohalikult(data, location="Desktop"): #<-- Muuda asukohta vastavalt vajadusele kuhu salvestada
    location = os.path.join(os.path.expanduser("~"), location+"/Kasutaja_hinded.json")
    if not os.path.exists(location):
        with open(location, 'w', encoding='utf-8') as f:
            f.write("{}")
    with open(location, 'w', encoding='utf-8') as f:
        js.dump(data, f, ensure_ascii=False, indent=4)

def loe_kohalikud_andmed(location="Desktop"):#<-- Muuda asukohta vastavalt vajadusele kuhu salvestada
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

def arvuta_hinne_gui(grades, alampiir, punktid_hindeks, hinded, self, tk): # Lisada täielik hinnde arvutus
    try:
        # mode: "kokk" for summary, "täie" for full. When called from GUI, pass mode explicitly.
        kokku_punkte = 0
        läbitud = True
        läbikukkudud = {}
        for i in grades.keys(): #iga kategooria kohta
            punkti_kontroll = 0
            vals_for_cat = grades.get(i)
            if not vals_for_cat:
                vals_iter = []
            else:
                vals_iter = vals_for_cat

            # sum up points for this category
            for v in vals_iter:
                if v is not None:
                    kokku_punkte += v
                    punkti_kontroll += v

            # Determine minimal required points for this category (if present)
            # alampiir is expected to be a list of dicts; find values safely
            def get_req_from_block(block_idx):
                try:
                    block = alampiir[block_idx]
                    if isinstance(block, dict):
                        return block.get(i, None)
                except Exception:
                    pass
                return None

            # Single-block minimal check
            req_single = get_req_from_block(0)
            if req_single is not None and len(alampiir) == 1:
                if punkti_kontroll < req_single:
                    läbitud = False
                    self.väljund.insert(tk.END, f"Kategoorias '{i}' ei ole saavutatud minimaalset punktide arvu, sull on {punkti_kontroll} vaja on {req_single}.\n")

            # Multi-block minimal checks
            if len(alampiir) > 1:
                läbikukkudud.setdefault(i, [])
                for j in range(len(alampiir)):
                    req = get_req_from_block(j)
                    if req is None:
                        # if no requirement for this block, treat as passed
                        läbikukkudud[i].append([None, True])
                        continue
                    if punkti_kontroll < req:
                        läbitud = False
                        läbikukkudud[i].append([req, False, punkti_kontroll])
                    else:
                        läbikukkudud[i].append([req, True])
                                        
        saadud_hinne = None
        # Lihtsustatud versioon: arvuta hinne ainult kokku_punkte alusel
        if len(hinded) > 0 and len(punktid_hindeks) > 0:
            for idx in range(len(punktid_hindeks)):
                if idx < len(hinded):
                    if kokku_punkte >= punktid_hindeks[idx]:
                        saadud_hinne = hinded[idx]
                        break
            # Kui hinne pole määratud, anna viimane hinne
            if saadud_hinne is None and len(hinded) > 0:
                saadud_hinne = hinded[-1]
        
        if läbitud:
            self.väljund.insert(tk.END, f"Kokku on punkte: {round(kokku_punkte,2)}\nSaadud hinne {saadud_hinne}.\n")
        else:
            self.väljund.insert(tk.END, f"Kokku saaksid punkte: {round(kokku_punkte, 2)}. Millega saaksid {saadud_hinne}.\nAga kuna ülaltoodud aine/ainede alampiir pole läbitud on hinne F.\n")
    
    except Exception as e:
        self.väljund.insert(tk.END, f"Viga arvutamisel: {str(e)}\n")


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

