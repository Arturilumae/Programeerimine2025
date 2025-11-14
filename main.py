import funktsioonid as fn # kus kõik funktsioonid on 

grades = {}
subjects = { #ainete määraine
    "Programeerimine": "Programmeerimine 1",
    "Arvuti arhitektuur ja riistvara 1": "AAR 1",
    "Operatsioonisüsteemid": "Opsys",
    "Kõrgem matemaatika 1": "KÕM 1",
    "Sissejuhatus erialasse": "Sissejuhatus erialasse"
}

subject_list = list(subjects.keys())
print("Vali õppeaine: ")
for i, subj in enumerate(subject_list, 1): #aine küsimine
    print(f"{i}. {subj}")

choice = int(input("Sisesta õppeaine number: "))
if 1 <= choice <= len(subject_list):
    subject_key = subject_list[choice - 1]
    subject = subjects[subject_key]
    print(f"Valisid: {subject_key}")
else:
    print("Vale valik!")

alampiirid, max_punktid, hinded, punktid_hindeks = fn.aine(subject) # Andmed tapelist
print(f"Valisid õppeaine: {subject}")
print("Sisesta oma punktid järgmiste katekooriate kohta ('-' tähendab, et puudub tulemus):")

grades = fn.küsi_punktid(max_punktid[0])  # Preagu kasutame esimest katekooriat   !!!NB HILJEM MUUTA

kokku_punkte = sum(p for p in grades.values() if p is not None)

saadud_hinne = fn.arvuta_hinne(kokku_punkte, punktid_hindeks, hinded)

print(f"Sinu hinne ja punktid hetkel on: {saadud_hinne} ja {kokku_punkte} punkti.")

