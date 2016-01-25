import csv

def read_file(f):
        data = []
        file_read = csv.reader(f)
        for row in file_read:
            data.append(row)
        return data

def write_file(data, f):
        writer = csv.writer(f)
        for row in data:
            writer.writerow(row)

f1 = open('students.csv')
f2 = open('courses.csv')
f3 = open('sessions.csv')

students = read_file(f1)
courses = read_file(f2)
sessions = read_file(f3)

dic = {}

for student in students:
    student[0], student[2] = student[2], student[0]
    if student[2] not in dic:
        dic[student[2]] = student
    else:
        course = student[3][1:]
        dic[student[2]].append(course)
student_specs = []
for i in dic:
    student_specs.append(dic[i])

dic_2 = {}

count = 0

for session in sessions:
    if session[1] not in dic_2:
        dic_2[session[1]] = [session[1],0,0,0,0,0]
    if session[3] == "Hoorcollege":
        dic_2[session[1]][1] += 1
    elif session[3] == "Werkcollege":
        dic_2[session[1]][2] += 1
        dic_2[session[1]][3] = session[4]
    elif session[3] == "Computer practicum":
        dic_2[session[1]][4] += 1
        dic_2[session[1]][5] = session[4]
    else:
        print "errrroore"

course_specs = []
for i in dic_2:
    course_specs.append(dic_2[i])

print course_specs



with open('student_specs.csv', 'wb') as o1:
    write_file(student_specs, o1)
with open('course_specs.csv', 'wb') as o2:
    write_file(course_specs, o2)
