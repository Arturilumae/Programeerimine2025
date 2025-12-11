import funktsioonid as fn # kus kõik funktsioonid on 

grades = { #ainete määramine
    "Programmeerimine 1": {},
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
käsud = ["Sisesta punktid", "Arvuta hinne #Pole valmis", "Loe salvestatud andmed", "Välju"]

subject_list = list(subjects.keys())

print("Tere tulemast hinde arvutaja programmi!")
print("Kas sa soovid oma andmed laadida eelmisest sessioonist? (jah/ei)")
load_choice = input().strip().lower()
if load_choice == "jah":
    saved_data = fn.get_local_data()
    if saved_data:
        grades = saved_data
        print("Andmed leitud ja laetud.")
    else:
        print("Eelnevaid andmeid ei leitud.")
print()


while True: #Põhiprogramm
    print("Mida teha soovid?")
    while True: #käskluse küsimine
        j=1
        for i in käsud:
            print(f"- {i}: {j}")
            j+=1
        cmd_choice = (input("Sisesta käsu number: ").strip())
        try:
            cmd_choice = int(cmd_choice)
            if 1 <= cmd_choice <= len(käsud):
                cmd_choice = käsud[cmd_choice - 1].lower()
                break
            else:
                print("Mitte sobiv valik.")
                print(f"Valik on 1-{j}.")
                continue
        except ValueError:
            cmd_choice = cmd_choice.lower()
            if cmd_choice in [k.lower() for k in käsud]:
                break
            else:               
                print(f"Palun sisesta kehtiv käsk.")
                continue 
    print()
    match cmd_choice:
        case "sisesta punktid":
            subject = fn.õppe_aine(subject_list,subjects)
            alampiirid, max_punktid, hinded, punktid_hindeks = fn.aine_exel(subject) # Andmed tapelist
            if 'saved_data' in locals() and saved_data != None:
                print("Kas tahad uuendada oma punkte või alustada algusest? (uuenda/algus)")
                update_choice = input().strip().lower()
                if update_choice == "uuenda":
                    # Kutsu `küsi_punktid`, edastades olemasolevad salvestatud andmed
                    grades[subject] = fn.küsi_punktid(max_punktid[0], grades.get(subject))
                else:
                    grades[subject] = fn.küsi_punktid(max_punktid[0])
            else:
                grades[subject] = fn.küsi_punktid(max_punktid[0])
        case "loe salvestatud andmed":
            fn.kuva_andmed(grades)
        case "arvuta hinne #pole valmis":
            subject = fn.õppe_aine(subject_list,subjects)
            alampiirid, max_punktid, hinded, punktid_hindeks = fn.aine_exel(subject) # Andmed tapelist
            fn.arvuta_hinne(grades[subject], alampiirid, punktid_hindeks, hinded, max_punktid)
        case "välju":
            print("Programm lõpetab töö.")
            print("Kas tahand andmed salvestada? (jah/ei)")
            save_choice = input().strip().lower()
            if save_choice == "jah":
                fn.local_save(grades)
                print("Andmed salvestatud.")
            break
