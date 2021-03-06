import preparation
import fitness_function
import random

def capacity_conflict(session, fitness, capacity_minus):

    """ When there are not enough seats in the room points are subtracted

    """
    num_students = len(session.students)
    room_capacity = session.slot.capacity
    if num_students > room_capacity:
        fitness -= (num_students - room_capacity)
        capacity_minus += (num_students - room_capacity)
    return fitness, capacity_minus

def student_conflict(session, fitness, student_minus, student_dict):

    """ When a student has more sessions at one timeslot points are subtracted

    """
    # all students that folllow this session
    for student in session.students:
        student_id = student.id
        # checks if student is already in dictionary
        if student_id not in student_dict:
            student_dict[student_id] = []
            student_dict[student_id].append(session.slot)
        # when student is in dict check if conflicting timeslots
        else:
            conflict = False
            for slot in student_dict.get(student_id):
                if slot.day == session.slot.day and slot.block == session.slot.block:
                    conflict = True
            if conflict == True:
                fitness -= 1
                student_minus += 1
            else:
                student_dict[student_id].append(session.slot)
    return fitness, student_minus

def sequence_conflict(course, fitness, sequence_minus):

    """ When tutorial or practimcum are scheduled before lecture points subtracted

    """
    other = []
    lectures = []
    for session in course.sessions:
        if session.type == "lecture":
            lectures.append(session)
            if session.slot.day > 2:
                fitness -= len(session.students)
                sequence_minus += len(session.students)
        else:
            other.append(session)

    for session in other:
        for lecture in lectures:
            if session.slot.day < lecture.slot.day:
                fitness -= len(session.students)
                sequence_minus += len(session.students)
    return fitness, sequence_minus



def main(session_list, course_list):

    """ Every succesfull seat in the schedule earns one point for fitness

    """
    # defines variables
    fitness = 0
    capacity_minus = 0
    student_minus = 0
    sequence_minus = 0


    # all students with their timeslot will be filled
    student_dict =  {}

    for session in session_list:
        # adds 1 point to fitness for every student in session
        fitness += len(session.students)
        # subtract 1 point of fitness per student of capacity_conflict
        fitness, capacity_minus = capacity_conflict(session, fitness, capacity_minus)
        # subtract 1 point of fitness when student_conflict
        fitness, student_minus = student_conflict(session, fitness, student_minus, student_dict)

    for course in course_list:
        # subtract 1 point of fitness per student of sequence_conflict
        fitness, sequence_minus = sequence_conflict(course, fitness, sequence_minus)


    return fitness, capacity_minus, student_minus, sequence_minus
