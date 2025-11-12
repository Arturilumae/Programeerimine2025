import funktsioonid as fn # kus kõik funktsioonid on 

"""Hinnete keskmine"""
grades = []
subjects = [
    "Programmeerimine 1",
    "Arvuti arhitektuur ja riistvara",
    "Operatsioonisüsteemid",
    "Kõrgem Matemaatika 1",
    "Sissejuhatus erialasse"
]

for i, subj in enumerate(subjects, 1):
    print(f"{i}. {subj}")

choice = int(input("Vali õppeaine number: "))
subject = subjects[choice - 1]
alam_punktid, maks_punktid, aine_max, hinded, hinded_vordlus, punktid_hindeks = fn.aine(subject) # Andmed tapelist
print(f"Õppeaine: {subject}")
count = int(input("Mitu hinnet soovid sisestada? "))

for i in range(count):
    grade = float(input(f"Sisesta hinne {i+1} (protsentides): "))
    grades.append(grade)

average = sum(grades) / len(grades)


if average >= punktid_hindeks[4]:  # Kontrollime, kas keskmine on piisav E saamiseks
    print(f"Hindete keskmine: {average:.2f} - Läbitud")
else:
    print(f"Hindete keskmine: {average:.2f} - Mitte läbitud")

