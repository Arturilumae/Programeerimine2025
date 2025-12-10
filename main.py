import funktsioonid as fn # kus kõik funktsioonid on 

grades = { #ainete määramine
    "Programeerimine 1": {},
    "AAR 1": {},
    "Opsys": {},
    "KÕM 1": {},
    "Sissejuhatus erialasse": {}
}
subjects = { #ainete määraine
    "Programmeerimine": "Programmeerimine 1",
    "Arvuti arhitektuur ja riistvara 1": "AAR 1",
    "Operatsioonisüsteemid": "Opsys",
    "Kõrgem matemaatika 1": "KÕM 1",
    "Sissejuhatus erialasse": "Sissejuhatus erialasse"
}
käsud = ["Sisesta punktid", "Arvuta hinne #Pole valmis", "Salvesta andmed #Pole valmis", "Loe salvestatud andmed #Pole valmis", "Välju"]

subject_list = list(subjects.keys())

print("Tere tulemast hinde arvutaja programmi!")
print("Kas sa soovid oma andmed laadida eelmisest sessioonist? (jah/ei)")
load_choice = input().strip().lower()
if load_choice == "jah":
    saved_data = fn.get_local_data()
    if saved_data:
        print("Andmed leitud ja laetud.")
        print(saved_data)
    else:
        print("Eelnevaid andmeid ei leitud.")
print()


while True: #Põhiprogramm
    print("Mida teha soovid?")
    for i in käsud:
        print(f"- {i}")
    cmd_choice = input("Sisesta käsk: ").strip().lower()

    if cmd_choice != "välju":
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
                print("Vale valik!")
    print()
    alampiirid, max_punktid, hinded, punktid_hindeks = fn.aine_exel(subject) # Andmed tapelist
    match cmd_choice:
        case "sisesta punktid":
                if 'saved_data' in locals():
                    print("Kas tahad uuendada oma punkte või alustada algusest? (uuenda/algus)")
                    update_choice = input().strip().lower()
                    if update_choice == "uuenda":
                        # Kutsu `küsi_punktid`, edastades olemasolevad salvestatud andmed
                        grades[subject] = fn.küsi_punktid(max_punktid[0], saved_data.get(subject))
                    else:
                        grades[subject] = fn.küsi_punktid(max_punktid[0])
                else:
                    grades[subject] = fn.küsi_punktid(max_punktid[0])
        case "välju":
            print("Programm lõpetab töö.")
            print("Kas tahand andmed salvestada? (jah/ei)")
            save_choice = input().strip().lower()
            if save_choice == "jah":
                fn.local_save(grades)
                print("Andmed salvestatud.")
            break

"""
grades = fn.küsi_punktid(max_punktid[0])  # Preagu kasutame esimest katekooriat   !!!NB HILJEM MUUTA

kokku_punkte = sum(p for p in grades.values() if p is not None)

saadud_hinne = fn.arvuta_hinne(kokku_punkte, punktid_hindeks, hinded)

print(f"Sinu hinne ja punktid hetkel on: {saadud_hinne} ja {kokku_punkte} punkti.")


print("Nüüd vali õppeaine: ")
for i, subj in enumerate(subject_list, 1): #aine küsimine
    print(f"{i}. {subj}")

choice = int(input("Sisesta õppeaine number: "))
if 1 <= choice <= len(subject_list):
    subject_key = subject_list[choice - 1]
    subject = subjects[subject_key]
    print(f"Valisid: {subject_key}")
else:
    print("Vale valik!")
print()
alampiirid, max_punktid, hinded, punktid_hindeks = fn.aine_e(subject) # Andmed tapelist
"""