class Student(object):
    """
    A Student represents a certain student

    """
    def __init__(self, student_id, courses):
        """
        Initializes a student with courses

        """
        self.id = student_id
        self.courses = courses
        self.sessions = []

class Course(object):
    """
    A Course represents a certain course.
    """
    def __init__(self, name, students):
        """
        Initializes a course with students

        """
        self.id = name
        self.students = students

    def numberStudents(self):
        """
        returns number of students

        """
        return len(self.students)


class Session(object):
    """
    A Session represents a certain session of a course.
    """
    def __init__(self, session_id, session_type, course, students):
        """
        Initializes a session with students

        """
        self.id = session_id
        self.type = session_type
        self.course = course
        self.students = students
        self.slot = ''

class Slot(object):
    """
    A  slot represents a certain slot in a room.
    """
    def __init__(self, slot_id, day, block, room, capacity):
        """
        Initializes a time_slot in a room

        """
        self.id = slot_id
        self.day = day
        self.block = block
        self.room = room
        self.capacity = capacity

def main():
    '''
    Extracts data from original CSV file (studenten_roostering).

    Creates random schedule.

    Outputs lists: student_list and course_list, which are lists of objects
    '''
    import csv
    import random

    # declares constants
    days = [0, 1, 2, 3, 4]
    blocks = [0, 1, 2, 3]

    # open csv files and reads into csv-file
    f1 = open('student_specs.csv')
    csv_file_1 = csv.reader(f1)
    f2 = open('course_specs.csv')
    csv_file_2 = csv.reader(f2)


    # empty list for student and course objects
    student_list = []
    course_list = []
    student_infos = []

    # extracts the id and courses of every student
    for csv_line in csv_file_1:
        student_infos.append(csv_line)

    for student_info in student_infos[1:]:
        student_id = student_info[2]
        courses_student = []
        for student_course in student_info[3:]:
            if student_course != "":
                courses_student.append(student_course)


        # create new student object and adds it to list
        student = Student(student_id, courses_student)

        student_list.append(student)

        # loops over courses of the student
        for course_student in courses_student:
            course_exists = False
            # checks if course already exists
            for course in course_list:
                if course.id == course_student:
                    course.students.append(student)
                    course_exists = True
            if course_exists == False:
                if course_student != '':
                    # creates new course object w
                    students = []
                    course = Course(course_student, students)
                    course_list.append(course)
                    course.students.append(student)


    # extracts the specifications of every course
    course_specifications = []
    for csv_line in csv_file_2:
        course_specifications.append(csv_line)

    session_list = []
    session_id = 0
    # creates different session objects for every course object
    for course in course_list:
        course_sessions = []
        num_students = course.numberStudents()

        for course_specification in course_specifications:
            if course.id == course_specification[0]:
                # creates lectures
                num_lectures = int(course_specification[1])
                for i in range(num_lectures):
                    session_type = "lecture"
                    new_lecture = Session(session_id, session_type, course.id, course.students)
                    session_id += 1
                    course_sessions.append(new_lecture)
                    session_list.append(new_lecture)
                    for student in course.students:
                        student.sessions.append(new_lecture)

                # creates tutorials
                if course_specification[2] != "0":
                    num_students_tutorial = int(course_specification[3])
                    num_tutorials = int((float(num_students) / float(num_students_tutorial)) + 1)
                    rest = course.students
                    for i in range(num_tutorials):
                        students_tutorial = rest[:num_students_tutorial]

                        rest = rest[num_students_tutorial:]
                        session_type = "tutorial"
                        new_tutorial = Session(session_id, session_type, course.id, students_tutorial)
                        session_id += 1
                        course_sessions.append(new_tutorial)
                        session_list.append(new_tutorial)
                        for student in students_tutorial:
                            student.sessions.append(new_tutorial)

                # creates practica
                if course_specification[4] != "0":
                    num_students_practicum = int(course_specification[5])
                    num_practicum = int((float(num_students) / float(num_students_practicum)) + 1)
                    rest = course.students
                    for i in range(num_practicum):
                        students_practicum = rest[:num_students_practicum]
                        rest = rest[num_students_practicum:]
                        session_type = "practicum"
                        new_practicum = Session(session_id, session_type, course.id, students_practicum)
                        session_id += 1
                        course_sessions.append(new_practicum)
                        session_list.append(new_practicum)
                        for student in students_practicum:
                            student.sessions.append(new_practicum)

    # extracts the specifications of every room
    room_specifications = [["A1.04",41], ["A1.06",22], ["C1.112",60]]

    # creates slot objects
    slot_id = 0
    slot_list = []
    for room_specification in room_specifications:
        for day in days:
            for block in blocks:
                new_slot = Slot(slot_id, day, block, room_specification[0], room_specification[1])
                slot_list.append(new_slot)
                slot_id += 1

    # returns list of student, session and slot objects
    return [session_list, slot_list]

main()
