""""
Programm: abifunktsioonid main programmi jaoks
Autorid: Artur Ilumäe ja Hannela Haavel

Rohkem info main.py failis
"""

import pandas as pd
import json as js
import os


def kirjuta_väljundisse(väljund, tekst): #gui kirjutamis funktsioon
    if hasattr(väljund, 'insert') and callable(getattr(väljund, 'insert')): # kontrollib kas self.väljund on tkinter.Text
        väljund.insert('end', tekst)
        return
    
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
        kõik_alampiirid.append(alampiir)
        kõik_max_punktid.append(max_punktid)

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

def loe_kohalikud_andmed(location="Desktop"):#<-- Muuda asukohta vastavalt vajadusele kus andmed asuvad
    location = os.path.join(os.path.expanduser("~"), location+"/Kasutaja_hinded.json")
    if os.path.exists(location) == False:
        return None
    with open(location, 'r', encoding='utf-8') as f:
        data = js.load(f)
    return data

def valideeri_ja_salvesta(aine, sisend_muutujad, salvestatud_andmed): #Valideerib ja salvestab aine punktid.
    aine_punktid = {}
    for k, (muutuja, maks) in sisend_muutujad.items():
        tekst = muutuja.get().strip()
        if tekst == "":
            aine_punktid[k] = None
            continue
        osad = [i.strip() for i in tekst.split(',') if i.strip() != ""]
        väärtused = []
        summa = 0
        kehtiv = True
        for i in osad:
            try:
                v = float(i)
                if v < 0:
                    kehtiv = False
                    break
                summa += v
                väärtused.append(v)
            except ValueError:
                kehtiv = False
                break
        if not kehtiv or summa > maks:
            return False, f"Kehtetud väärtused kategoorias {k} või summa ületab maksimumi ({maks}).", None
        aine_punktid[k] = väärtused
    
    # salvesta salvestatud_andmete sisse
    salvestatud_andmed.setdefault(aine, {})
    salvestatud_andmed[aine].update(aine_punktid)
    salvesta_kohalikult(salvestatud_andmed)
    return True, "Punktid salvestatud.", salvestatud_andmed

def kuvamiseks_andmed(aine, salvestatud_andmed):
    #Ettevalmistab andmed kuvamiseks. Tagastab (edukas, tekst_väljund)
    if not salvestatud_andmed:
        return "Salvestatud andmed puuduvad.\n"
    
    aine_andmed = salvestatud_andmed.get(aine)
    if not aine_andmed:
        return f"Salvestatud andmed ainele {aine} puuduvad.\n"
    
    tekst = f"Aine: {aine}\n"
    if isinstance(aine_andmed, dict):
        for k, v in aine_andmed.items():
            tekst += f"  {k}: {v}\n"
    else:
        tekst += f"  {repr(aine_andmed)}\n"
    
    return tekst

def arvuta_hinne(punktid, alampiir, punktid_hindeks, hinded, väljund=None): # Lisada täielik hinnde arvutus
    kokku_punkte = 0
    läbitud = True
    läbikukkudud = {}
    for i in punktid.keys(): #iga kategooria kohta
        punkti_kontroll = 0
        väärtused_kategoorias = punktid.get(i)
        if not väärtused_kategoorias:
            väärtuste_iter = []
        else:
            väärtuste_iter = väärtused_kategoorias

        for väärtus in väärtuste_iter:
            if väärtus is not None:
                kokku_punkte += väärtus
                punkti_kontroll += väärtus

        # Kontrollib alampiire
        def alampiiri_plokk(ploki_indeks):
            try:
                plokk = alampiir[ploki_indeks]
                if isinstance(plokk, dict):
                    return plokk.get(i, None)
            except Exception:
                pass
            return None

        # üks nõue
        nõue_üks = alampiiri_plokk(0)
        if nõue_üks is not None and len(alampiir) == 1:
                    if punkti_kontroll < nõue_üks:
                        läbitud = False
                        kirjuta_väljundisse(väljund, f"Kategoorias '{i}' ei ole saavutatud minimaalset punktide arvu, sull on {punkti_kontroll} vaja on {nõue_üks}.\n")

        # mittu nõuet
        if len(alampiir) > 1:
            läbikukkudud.setdefault(i, [])
            for ploki_indeks in range(len(alampiir)):
                nõue = alampiiri_plokk(ploki_indeks)
                if nõue is None:
                    läbikukkudud[i].append([None, True])
                    continue
                if punkti_kontroll < nõue:
                    läbitud = False
                    läbikukkudud[i].append([nõue, False, punkti_kontroll])
                    kirjuta_väljundisse(väljund, f"Kategoorias '{i}' ei ole saavutatud minimaalset punktide arvu, sull on {punkti_kontroll} vaja on {nõue}.\n")
                else:
                    läbikukkudud[i].append([nõue, True])
                                    
    saadud_hinne = None
    if len(hinded) > 0 and len(punktid_hindeks) > 0:
        for indeks in range(len(punktid_hindeks)):
            if indeks < len(hinded):
                if kokku_punkte >= punktid_hindeks[indeks]:
                    saadud_hinne = hinded[indeks]
                    break
        if saadud_hinne is None and len(hinded) > 0:
            saadud_hinne = hinded[-1]
    
    if läbitud:
        kirjuta_väljundisse(väljund, f"Kokku on punkte: {round(kokku_punkte,2)}\nSaadud hinne {saadud_hinne}.\n")
    else:
        kirjuta_väljundisse(väljund, f"Kokku saaksid punkte: {round(kokku_punkte, 2)}. Millega saaksid {saadud_hinne}.\nAga kuna ülaltoodud aine/ainede alampiir pole läbitud on hinne F.\n")

