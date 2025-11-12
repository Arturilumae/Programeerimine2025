"""Hinnete keskmine"""


grades = []
subjects = [
    "Programmeerimine I",
    "Arvuti arhitektuur ja riistvara",
    "Operatsioonisüsteemid",
    "Kõrgem Matemaatika I",
    "Sissejuhatus erialasse"
] #valikud, et kasutaja ei peaks käsitsi sisestama

for i, subj in enumerate(subjects, 1):
    print(f"{i}. {subj}")

choice = int(input("Vali õppeaine number: "))
subject = subjects[choice - 1]
print(f"Õppeaine: {subject}")
#kindlate nõuete funktsioon iga õppeaine kohta
count = int(input("Mitu hinnet soovid sisestada? "))

for i in range(count):
    grade = float(input(f"Sisesta hinne {i+1} (punktides): "))
    grades.append(grade)

average = sum(grades) / len(grades)

thresholds = {
    "Programmeeriimine I": 50,
    "Arvuti arhitektuur ja riistvara": 51,
    "Operatsioonisüsteemid": 50,
    "Kõrgem Matemaatika I": 50,
    "Sissejuhatus erialasse": 50
}
threshold = thresholds.get(subject, 50)

if average >= threshold:
    print(f"Hindete keskmine: {average:.2f} - Läbitud")
else:
    print(f"Hindete keskmine: {average:.2f} - Mitte läbitud")

