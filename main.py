"""Hinnete keskmine"""
grades = []
subject = input("Sisesta õppeaine: ")
print(f"Õppeaine: {subject}")
count = int(input("Mitu hinnet soovid sisestada? "))

for i in range(count):
    grade = float(input(f"Sisesta hinne {i+1} (protsentides): "))
    grades.append(grade)

average = sum(grades) / len(grades)

if average >= 50:
    print(f"Hindete keskmine: {average:.2f} - Läbitud")
else:
    print(f"Hindete keskmine: {average:.2f} - Mitte läbitud")
