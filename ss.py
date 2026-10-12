

a=open("kk.py", "r")
s=a.readlines()
d=[]
r=[]

for i in range(len(s)):
    if len(s[i]) > 0 and s[i][0].isdigit():

        name = s[i].split("   ")[1].strip()

        marks = s[i + 1].split()

        c = int(marks[0]) + int(marks[2]) + int(marks[4]) + int(marks[6]) + int(marks[8]) + int(marks[10])
        j=(c/6)

        x = s[i].split()

        roll = x[0]
        name = ""
        j = 2

        if x[1] == "I":
            j = 3

        while j < len(x) and not (len(x[j]) == 3 and x[j].isdigit()):
            name = name + x[j] + " "
            j = j + 1

        name = name.strip()

        marks = s[i + 1].split()

        m1 = int(marks[0])
        m2 = int(marks[2])
        m3 = int(marks[4])
        m4 = int(marks[6])
        m5 = int(marks[8])
        m6 = int(marks[10])

        d.append([c,roll,name,m1,m2,m3,m4,m5,m6])

d.sort(reverse=True)

print(r)



a.close()
import csv
a = open("students.csv", "w", newline="")
w = csv.writer(a)

w.writerow(["Roll No", "Name", "Marks 1", "Marks 2",
            "Marks 3", "Marks 4", "Marks 5", "Marks 6", "Total"])

for i in d:
    w.writerow([i[1], i[2], i[3], i[4], i[5], i[6],
                i[7], i[8], i[0]])

a.close()
a=open("students.csv", "r")
k=csv.reader(a)
for l in k:
    print(l)
a.close

print("CSV file created")







